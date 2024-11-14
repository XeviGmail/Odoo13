from odoo import models, fields, api
from odoo.exceptions import RedirectWarning
from datetime import timedelta
import json

imc_mapping = {
    'underweight': (0, 18.5),
    'normal': (18.5, 25),
    'overweight': (25.0, 30),
    'oc1': (30.0, 35),
    'oc2': (35.0, 40),
    'oc3': (40, float('inf')),
}

days = {
    'day': 1,
    'week': 7,
    'month': 30
}

class HealthRecord(models.Model):
    _name = 'health.record'
    _description = 'Health Record'
    _rec_name = 'day'

    day = fields.Date(string='Date', default=fields.Date.today())
    user_id = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.user)
    weight = fields.Float(string='Weight (kg)', digits=(5, 2))
    weight_history = fields.Char(compute='_compute_weight_history')
    weight_path = fields.Char(compute='_compute_weight_path')
    glycemic_index = fields.Integer('Glycemic Index')
    waist_size = fields.Integer('Waist size')
    exercise = fields.Text(string='Exercise')
    food_intake_ids = fields.One2many(comodel_name='food.intake', inverse_name='health_record_id', string='Food intake')
    exercise_ids = fields.One2many(comodel_name='exercise.line', inverse_name='health_record_id', string='Exercises')
    initial_weight = fields.Float(related='user_id.initial_weight', store=True, readonly=False)
    desired_weight = fields.Float(related='user_id.desired_weight', store=True, readonly=False)
    by_interval_decrease = fields.Integer(related='user_id.by_interval_decrease', string='Decrease (gr)', store=True, readonly=False)
    by_interval = fields.Selection(related='user_id.by_interval', store=True, readonly=False)
    final_day = fields.Date(compute='_compute_final_day', help='Final day depending of the todays weight')
    final_initial_day = fields.Date(compute='_compute_final_initial_day', help='Final day depending of the first weight')
    initial_day = fields.Date(related='user_id.initial_day', string='Initial day', store=True, readonly=False)
    daily_calories = fields.Integer(string='Daily Calories', compute='compute_daily_calories')
    remaining_calories = fields.Integer(string='Calory Remaining', compute='compute_remaining_calories')
    height = fields.Integer(string='Height (.cm)', related='user_id.height', store=True, readonly=False)
    date_of_birth = fields.Date(string='Date of birth', related='user_id.date_of_birth', store=True, readonly=False)
    tmb = fields.Float(string='Tasa Metabolica Basal', compute='_compute_tmb')
    gedt = fields.Float(string='Gasto Energetico Diario Total', compute='_compute_gedt')
    caloric_deficit = fields.Integer(string='Caloric Deficit', related='user_id.caloric_deficit', store=True, readonly=False)
    activity = fields.Selection(related='user_id.activity', store=True, readonly=False)
    sex = fields.Selection(related='user_id.sex', store=True, readonly=False)
    diet_type = fields.Selection(related='user_id.diet_type', store=True, readonly=False)
    imc = fields.Float(compute='_compute_imc')
    imc_selection = fields.Selection(
        selection=[
            ('underweight', 'Underweight (BMI: < 18.5)'),
            ('normal', 'Normal weight (BMI: 18.5 - <25.0)'),
            ('overweight', 'Overweight (BMI: 25.0 - <30.0)'),
            ('oc1', 'Obesity class 1 (Mild obesity) (BMI: 30.0 - <35.0)'),
            ('oc2', 'Obesity class 2 (Moderate obesity) (BMI: 35.0 - <40.0)'),
            ('oc3', 'Obesity class 3 (Severe or morbid obesity) (BMI: >= 40)'),
        ],
        string='IMC',
        compute='_compute_imc_selection'
    )
    weight_low_imb = fields.Float(string='Weight to next low IMC (low than...)', compute='compute_weight_low_imb')
    target_calculation = fields.Selection(related='user_id.target_calculation', store=True, readonly=False)
    by_final_day = fields.Date(related='user_id.by_final_day', store=True, readonly=False)

    @api.onchange('target_calculation')
    def onchange_target_calculation(self):
        if self.target_calculation == 'date':
            if self.final_day:
                days = self.by_final_day - fields.Date.today()
                print('days', days.days)
                weight_lose = self.weight - self.desired_weight
                by_end_date_decrease = weight_lose / days.days
                print(by_end_date_decrease, weight_lose, days.days)

    @api.depends('imc')
    def compute_weight_low_imb(self):
        for r in self:
            if r.imc:
                low, high = imc_mapping[r.imc_selection]
                r.weight_low_imb = low * ((r.height/100) ** 2)
            else:
                r.weight_low_imb = False

    @api.depends('weight', 'height')
    def _compute_imc(self):
        for r in self:
            if r.height > 0 and r.weight > 0:
                r.imc = r.weight / ((r.height/100) ** 2)
            else:
                r.imc = False

    @api.depends('imc')
    def _compute_imc_selection(self):
        for r in self:
            if r.imc > 0:
                r.imc_selection = next(key for key, (low, high) in imc_mapping.items() if low <= r.imc < high)
            else:
                r.imc_selection = False  # En caso de que la altura sea 0 o menor

    # @api.depends('day', 'weight', 'initial_day', 'by_interval_decrease', 'by_interval')
    # def _compute_weight_path(self):
    #     first_date_record = self.env['health.record'].search([('user_id', '=', self.user_id.id)], order='day asc', limit=1)
    #     first_date = first_date_record.day if first_date_record else None
    #     delta = self.by_final_day - first_date
    #     for r in self:
    #         lista_path = list()
    #         decrease_per_day = (self.initial_weight - self.desired_weight) / delta.days
    #         for i in range(delta.days + 1):
    #             actual_date = first_date + timedelta(days=i)
    #             registro = self.env['health.record'].search([('day', '=', actual_date), ('user_id', '=', r.user_id.id)])
    #             if registro:
    #                 lista_path.append((actual_date.strftime('%Y-%m-%d'), registro.weight, self.weight - (i * decrease_per_day)))
    #             else:
    #                 lista_path.append((actual_date.strftime('%Y-%m-%d'), None, self.weight - (i * decrease_per_day)))
    #         r.weight_path = json.dumps(lista_path)

    # @api.depends('day', 'weight', 'initial_day', 'by_interval_decrease', 'by_interval')
    # def _compute_weight_history(self):
    #     for r in self:
    #         registros = self.env['health.record'].search([('day', '<=', r.day), ('user_id', '=', r.user_id.id)])
    #         lista = list()
    #         for registro in registros:
    #             if self.initial_day and self.by_interval and self.by_interval_decrease:
    #                 decrease_per_day = (r.by_interval_decrease / days[r.by_interval]) / 1000
    #                 passed_days = (registro.day - r.initial_day).days
    #                 wish_lose_weight = (passed_days * decrease_per_day) if (passed_days * decrease_per_day) > 0 else 0
    #                 if registro.id == r._origin.id:
    #                     lista.append((registro.day.strftime('%Y-%m-%d'), self.weight, self.initial_weight - wish_lose_weight))
    #                 else:
    #                     lista.append((registro.day.strftime('%Y-%m-%d'), registro.weight, registro.initial_weight - wish_lose_weight))
    #             else:
    #                 if registro.id == r._origin.id:
    #                     lista.append((registro.day.strftime('%Y-%m-%d'), self.weight))
    #                 else:
    #                     lista.append((registro.day.strftime('%Y-%m-%d'), registro.weight))
    #
    #         r.weight_history = json.dumps(lista)

    @api.depends('by_interval_decrease', 'by_interval', 'weight', 'desired_weight')
    def _compute_final_day(self):
        """
        Calcula la fecha en la que habremos conseguido nuestro pero ideal
        """
        for r in self:
            if r.weight and r.by_interval_decrease and r.by_interval and r.desired_weight:
                weight_to_lose = r.weight - r.desired_weight
                days_to_goal = weight_to_lose / ((r.by_interval_decrease / days[r.by_interval] ) / 1000)
                r.final_day = fields.Date.today() + timedelta(days=days_to_goal)
            else:
                r.final_day = False

    @api.depends('by_interval_decrease', 'by_interval', 'initial_weight', 'desired_weight', 'initial_day')
    def _compute_final_initial_day(self):
        """
        Calcula la fecha en la que habremos conseguido nuestro pero ideal
        """
        for r in self:
            if r.initial_weight and r.by_interval_decrease and r.by_interval and r.desired_weight and r.initial_day:
                weight_to_lose = r.initial_weight - r.desired_weight
                days_to_goal = weight_to_lose / ((r.by_interval_decrease / days[r.by_interval] ) / 1000)
                r.final_initial_day = r.initial_day + timedelta(days=days_to_goal)
            else:
                r.final_initial_day = False

    @api.depends('tmb', 'activity')
    def _compute_gedt(self):
        activity = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'high': 1.725,
            'very': 1.9
        }
        for r in self:
            print('r.activity', r.activity)
            if r.activity:
                r.gedt = r.tmb * activity[r.activity]
            else:
                r.gedt = r.tmb
    @api.depends('caloric_deficit', 'gedt')
    def compute_daily_calories(self):
        for r in self:
            r.daily_calories = r.gedt - r.caloric_deficit
    @api.depends('height', 'date_of_birth', 'weight', 'sex')
    def _compute_tmb(self):
        for r in self:
            if r.date_of_birth:
                years = fields.Date.today().year - r.date_of_birth.year
                if r.sex == 'female':
                    r.tmb = 447.593 + (9.247 * r.weight) + (3.098 * r.height) - (4.330 * years)
                else:
                    r.tmb = 88.362 + (13.397 * r.weight) + (4.799 * r.height) - (5.677 * years)
            else:
                r.tmb = 0
    @api.depends('food_intake_ids', 'gedt')
    def compute_remaining_calories(self):
        for r in self:
            r.remaining_calories = r.daily_calories
            for intake in r.food_intake_ids:
                r.remaining_calories -= intake.calories


    @api.model
    def default_get(self, fields_list):
        """
        Al crear un nuevo registro, verificaremos que el dia de hoy ya tenga un registro, si es asi:
        - Lanzamos un aviso
        - Cargaremos ese registro si el usuario lo desea.
        """
        # Obtener el valor predeterminado de los campos
        defaults = super().default_get(fields_list)

        # Obtener el día y el usuario actual
        day = defaults.get('day', fields.Date.today())
        user_id = self.env.user.id

        # Buscar un registro existente con el mismo día y usuario
        existing_record = self.search([('day', '=', day), ('user_id', '=', user_id)], limit=1)
        if existing_record:
            # Redirigir al formulario del registro existente
            action_error = {
                'view_mode': 'form',
                'name': 'Record',
                'res_model': 'health.record',
                'type': 'ir.actions.act_window',
                'res_id': existing_record.id,
                'views': [[False, 'form']],
                'target': 'current',
            }
            raise RedirectWarning(
                'A record already exists for this date. You will be redirected to the existing record.',
                action_error,
                'Open Record'
            )

        return defaults