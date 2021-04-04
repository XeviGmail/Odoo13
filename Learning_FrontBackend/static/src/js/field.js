odoo.define('Learning_FrontBackend.field', (require) => {

    // 'web.field_registry' -> importacion especifica para registrar los fields
    const registry = require('web.field_registry');

    // 'web.AbstractField' -> importamos los widgets en el Backend, esto implementa all lo necesario para que se pueda
    // renderizar all en el Backend
    const Widget = require('web.AbstractField');

    const FieldForShare = Widget.extend({
        // Busca un ID externo para renderizar la vista asociada al ID externo
        template: 'Learning_FrontBackend.share_button',
        events: {
            'click .js_reset_field': 'resetShareCount'
        },
        renderElement () {
            this.newValue = Intl.NumberFormat().format(this.value);
            this._super(...arguments);
        },
//        async resetShareCount(ev){
//            await this._setValue('0');
//            this.renderElement();
//        },

        resetShareCount(){
            this._setValue('0');
        },


        // isSet evalua cuando hay que mostrar el widget
        isSet(){
            // Queremos que se muestre siempre
            return true
        },

    });

    // 'share_count_widget' -> el nombre del widget que tendra en los xml
    registry.add('share_count_widget', FieldForShare)

})