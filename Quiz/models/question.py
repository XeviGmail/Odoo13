# -*- coding: utf-8 -*-

from odoo import models, fields

class Question(models.Model):
    _name = 'quiz.question'
    _description = 'Quiz Questions'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Question'
    )

    answer = fields.Char(
        string='Answer'
    )

    extra = fields.Char(
        string='Extra'
    )

    type_ids = fields.Many2many(
        comodel_name='question.type',
        string='Type',
    )

    statistics_ids = fields.One2many(
        comodel_name='question.statistics',
        inverse_name='question_id',
        string='Statistics'
    )

    issue_id = fields.One2many(
        comodel_name='question.issue',
        inverse_name='question_id',
        string='Issue'
    )