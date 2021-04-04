odoo.define('Learning_FrontBackend.ie_followers', function (require) {
    "use strict";

    const Followers = require('mail.Followers');
    console.log("FUERA ESTOY VIVO!!!!!");

    var internal_followers
    var internal_mail_followers

    Followers.include({

        willStart: async function () {
            console.log('WILL START() ')

            /*
            console.log(this.record.id)
            console.log('this.record: ', this.record)
            console.log('this.record: ', this.record['context'])
            console.log('this.value.res_ids: ', this.value.res_ids)
            */
            this._super.apply(this, arguments);
            // Aqui conseguimos los usuarios internos
            var internal_users = await this._rpc({
                model: 'res.groups',
                method: 'search_read',
                domain: [['id','=',1]],
                fields: ['id','name','users'],//8, 6, 2 (usuaris de odoo)
            });
            // Aqui conseguimos la relacion entre usuario interno y el seguidor interno (Cliente)
            internal_followers = await this._rpc({
                model: 'res.users',
                method: 'search_read',
                domain: [['id','in',internal_users[0].users]],
                fields: ['partner_id'],
                // 8 -> 43 (anna Baeza)
                // 6 -> 7 (Marc Demo)
                // 2 -> 3 (Michael Admin)
            });

            console.log('record.res_model: ', this.record.model)
            internal_mail_followers = await this._rpc({
                model: 'mail.followers',
                method: 'search_read',
                domain: [['id', 'in', this.value.res_ids]],
                fields: ['id', 'partner_id'],
            });
            console.log('internal_mail_followers: ', internal_mail_followers)
        },

        renderElement: function() {
            console.log('RenderElement: ')
            this._super(...arguments);
            /*
                Aqui faig malabars,
                Vull una llista de followers i si s'ha de mostrar o no la bola del mon
                [[2,''], [10,''], [3,'invisible'], [7,'invisible'], [43,'invisible']]
                els que coincideixin, no mostraran la bola del mon ja que son interns
            */
            var lista = []
            var list_element
            this.newValue = []
            var internal_followers_list = []
            internal_followers.forEach(function(element){
                internal_followers_list.push(element.partner_id[0])
            });

            internal_mail_followers.forEach(function(element){
                list_element = []
                list_element.push(element.partner_id[0])
                if (internal_followers_list.includes(element.partner_id[0])){
                    list_element.push('fa fa-globe invisible')
                } else {
                    list_element.push('fa fa-globe')
                }
                lista.push(list_element)
            });
            var d = new Date();
            var n = d.getTime();
            console.log('Time: ', d.getTime())
            this.newValue = lista
        },
    });
});

/*
    La idea es que antes de renderizar el elemento pasar class="invisible" a los elementos que no se tengan que mostrar
    porque son internos
*/