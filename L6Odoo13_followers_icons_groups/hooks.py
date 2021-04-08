from odoo import api, SUPERUSER_ID

def set_default_settings_values(cr, registry):
    """ Post init function"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.config_parameter'].set_param('L6Odoo13_followers_icons_groups.internal', 'fa fa-address-book')
    env['ir.config_parameter'].set_param('L6Odoo13_followers_icons_groups.portal', 'fa fa-sign-in')
    env['ir.config_parameter'].set_param('L6Odoo13_followers_icons_groups.public', 'fa fa-globe')
