# -*- coding: utf-8 -*-

from odoo import models, fields, api
from random import choice

class Quiz(models.TransientModel):
    _name = 'quiz.quiz'
    _description = 'Quiz'

    wrong_answers_set = {-1}
    wrong_answers_set.remove(-1)

    question_id = fields.Integer()
    name = fields.Char(
        string='Question',
    )

    user_answer = fields.Char(
        string='Your Answer'
    )

    answer = fields.Char(
        string='Answer'
    )

    extra = fields.Char(
        string='Extra'
    )

    default_question_types_ids = fields.Many2many(
        comodel_name='question.type',
        string='Question Types'
    )

    default_number_of_questions = fields.Integer(
        string='Number of questions',
        default=lambda self: self.get_setting('number_of_questions'),
        help='0 means No limit'
    )

    # GAME: the actual cuestion number of the game
    question_counter = fields.Integer(
        string='Question number',
        default=0
    )

    start_new_game = fields.Boolean(
        default=False
    )

    end_game = fields.Boolean(
        default=False
    )

    fix_errors = fields.Boolean(default=False)

    # if checking_answer = True then
    #   answer and extra are visible
    checking_answer = fields.Boolean(
        default=False
    )

    @api.depends('question_counter')
    def _get_statistic_question_counter(self):
        if self.question_counter == 0:
            self.statistic_question_counter = 0
        else:
            self.statistic_question_counter = 100.0 * float(self.question_counter) / float(self.default_number_of_questions)

    statistic_question_counter = fields.Float(
        string='Asked questions',
        compute='_get_statistic_question_counter'
    )

    wrong_answers = fields.Integer(
        default=0
    )

    @api.depends('wrong_answers')
    def _get_statistic_wrong_answers(self):
        if self.wrong_answers == 0:
            self.statistic_wrong_answers = 0
        else:
            self.statistic_wrong_answers = 100.0 * float(self.wrong_answers) / float(self.default_number_of_questions)

    statistic_wrong_answers = fields.Float(
        string='Wrong Answers',
        compute='_get_statistic_wrong_answers'
    )

    correct_answers = fields.Integer(
        default=0
    )

    @api.depends('correct_answers')
    def _get_statistic_correct_answers(self):
        if self.correct_answers == 0:
            self.statistic_correct_answers = 0
        else:
            self.statistic_correct_answers = 100.0 * float(self.correct_answers) / float(self.default_number_of_questions)

    statistic_correct_answers = fields.Float(
        string='Correct Answers',
        compute='_get_statistic_correct_answers'
    )

    # Question Error handling
    count_error_handling = fields.Integer(
        string='Errors to be handled',
        default=0,
    )

    def new_question(self, questions):
        """
            IA de preguntas:
            1.- pregunta sin estadisticas (Randomize)
            2.- ultima respuesta incorrecta
                2.1 - la que no tenga respuestas correctas
                    2.1.1 - la que tenga mas respuestas erroneas (asi se repiten mas amenudo)
                2.2- la que tenga la relacion preguntas error / preguntas ok mas grande
            3.- todas las utlimas respuestas correctas
                3.1- la que se haya preguntado menos 
        """
        # IA
        # Preguntas sin estadisticas
        print('questions: ', questions.ids)
        print('questions: ', questions.search([('id', 'in', questions.ids),('statistics_ids', '=', False)]).ids)
        possible_questions_ids = questions.search([('id', 'in', questions.ids),('statistics_ids', '=', False)]).ids
        if len(possible_questions_ids) == 0:
            possible_questions_ids = questions.search([('id', 'in', questions.ids),('statistics_ids.last_answer', '=', False)]).ids
            print('more_possible_questions_ids: ', possible_questions_ids)
            if possible_questions_ids == 0:
                possible_questions_ids = questions.ids

        print('len(possible_questions) ', len(possible_questions_ids))
        print('possible_questions ', possible_questions_ids)

        id = choice(possible_questions_ids)
        print('id: ', id)
        return questions.search([('id', '=', id)])

        # random de una de las preguntas
        #id = choice(questions) - 1
        return questions.search([('id', '=', id)])

    def clean_all_fields(self):
        self.name = ''
        self.user_answer = ''
        self.answer = ''
        self.extra = ''

    def btn_load_new_question(self):
        if self.question_counter < self.default_number_of_questions:
            self.checking_answer = False
            self.question_counter += 1
            self.clean_all_fields()
            print(self.env['quiz.question'].search([('type_ids','in',self.default_question_types_ids.ids)]))
            question = self.new_question(self.env['quiz.question'].search([('type_ids','in',self.default_question_types_ids.ids)]))
            self.question_id = question.id
            self.name = question.name
            self.answer = question.answer
            self.extra = question.extra
        elif len(self.wrong_answers_set) > 0:
            self.count_error_handling = 100 * len(self.wrong_answers_set) / self.wrong_answers
            self.fix_errors = True
            self.checking_answer = False
            self.clean_all_fields()
            print('len(self.wrong_answers_set): ', len(self.wrong_answers_set))
            lista = list(self.wrong_answers_set)
            # id = lista.pop()
            # print('id: ', id)
            id = choice(lista)
            question = self.env['quiz.question'].search([('id', '=', id)])
            self.question_id = question.id
            self.name = question.name
            self.answer = question.answer
            self.extra = question.extra
        else:
            self.manage_end_of_game()
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'quiz.quiz',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def manage_end_of_game(self):
        print('manage_end_of_game')
        self.end_game = True;

    def exist_statistics_record(self):
        return self.env['question.statistics'].search([('question_id', '=', self.question_id), ('user_id', '=', self.env.user.id)])


    def statistics_record(self):
        record = self.exist_statistics_record()
        if not record:
            record = self.env['question.statistics'].create({
                'question_id': self.question_id,
                'user_id': self.env.user.id,
            })
        return record

    def correct_answer(self):
        if not self.fix_errors:
            self.correct_answers += 1
            record = self.statistics_record()
            record.write({
                'asked_times': record.asked_times + 1,
                'correct_answers': record.correct_answers + 1,
                'last_answer': True,
            })
        else:
            print('correct')
            self.wrong_answers_set.remove(self.question_id)

    def wrong_answer(self):
        if not self.fix_errors:
            self.wrong_answers += 1
            self.wrong_answers_set.add(self.question_id)
            print('self.wrong_answers_set: ', self.wrong_answers_set)
            record = self.statistics_record()
            record.write({
                'asked_times': record.asked_times + 1,
                'wrong_answers': record.wrong_answers + 1,
                'last_answer': False,
            })

    def btn_check_answer(self):
        if self.answer == self.user_answer:
            self.correct_answer()
        else:
            self.wrong_answer()

        self.checking_answer = True
        print('self.fix_errors: ', self.fix_errors)
        print('self.default_number_of_questions: ', self.default_number_of_questions)
        print('self.question_counter: ', self.question_counter)
        print('self.wrong_answers_set: ', self.wrong_answers_set)
        if self.default_number_of_questions == self.question_counter and len(self.wrong_answers_set) == 0:
            self.count_error_handling = 0
            print('self.end_game = True;')
            self.end_game = True;

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'quiz.quiz',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def btn_start_new_game(self):
        if self.question_counter == 0 or self.question_counter == self.default_number_of_questions:
            self.correct_answers = 0
            self.wrong_answers = 0
            self.start_new_game = True
            self.end_game = False
            self.checking_answer = False
            self.question_counter = 0
            self.btn_load_new_question()
            self.fix_errors = False
        else:
            print('The game has already begun')

        return {
            'context': self.env.context,
            'view_mode': 'form',
            'res_model': 'quiz.quiz',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def btn_set_as_default(self):
        self.env['ir.config_parameter'].set_param('Quiz.number_of_questions', self.default_number_of_questions)

    def get_setting(self, setting):
        return self.env['ir.config_parameter'].sudo().get_param(f'Quiz.{setting}')