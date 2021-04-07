odoo.define('Learning_FrontBackend.ie_followers', function (require) {
"use strict";

const Followers = require('mail.Followers');
console.log("FUERA ESTOY VIVO!!!!!");

var core = require('web.core');
var _t = core._t;
var QWeb = core.qweb;

var settings = []

Followers.include({

    start: async function () {
        this._super.apply(this, arguments);

        //Settings
        var internal = await this._rpc({
            model: 'ir.config_parameter',
            method: 'get_param',
            args: [
                'L6Odoo13_followers_icons_groups.internal',
            ],
        });
        settings.push(['Internal User', internal])

        var portal = await this._rpc({
            model: 'ir.config_parameter',
            method: 'get_param',
            args: [
                'L6Odoo13_followers_icons_groups.portal',
            ],
        });
        settings.push(['Portal', portal])

        var publico = await this._rpc({
            model: 'ir.config_parameter',
            method: 'get_param',
            args: [
                'L6Odoo13_followers_icons_groups.public',
            ],
        });
        settings.push(['Public', publico])
    },

    _displayFollowers: async function () {
        var self = this;

        console.log('settings: ', settings)

        /*  Tipos de Usuarios:
                1 -> Internal User
                8 -> Portal
                9 -> Public
        */
        var internal_user = 1
        var portal = 8

        var internal_users = await this._rpc({
            model: 'res.groups',
            method: 'search_read',
            domain: [['id','=',internal_user]],
            fields: ['id','name','users'],
        });

        var portal = await this._rpc({
            model: 'res.groups',
            method: 'search_read',
            domain: [['id','=',portal]],
            fields: ['id','name','users'],
        });

        // Aqui conseguimos la relacion entre usuario interno y el seguidor interno (Cliente)
        var internal_followers = await this._rpc({
            model: 'res.users',
            method: 'search_read',
            domain: [['id','in',internal_users[0].users]],
            fields: ['partner_id'],
        });

        var internal_followers_list = []
        internal_followers.forEach(function(element){
            internal_followers_list.push(element.partner_id[0])
        });

        //Relacion entre el usuario Portal y el seguidor interno (Cliente)
        var portal_followers = await this._rpc({
            model: 'res.users',
            method: 'search_read',
            domain: [['id','in',portal[0].users]],
            fields: ['partner_id'],
        });

        var portal_followers_list = []
        portal_followers.forEach(function(element){
            portal_followers_list.push(element.partner_id[0])
        });

        // render the dropdown content
        var $followers_list = this.$('.o_followers_list').empty();
        $(QWeb.render('mail.Followers.add_more', {widget: this})).appendTo($followers_list);
        var $follower_li;
        var user_type
        var user_icon
        _.each(this.followers, function (record) {

            if(!record.active) {
                record.title = _.str.sprintf(_t('%s \n(inactive)'), record.name);
            } else {
                record.title = record.name;
            }
            if (internal_followers_list.includes(record.res_id)){
                user_type = settings[0][0];
                user_icon = settings[0][1];
            } else if (portal_followers_list.includes(record.res_id)){
                user_type = settings[1][0];
                user_icon = settings[1][1];
            } else {
                user_type = settings[2][0];
                user_icon = settings[2][1];
            }
            $follower_li = $(QWeb.render('mail.Followers.partner', {
                'record': _.extend(record, {
                    'avatar_url': '/web/image/' + record.res_model + '/' + record.res_id + '/image_128',
                    'user_type': user_type,
                    'user_icon': user_icon,
                }),
                'widget': self})
            );
            $follower_li.appendTo($followers_list);

            // On mouse-enter it will show the edit_subtype pencil.
            if (record.is_editable) {
                $follower_li.on('mouseenter mouseleave', function (e) {
                    $(e.currentTarget).find('.o_edit_subtype').toggleClass('d-none', e.type === 'mouseleave');
                });
            }
        });

        // clean and display title
        this.$('.o_followers_actions').show();
        this.$('.o_followers_title_box > button').prop('disabled', !$followers_list.children().length);
        this.$('.o_followers_count')
            .html(this.value.res_ids.length)
            .parent().attr('title', this._formatFollowers(this.value.res_ids.length));
    },
});
});
