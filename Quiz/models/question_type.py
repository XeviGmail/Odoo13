# -*- coding: utf-8 -*-

from odoo import models, fields

class QuestionType(models.Model):
    _name = 'question.type'
    _description = 'Question Type'

    name = fields.Char(
        string='Type'
    )

    question_ids = fields.Many2many(
        comodel_name='quiz.question',
        string='Questions',
    )