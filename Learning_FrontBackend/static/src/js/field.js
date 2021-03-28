odoo.define('Learning_FrontBackend.field', (require) => {

    const registry = require('web.field_registry');
    const Widget = require('web.AbstractField');

    const FieldForShare = Widget.extend({
        // Busca un ID externo para renderizar la vista asociada al ID externo
        template: 'Learning_FrontBackend.share_button',
        events: {
            'click .js_reset_field': 'resetShareCount'
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

    console.warn('FUNCIONO')

    registry.add('share_count_widget', FieldForShare)

})