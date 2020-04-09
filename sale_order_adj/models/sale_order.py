# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_manager_user_id = fields.Many2one(
        related='project_project_id.user_id',
        string='Project Manager',
    )
    gross_profit_margin = fields.Float(
        string='Gross Profit Margin',
    )
