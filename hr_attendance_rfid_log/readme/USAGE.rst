#. The HR employee responsible to set up new employees should go to
   'Attendances -> Manage Attendances -> Employees' and register the
   RFID card code of each of your employees. You can use an USB plugged
   RFID reader connected to your computer for this purpose.
#. The employee should put his/her card to the RFID based employee
   attendance system. It is expected that the system will provide some form
   of output of the registration event.

You can monitor all synced events by going to **Attendances > Reporting > Logs**.
This view displays both successful and failed syncs.

- **Successful Syncs:** These are kept in the log for a period defined by a scheduled job.
- **Failed Syncs:** When an error occurs during syncing, the record will show as failed.
  Clicking on a failed record opens a wizard that allows you to resolve the issue:

  1. **"No employee found with card xxx":** You can assign an employee to this new card,
     ignore the clocking, or ask Odoo to retry syncing.
  2. **Validation Errors (e.g., missing check-out):** If an employee hasn't checked out,
     you will see an error. After fixing the attendance record (e.g., adding a manual
     check-out), you can click "Retry" in the wizard to successfully sync the event.
