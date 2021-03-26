// We are declaring an external frontend widget

odoo.define('Learning_FrontBackend.button', (require) => {

    // con require importamos modulos JS de oddo
    const {Widget, registry} = require('web.public.widget');

    // importamos el modulo Dialog de web
    const Dialog = require('web.Dialog');

    const WidgetButton = Widget.extend({
        // Aqui asociamos el elemento con este widget
        selector: '.js_class_button_to_share',
        events: {
            'click button': 'clickEvent',
        },
        clickEvent(ev){
            Dialog.alert(
                this,
                'Has clicado un boton',
                {
                    title: 'Exito!'
                }
            )
        },

    });

    // registramos el widget en el espacio publico, esto SOLO se ejecutara en el Frontend
    registry.WidgetButton = WidgetButton;

});