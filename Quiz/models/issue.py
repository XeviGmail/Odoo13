# -*- coding: utf-8 -*-

from odoo import models, fields

class QuestionIssues(models.Model):
    _name = 'question.issue'

    question_id = fields.Many2one(
        comodel_name='quiz.question',
        string='Question',
        required=True,
    )

    submitted_by = fields.Many2one(
        comodel_name='res.users',
    )

    description = fields.Text()