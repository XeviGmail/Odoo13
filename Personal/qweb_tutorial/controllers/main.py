# -*- coding: utf-8 -*-

from odoo import http

class QwebTutoriasl(http.Controller):
    @http.route('/qweb-tutorials', type='http', auth='public')
    def qweb_tutorials(self):
        """ QWEB Tutorials"""

        return http.request.render("qweb_tutorial.somePythonTemplate")