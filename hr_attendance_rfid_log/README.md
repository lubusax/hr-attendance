**Module Purpose:** This module provides an intermediary logging layer between external RFID
  terminals and Odoo's hr.attendance model, capturing raw clocking events to prevent
  them from accumulating on devices. It features an UI (displaying both successful
  and failed syncs) coupled with a transient wizard to troubleshoot database sync errors
  and map new RFID cards to employees. Includes a scheduled cron job to automatically
  purge old records, utilizing separate retention periods for successful versus failed
  events.
  
  **UI that displays both successful and failed syncs**
  In this picture you can see the three typical cases that the View found in (Attendances > Reporting > Logs) shows now.
   ![[Pasted image 20260320100620.png]]
  
  The log in the picture shows a "successful sync" log that will be shown there for a certain period defined in a cron delete entry.
  
  It shows also two "falied sync" logs:
  1. one is caused because "No employee found with card xxx". When clicking on this entry a wizard view will appear allowing the user to take actions with this clocking.  (a) the user can assign an employee to this "new" card, (b) the user can "ignore" the clocking or (c) the user can let odoo "retry" to sync the clocking.
![[Pasted image 20260320102113.png]]

  2. the second "failed sync" shows a typical error that says "ValidationError("Cannot create new attendance record for Anita Oliver, the employee hasn't checked out since 03/16/2026 15:38:38", None)". This error can be solved for example when a "check out" is added just after the timestamp mentioned in the error. After fixing this, the user can click on "retry" in the wizard view of the "rfid logs" and then the clocking will be sync successfully.
![[Pasted image 20260320102031.png]]