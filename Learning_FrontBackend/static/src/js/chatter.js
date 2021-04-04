odoo.define('Learning_FrontBackend.chatter', function(){

    const {PortalComposer} = require('portal.composer');

    PortalComposer.include({
        xmlDependencies: [
            '/Learning_FrontBackend/static/src/xml/chatter.xml',
        ],
    });

});