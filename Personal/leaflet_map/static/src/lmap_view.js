//* @odoo-module */

import { registry } from "@web/core/registry"
import { Component, xml } from "@odoo/owl"

class LeafletMapController extends Component{
    static template = xml`<div>Leaflet Map View</div>`;
}

const leafletMapView = {
    type: "lmap",
    display_name: "Leaflet Map",
    icon: "fa fa-map-marker",
    multiRecord: true,
    Controller:LeafletMapController,
}

registry.category("views").add("lmap", leafletMapView)