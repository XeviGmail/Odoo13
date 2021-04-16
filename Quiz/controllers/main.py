# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class Main(http.Controller):

    ''' Listado de questions con un html basico
        Esto de usar <html> solo es para fines didacticos, no hay que usarlo en produccion
        En produccion hay que usar request.render()

        request.env = self.env
        request.session
        request.session.sid
    '''
    @http.route('/questions/questions_list', type='http', auth='none')
    def questions_list(self):
        questions = request.env['quiz.question'].sudo().search([])
        html_result = '<html><body><ul>'
        for question in questions:
            html_result += f'<li>{question.name}</li>'
        html_result += '<ul><body><html>'
        return html_result

    # No funciona porque hay mas de una base de datos
    @http.route('/questions/questions_list/json', type='json', auth='none')
    def questions_list_json(self):
        questions = request.env['quiz.question'].sudo().search([])
        return questions.read(['name'])

    #Consumir parametros
    @http.route('/questions/question_details', type='http', auth='none')
    def question_details(self, question_id):
        record = request.env['quest.question'].sudo().browse(int(question_id))
        html_result = f'<html><body><h1>{record.name}</h1>'
        return html_result

    @http.route('/questions/submit_issues', type='http', auth="user", website=True)
    def questions_issues(self, **post):
        if post.get('question_id'):
            question_id = int(post.get('question_id'))
            description = post.get('description')
            request.env['question.issue'].sudo().create({
                'question_id': question_id,
                'description': description,
                'submitted_by': request.env.user.id
            })
            return request.redirect('/questions/submit_issues?submitted=1')

        return request.render('Quiz.questions_issue_form', {
            'questions': request.env['quiz.question'].search([]),
            'submitted': post.get('submitted', False)
        })

    @http.route('/questions/ask_question', type='http', auth='user', website=True)
    def questions_ask_question(self):
        return request.render('Quiz.questions_ask_question_form', {
            'questions': request.env['quiz.question'].search([]),
        })


