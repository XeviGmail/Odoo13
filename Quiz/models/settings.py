# -*- coding: utf-8 -*-

from odoo import fields, models

class QuizSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    number_of_questions = fields.Integer(
        string='Number of Questions'
    )

    #Function that saves the values to the DDBB
    def set_values(self):
        res = super(QuizSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('Quiz.number_of_questions', self.number_of_questions)
        return res

    #Function that loads the values from the DDBB
    def get_values(self):
        res = super(QuizSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        xnumber_of_questions = ICPSudo.get_param('Quiz.number_of_questions')
        res.update(
            number_of_questions=int(xnumber_of_questions),
        )
        return res