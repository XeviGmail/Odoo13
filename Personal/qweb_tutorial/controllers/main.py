# -*- coding: utf-8 -*-

from odoo import http

class QwebTutoriasl(http.Controller):
    # Definimos la ruta en la que estara disponible esta accion
    @http.route('/qweb-tutorials', type='http', auth='public', website=True)

    # metodo que se usara al entrar en la ruta
    def qweb_tutorials(self):
        """ QWEB Tutorials"""
        def hello_function():
            return "Helo my friend"

        model = http.request.env['res.partner'].search([])

        data = {
            'string': "This is a string",
            'integer': 1000,
            'some_float': 9.8,
            'boolean': True,
            'some_list': [1, 2, 3, 4, 5],
            'some_dictionary': {'name': 'Xevi', 'surname': 'Mesones'},
            'hello_function': hello_function(),
            'model': model,
        }
        """ 
        renderizamos una plantilla qweb
        <template id="somePythonTemplate">
        """
        return http.request.render("qweb_tutorial.somePythonTemplate", data)