odoo.define('Learning_FrontBackend.ie_followers', function (require) {
"use strict";

const Followers = require('mail.Followers');
console.log("FUERA ESTOY VIVO!!!!!");

var core = require('web.core');
var _t = core._t;
var QWeb = core.qweb;
var d = 0;

Followers.include({
    _displayFollowers: async function () {
        var self = this;
        // Aqui conseguimos los usuarios internos
        var internal_users = await this._rpc({
            model: 'res.groups',
            method: 'search_read',
            domain: [['id','=',1]],
            fields: ['id','name','users'],//8, 6, 2 (usuaris de odoo)
        });
        // Aqui conseguimos la relacion entre usuario interno y el seguidor interno (Cliente)
        var internal_followers = await this._rpc({
            model: 'res.users',
            method: 'search_read',
            domain: [['id','in',internal_users[0].users]],
            fields: ['partner_id'],
            // 8 -> 43 (anna Baeza)
            // 6 -> 7 (Marc Demo)
            // 2 -> 3 (Michael Admin)
        });
        d = d + 1
        console.log('valor de d: ', d)
        console.log('internal_users', internal_followers[0].partner_id)
        var internal_followers_list = []
        internal_followers.forEach(function(element){
            internal_followers_list.push(element.partner_id[0])
        });
        // render the dropdown content
        var $followers_list = this.$('.o_followers_list').empty();
        $(QWeb.render('mail.Followers.add_more', {widget: this})).appendTo($followers_list);
        var $follower_li;
        var internal
        _.each(this.followers, function (record) {
            console.log('record: ', record)

            if(!record.active) {
                record.title = _.str.sprintf(_t('%s \n(inactive)'), record.name);
            } else {
                record.title = record.name;
            }
            if (internal_followers_list.includes(record.res_id)){
                internal = true;
            } else {
                internal = false;
            }
            $follower_li = $(QWeb.render('mail.Followers.partner', {
                'record': _.extend(record, {
                    'avatar_url': '/web/image/' + record.res_model + '/' + record.res_id + '/image_128',
                    'internal': internal,
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

/*
    La idea es que antes de renderizar el elemento pasar class="invisible" a los elementos que no se tengan que mostrar
    porque son internos
*/