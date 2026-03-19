# NURZEIT GmbH - Module Development Context

`<role_instruction>`

You are developing a specific Odoo module for NURZEIT GmbH. You must strictly adhere to
the global architecture rules defined in the `.ai_docs/` folder at the root of this
repository.

`</role_instruction>`

`<module_context>`

- **Module Name:** [hr_attendance_rfid_log]

- **Target Odoo Version:** [13.0]

- **Business Purpose:** [Provides an intermediary logging layer between external RFID
  terminals and Odoo's hr.attendance model, capturing raw clocking events to prevent
  them from accumulating on devices. It features an admin UI (displaying both successful
  and failed syncs) coupled with a transient wizard to troubleshoot database sync errors
  and map new RFID cards to employees. Includes a scheduled cron job to automatically
  purge old records, utilizing separate retention periods for successful versus failed
  events.]

`</module_context>`

`<routing_directive>`

BEFORE writing or modifying any code in this module:

1. Verify the Target Odoo Version listed above.

2. Read the global rules in `.ai_docs/common_rules/`.

3. Read the strict syntax rules in `.ai_docs/v[Target Version]_specific/`.

   `</routing_directive>`
