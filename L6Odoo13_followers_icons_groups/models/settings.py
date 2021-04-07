# -*- coding: utf-8 -*-

from odoo import fields, models, api

class FollowersIconsGroupsSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # @api.model
    # def default_get(self, fields):
    #     res = super(FollowersIconsGroupsSettings, self).default_get(fields)
    #
    #     if not res['internal']:
    #         res['internal'] = 'fa fa-address-book'
    #
    #     if not res['portal']:
    #         res['portal'] = 'fa fa-sign-in'
    #
    #     if not res['public']:
    #         res['public'] = 'fa fa-globe'
    #
    #     return res

    internal = fields.Char(
        string='Internal',
    )

    @api.depends('internal')
    def _get_internal_icon(self):
        self.internal_icon = self.internal

    internal_icon = fields.Char(
        compute='_get_internal_icon',
    )

    portal = fields.Char(
        string='Portal',
    )

    @api.depends('portal')
    def _get_portal_icon(self):
        self.portal_icon = self.portal

    portal_icon = fields.Char(
        compute='_get_portal_icon',
    )

    public = fields.Char(
        string='External',
    )

    @api.depends('public')
    def _get_public_icon(self):
        self.public_icon = self.public

    public_icon = fields.Char(
        compute='_get_public_icon',
    )


    #Function that saves the values to the DDBB
    def set_values(self):
        res = super(FollowersIconsGroupsSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('L6Odoo13_followers_icons_groups.internal', self.internal if self.internal else 'fa fa-address-book')
        self.env['ir.config_parameter'].set_param('L6Odoo13_followers_icons_groups.portal', self.portal if self.portal else 'fa fa-sign-in')
        self.env['ir.config_parameter'].set_param('L6Odoo13_followers_icons_groups.public', self.public if self.public else 'fa fa-globe')
        return res

    #Function that loads the values from the DDBB
    def get_values(self):
        res = super(FollowersIconsGroupsSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        xinternal = ICPSudo.get_param('L6Odoo13_followers_icons_groups.internal')
        xportal = ICPSudo.get_param('L6Odoo13_followers_icons_groups.portal')
        xpublic = ICPSudo.get_param('L6Odoo13_followers_icons_groups.public')
        res.update(
            internal=xinternal,
            portal=xportal,
            public=xpublic,
        )
        return res

