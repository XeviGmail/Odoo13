odoo.define('Learning_FrontBackend.field', (require) => {

    const registry = require('web.field_registry');
    const Widget = require('web.AbstractField');

    const FieldForShare = Widget.extend({
        // Busca un ID externo para renderizar la vista asociada al ID externo
        template: 'Learning_FrontBackend.share_button',

        // isSet evalua cuando hay que mostrar el widget
        isSet(){
            // Queremos que se muestre siempre
            return true
        },

    });

    console.warn('FUNCIONO')

    registry.add('share_count_widget', FieldForShare)

})