# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Duplicate Purchase Order Lines",
    "summary": "",
    "description": """
- Add "Duplicate Purchase Lines" button to sale order form view that will 
duplicate specific order line in the purchase order.
    """,
    "version": "10.0.1.0.0",
    "category": "Purchase",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase",
    ],
    "data": [
        'views/purchase_order_views.xml',
    ],
}
