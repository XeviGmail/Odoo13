from odoo import models, fields

class ExerciseLine(models.Model):
    _name = 'exercise.line'
    _description = 'Exercise Line'

    health_record_id = fields.Many2one(comodel_name='health.record', string='Health Record')
    exercise_id = fields.Many2one(comodel_name='exercise.type', string='Exercise')
    hours = fields.Float(string='Hours')