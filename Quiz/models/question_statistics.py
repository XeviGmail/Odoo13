# -*- coding: utf-8 -*-

from odoo import models, fields

class QuizStatistics(models.Model):
    _name = 'question.statistics'
    _description = 'Question Statistics'

    question_id = fields.Many2one(
        comodel_name='quiz.question',
        string='Question',
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
    )

    # how many times this question is asked to this user
    asked_times = fields.Integer(
        string='Asked'
    )

    # how many times this question is answered correctly
    correct_answers = fields.Integer(
        string='Correct Answer'
    )

    # how many times this question is answered wrong
    wrong_answers = fields.Integer(
        string='Wrong Answer'
    )

    # last answer was...
    last_answer = fields.Boolean(
        string='Last Answer'
    )