odoo.define('L6Odoo13_followers_icons_groups.name2value', function(require){

console.log('PAPARRUCHAS')

const Widget = require('web.AbstractField');
const registry = require('web.field_registry');

const FieldForShow = Widget.extend({
    template: 'L6Odoo13_followers_icons_groups.name2value',
    isSet(){
        return true
    },
});

registry.add('name2value', FieldForShow)

});