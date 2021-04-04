// We are declaring an external frontend widget

odoo.define('Learning_FrontBackend.button', (require) => {

    // con require importamos modulos JS de oddo
    // 'web.public.widget' es para declarar widgets publicos y nos retorna un objeto con varios valores:
    // Widget: es la clase principal donde crearemos el nuevo widget
    // Registry: donde registraremos el nuevo widget
    const {Widget, registry} = require('web.public.widget');

    // importamos el modulo Dialog de web
    const Dialog = require('web.Dialog');

    // extend crea un prototipo nuevo para el nuevo widget
    const WidgetButton = Widget.extend({
        // Crea un widget por cada instancia encontrada
        // Selector, asocia este widget con un selector css, es decir con el Boton que hemos creado
        selector: '.js_class_button_to_share',

        // Declaramos los eventos que esten siempre dentro de widget

        events: {
            // click -> Evento
            // button -> selector css
            // clickEvent -> Funcion
            'click .share_button': 'clickEvent',
        },

        // Para crear eventos sobre el propio widget
        // Uno de los metodos que representa el ciclo de vida de un widget
        // El metodo Start() Se llama justo despues de que se renderice, y antes de que el widget se incluya en el DOM
        start(){
            // usamos _super() para saltar los permisos del usuario.
            this._super(...arguments);
            // this.el = 'HTMLElement' es un DOM element
            // this.$el = 'JQuery'
            new ClipboardJS(this.el, {
                text: () => document.location.origin + this.el.dataset.url
            });

        },
        async clickEvent(){
            await this._rpc({
                route: '/update/share/count',
                params: {product_id: this.el.dataset.id}
            });
            Dialog.alert(
                this,
                'El producto ' + this.el.dataset.name + ' con URL: ' + document.location.origin + this.el.dataset.url,
                {
                    title: 'Exito!'
                }
            );
        },
    });

    // registramos el widget en el espacio publico, esto SOLO se ejecutara en el Frontend
    registry.WidgetButton = WidgetButton;

    // Esto permite a desarrolladores heredar este widget con require
    return WidgetButton
});