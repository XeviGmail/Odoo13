# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class Main(http.Controller):
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
    def questions_ask_question(self, **post):
        return request.render('Quiz.questions_ask_question_form', {
            'questions': request.env['quiz.question'].search([]),
        })