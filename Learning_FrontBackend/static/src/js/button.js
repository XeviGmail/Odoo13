// We are declaring an external frontend widget

odoo.define('Learning_FrontBackend.button', (require) => {

    // con require importamos modulos JS de oddo
    // 'web.public.widget' es para declarar widgets publicos
    const {Widget, registry} = require('web.public.widget');

    // importamos el modulo Dialog de web
    const Dialog = require('web.Dialog');

    const WidgetButton = Widget.extend({
        // Aqui asociamos el elemento con este widget
        // Crea un widget por cada instancia encontrada
        selector: '.js_class_button_to_share',

        // Declaramos los eventos que esten siempre dentro de widget
        events: {
            'click button': 'clickEvent',
        },

        // Para crear eventos sobre el propio widget
        // Uno de los metodos que representa el ciclo de vida de un widget
        start(){
            //Se llama antes de que el widget se incluya en el DOM, justo despues de que se renderice

            this._super(...arguments);
            // this.el = 'HTMLElement'
            // this.$el = 'JQuery'
            new ClipboardJS(this.el, {
                text: () => document.location.origin + this.el.dataset.url
            });

        },
        clickEvent(ev){
            Dialog.alert(
                this,
                document.location.origin + this.el.dataset.url,
                {
                    title: 'Exito!'
                }
            );
            return document.location.origin + this.el.dataset.url
        },

    });

    // registramos el widget en el espacio publico, esto SOLO se ejecutara en el Frontend
    registry.WidgetButton = WidgetButton;

    // Esto permite a desarrolladores heredar este widget con require
    return WidgetButton;

});