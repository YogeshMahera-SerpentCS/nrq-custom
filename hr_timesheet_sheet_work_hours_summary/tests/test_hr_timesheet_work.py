# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time
from datetime import datetime

from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TestHrTimesheetSheet(common.TransactionCase):

    def setUp(self):
        super(TestHrTimesheetSheet, self).setUp()
        self.holiday_model = self.env["hr.holidays.public"]
        self.holiday_model_line = self.env["hr.holidays.public.line"]
        self.timesheet_sheet = self.env['hr_timesheet_sheet.sheet']
        self.test_employee = self.browse_ref('hr.employee_qdp')
        self.resource_id = self.env.ref('resource.timesheet_group1')
        self.test_timesheet_sheet = self.timesheet_sheet.create({
            'date_from': self.timesheet_sheet._default_date_from(),
            'date_to': self.timesheet_sheet._default_date_to(),
            'name': 'Gilles Gravie',
            'state': 'new',
            'user_id': self.browse_ref('base.user_demo').id,
            'employee_id': self.test_employee.id,
        })

    def test_compute_works_hours(self):
        # Check Standard Hours without resource set
        self.assertEqual(self.test_timesheet_sheet.standard_work_hours, 0)
        self.test_timesheet_sheet.employee_id.write({
            'calendar_id': self.resource_id.id
        })

        self.test_timesheet_sheet._compute_standard_work_hours()

        # Check Standard Hours with resource set
        date_from = datetime.strptime(str(
            self.test_timesheet_sheet.date_from),
            DEFAULT_SERVER_DATE_FORMAT).date()

        hours = ((datetime.today().date() - date_from).days + 1) * 8

        self.assertEqual(
            self.test_timesheet_sheet.standard_work_hours,
            hours,
            "The Standard Hours did not match the with value"
        )

        # Create holidays
        holiday2 = self.holiday_model.create({
            'year': time.strftime('%Y'),
            'country_id': self.test_employee.user_id.partner_id.country_id.id
        })

        self.holiday_model_line.create({
            'name': 'holiday 1',
            'date': datetime.today().date(),
            'year_id': holiday2.id
        })
        self.test_timesheet_sheet.employee_id.write({
            'calendar_id': self.resource_id.id
        })

        self.test_timesheet_sheet._compute_holiday_hours()

        date_to = self.test_timesheet_sheet.date_to if\
            self.test_timesheet_sheet.date_to > str(datetime.now().date())\
            else self.test_timesheet_sheet.date_to

        holidays = self.env['hr.holidays.public.line'].search_count([
            ('date', '>=', self.test_timesheet_sheet.date_from),
            ('date', '<=', date_to),
            ('year_id.year', '=', datetime.now().year)])

        holidays_hours = holidays * 8

        # Check Holiday Hours
        self.assertEqual(
            self.test_timesheet_sheet.holiday_hours,
            holidays_hours,
            "The Holiday Hours did not match the with value")

        # Check Expected Hours
        self.assertEqual(
            self.test_timesheet_sheet.expected_work_hours,
            self.test_timesheet_sheet.standard_work_hours -
            self.test_timesheet_sheet.holiday_hours,
            "The Expected Hours did not match the with value")

        self.test_timesheet_sheet.write({
            'timesheet_ids': [(0, 0, {
                'project_id': self.browse_ref('project.project_project_2').id,
                'date': datetime.today().date(),
                'name': 'Develop yaml for hr module(2)',
                'user_id': self.browse_ref('base.user_demo').id,
                'unit_amount': 8.00,
                'product_id': self.browse_ref('product.product_product_1').id,
            })]})

        # Check Overtime Working Hours
        self.assertEqual(
            self.test_timesheet_sheet.overtime_hours,
            self.test_timesheet_sheet.total_timesheet -
            self.test_timesheet_sheet.expected_work_hours,
            "The Overtime Working Hours did not match the with value")

        standard_work_hours = \
            self.test_timesheet_sheet.get_standard_work_hours(
                self.test_timesheet_sheet.date_to)
        holiday_hours = self.test_timesheet_sheet.get_holiday_hours(
            self.test_timesheet_sheet.date_to)

        # Check Timesheet Expected Working Hours
        self.assertEqual(
            self.test_timesheet_sheet.timesheet_expected_work_hours,
            standard_work_hours - holiday_hours,
            "The Overtime Working Hours did not match the with value")
