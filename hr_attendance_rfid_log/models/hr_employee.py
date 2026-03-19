# Copyright 2023 - thingsintouch.com
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields
from datetime import datetime

import freezegun


class HrEmployeeBase(models.AbstractModel):

    _inherit = "hr.employee.base"

    @api.model
    def register_attendance(self, card_code, log=False, iot_device_id=False):
        res = super().register_attendance(card_code)
        if iot_device_id:
            res["iot_device_id"] = iot_device_id
        new_log = self._prepare_attendance_rfid_log(res)
        if log:
            log.sudo().write(
                new_log
            )
        else:
            self.env["hr.attendance.rfid.log"].create(
                new_log
            )
        res["in_rfid_log"] = True
        return res

    def _prepare_attendance_rfid_log(self, res):
        vals = {
            "state": "success" if res.get("logged") else "failed",
            "rfid_card_code": res.get("rfid_card_code"),
            "employee_name": res.get("employee_name"),
            "employee_id": res.get("employee_id"),
            "error_message": res.get("error_message"),
            "logged": res.get("logged"),
            "action": res.get("action"),
            "timestamp": fields.Datetime.now()
        }
        if "iot_device_id" in res:
            vals["iot_device_id"] = res["iot_device_id"]
        return vals

    @api.model
    def register_attendance_with_log(self, log):
        with freezegun.freeze_time(datetime.fromtimestamp(log.timestamp.timestamp(), tz=None)):
            result = self.register_attendance(log.rfid_card_code, log, iot_device_id=log.iot_device_id.id if log.iot_device_id else False)
        return result
