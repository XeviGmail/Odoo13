# -*- coding: utf-8 -*-

from odoo import models, fields

class UsersQuizSettings(models.Model):
    _inherit = 'res.users'

    question_type_ids = fields.Many2many(
        comodel_name='question.type',
        string='Question types',
    )

    number_of_questions = fields.Integer(
        string='Number of Questions',
    )
