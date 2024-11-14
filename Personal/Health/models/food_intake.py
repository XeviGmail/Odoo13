from odoo import models, fields, api

class FoodIntake(models.Model):
    _name = 'food.intake'
    _description = 'Food Intake'

    health_record_id = fields.Many2one(comodel_name='health.record')
    ingredient_id = fields.Many2one(comodel_name='ingredient.information', string='Ingredient')
    weight = fields.Float(string='Weight (gr.)')
    calories = fields.Integer(string='Calories', compute='compute_calories')
    glycemic_index = fields.Integer(string='Glycemix index', related='ingredient_id.glycemic_index')
    glycemic_load = fields.Float(string='Glycemic load', compute='compute_glycemic_load')
    fiber = fields.Float(string='Fiber', compute='compute_fiber')
    protein = fields.Float(string='Protein', compute='compute_protein')
    net_carbohydrates = fields.Float(string='Net Carbohydrates', help='Carbs - Fiber', compute='compute_net_carbohydrates')
    carbohydrates = fields.Float(string='Carbohydrates', compute='compute_carbohydrates')
    fat = fields.Float(string='Fat', compute='compute_fat')
    info = fields.Text(related='ingredient_id.info', string='Info', readonly=False, store=True)

    @api.depends('carbohydrates', 'fiber')
    def compute_net_carbohydrates(self):
        for r in self:
            r.net_carbohydrates = r.carbohydrates - r.fiber

    @api.depends('ingredient_id', 'weight', 'carbohydrates', 'fiber')
    def compute_glycemic_load(self):
        for r in self:
            r.glycemic_load = (r.glycemic_index * (r.carbohydrates - r.fiber)) / 100
    @api.depends('ingredient_id', 'weight')
    def compute_calories(self):
        for r in self:
            r.calories = r.ingredient_id.calories * r.weight / 100
    @api.depends('ingredient_id', 'weight')
    def compute_fiber(self):
        for r in self:
            r.fiber = r.ingredient_id.fiber * r.weight / 100
    @api.depends('ingredient_id', 'weight')
    def compute_protein(self):
        for r in self:
            r.protein = r.ingredient_id.protein * r.weight / 100
    @api.depends('ingredient_id', 'weight')
    def compute_carbohydrates(self):
        for r in self:
            r.carbohydrates = r.ingredient_id.carbohydrates * r.weight / 100
    @api.depends('ingredient_id', 'weight')
    def compute_fat(self):
        for r in self:
            r.fat = r.ingredient_id.fat * r.weight / 100
