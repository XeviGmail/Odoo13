from odoo import models, fields, api

class ingredientInformation(models.Model):
    _name = 'ingredient.information'
    _description = 'ingredient Information'

    name = fields.Char(string='ingredient Name', required=True)
    calories = fields.Integer(string='Calories ( kcal / 100 gr.)')
    glycemic_index = fields.Integer(string='Glycemix index')
    carbohydrates = fields.Float(string='Carbohydrates')
    net_carbohydrates = fields.Float(string='Net Carbohydrates', help='Carbs - Fiber', compute='compute_net_carbohydrates')
    fiber = fields.Float(string='Fiber')
    protein = fields.Float(string='Protein')
    fat = fields.Float(string='Fat')
    info = fields.Text(string='Info')

    @api.depends('carbohydrates', 'fiber')
    def compute_net_carbohydrates(self):
        for r in self:
            r.net_carbohydrates = r.carbohydrates - r.fiber
