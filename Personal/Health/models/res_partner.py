from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    initial_weight = fields.Float(string='Initial Weight')
    desired_weight = fields.Float(string='Desired Weigth')
    height = fields.Integer(string='Height (cm)')
    date_of_birth = fields.Date(string='Date of birth')
    caloric_deficit = fields.Integer(string='Caloric Deficit')
    activity = fields.Selection(
        selection=[
            ('sedentary', 'Sedentary (little or no exercise)'),
            ('light', 'Light activity (light exercise or sport 1-3 days/week)'),
            ('moderate', 'Moderate activity (moderate exercise or sport 3-5 days/week)'),
            ('high', 'High activity (intense exercise or sport 6-7 days/week)'),
            ('very', 'Very high activity (very intense exercise, physical work, or two workouts per day)'),
        ],
        string='Activity',
        required=True,
    )
    sex = fields.Selection(
        selection=[
            ('female', 'Female'),
            ('male', 'Male'),
        ],
        string='Sex'
    )
    diet_type = fields.Selection(
        selection=[
            ('protein', 'Diet high in protein and soluble fiber.'),
            ('fat', 'Diet high in Fat.'),
            ('carbs', 'Diet high in Carbohydrates'),
        ],
        string='Diet type'
    )
    by_interval = fields.Selection(
        selection=[
            ('day', 'Day'),
            ('week', 'Week'),
            ('month', 'Month'),
        ],
        string='Interval',
    )
    by_interval_decrease = fields.Integer(string='Decrease (gr)')
    initial_day = fields.Date(string='Initial day')
    target_calculation = fields.Selection(
        selection=[
            ('date', 'By End Date'),
            ('weight', 'For Weight Loss'),
        ],
        string='Target calculation'
    )
    by_final_day = fields.Date(string='Final day')