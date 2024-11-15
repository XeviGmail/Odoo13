from odoo import models, fields

class XmScript(models.Model):
    _name = 'xms.contact'
    _description = 'XMS Contact'

    name = fields.Char()
    age = fields.Integer()
