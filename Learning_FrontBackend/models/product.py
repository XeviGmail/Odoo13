# -*- coding: utf-8 -*-

from odoo import models, fields

class ProductInherit(models.Model):
    _inherit = 'product.template'

    share_count = fields.Integer()