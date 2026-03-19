# Proposal: Why `iot_device_name` is blank and how to fix it

## Problem Description
In `hr_attendance_log_view.xml`, the tree view includes the field `iot_device_name`, which is a related field pointing to `iot_device_id.name` defined in the Python model `hr.attendance.rfid.log`. However, it displays a blank value instead of the expected IoT device name.

## Potential Causes

1. **Access Rights for `iot.device`:**
   If the user viewing the RFID logs does not have `read` access to the `iot.device` model, Odoo will not be able to evaluate the related field `iot_device_id.name` for that user. Consequently, the value will appear blank in the UI, or Odoo will silently suppress it to prevent security violations.

2. **The IoT Device Record Doesn't Exist or the ID is Invalid:**
   If the `iot_device_id` field is successfully populated but points to a record ID that doesn't actually exist in the `iot.device` database table (perhaps due to being deleted or a database inconsistency), the related name will be blank.

3. **No IoT Device Passed During Logging:**
   The process creating the log (`hr.employee`'s `register_attendance` method) might not be passing the `iot_device_id` correctly. If the base `iot_device_id` field on the log record itself is null/empty, the related name will also obviously be blank.

## Codebase Analysis on `iot_device_id` propagation

We investigated the repository to see if `iot_device_id` is passed correctly between the modules handling the RPC call.

1. In the base module (`hr_attendance_rfid`), the method `register_attendance` is defined as:
   ```python
   @api.model
   def register_attendance(self, card_code):
       # ...
   ```
2. In the dependent module (`hr_attendance_rfid_log`), this method is overridden as:
   ```python
   @api.model
   def register_attendance(self, card_code, log=False, iot_device_id=False):
       res = super().register_attendance(card_code)
       if iot_device_id:
           res["iot_device_id"] = iot_device_id
       # ...
   ```

### Findings:
Because external systems call `register_attendance` via RPC, they might encounter issues passing `iot_device_id`. If they send it as a keyword argument (e.g., `iot_device_id=5`), it will only work if `hr_attendance_rfid_log` is installed. If only `hr_attendance_rfid` is installed, this will result in a `TypeError` due to an unexpected keyword argument in the base method.

Conversely, if external systems strictly rely on the base method's signature, they won't pass `iot_device_id` at all, resulting in empty values for `iot_device_id` and consequently blank `iot_device_name` fields.

### Recommendations for changes:
To fix this and ensure the ID is always passed without risking method signature conflicts, we recommend the following changes:

1. **Update `hr_attendance_rfid` base module:** Modify the `register_attendance` signature in `hr_attendance_rfid/models/hr_employee.py` to gracefully accept arbitrary keyword arguments or explicitly accept `iot_device_id`. E.g.,
   ```python
   @api.model
   def register_attendance(self, card_code, **kwargs):
       # ...
   ```

2. **Check external systems:** Update the external systems making the RPC call to ensure they actually send the `iot_device_id` in their payload. If they are sending it as part of kwargs, step 1 will resolve the issue and safely propagate the parameter to overriding methods like the one in `hr_attendance_rfid_log`.

## How to Manually Check and Fix

### Step 1: Verify `iot_device_id` is populated
To determine if this is just a related field issue or a missing data issue, add the `iot_device_id` directly to your view temporarily:
```xml
<field name="iot_device_id" />
```
Upgrade the module and refresh the page. If the ID is empty, the problem is in the data creation (the `iot_device_id` is never being passed or saved).

### Step 2: Check Access Rights
If `iot_device_id` is populated (e.g., showing a valid link like "IoT Device #3") but the `iot_device_name` is still blank, check the access rights for the model `iot.device`.
1. Enable Odoo Developer Mode.
2. Go to **Settings > Technical > Security > Access Rights**.
3. Search for the Object `iot.device`.
4. Ensure that the group assigned to the current user (or the `base.group_user` / `base.group_system` depending on who is accessing the view) has **Read Access** checked for `iot.device`.

If missing, you must define or update an access right in your security files (e.g., `security/ir.model.access.csv` in the `iot` or current module) granting read permissions to `iot.device` for the relevant groups.

### Step 3: Run Database Queries (Technical Verification)
Use a PostgreSQL client or Odoo's shell to check the raw data:
```sql
SELECT iot_device_id FROM hr_attendance_rfid_log ORDER BY id DESC LIMIT 10;
```
If you see valid IDs, verify they exist in the `iot_device` table:
```sql
SELECT id, name FROM iot_device WHERE id IN (SELECT iot_device_id FROM hr_attendance_rfid_log);
```
If the records exist and have names, the issue is certainly Access Rights or a UI cache issue (update module/clear cache).
