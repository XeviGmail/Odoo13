====
Quiz
====

.. contents::

Origin
======
* We take the lesson from here
    https://www.youtube.com/watch?v=w3VtCsq-avo&t=7932s

Description
===========

Module to Learn Frontend and Backend

Add a button to an element in the shop that copies the URL of the element


Objectives
==========

Learn the WEB model in Odoo13

Versions
========


Improvements
============

Creadits
========

Authors
-------
* Xevi Mesones (x.mesones@gmail.com)
    Adder Computer Developer - https://www.addercomputer.com/


Mainteiners
-----------
* This software is maintained by Xevi Mesones

Learning
========
* Las templates con la tag <odoo> se renderizan con python, por tanto sera True / False, no true / false, eso es en JS
(Frontend)
1.- En product.xml modificamos la vista añadiendo un boton
2.- Crearemos un assets.xml para añadir el fichero button.js al bundle (paquete) de Frontend
3.- Creamos button.js para añadirle funcionalidades al boton
    Para pasar informacion del widget(xml) al widget(js) usamos
        desde xml (t-att-data-variable o t-attf-data-variable) para cargar info a la variable
        desde js this.el.dataset.variable obtenemos el valor que cargamos en xml

(Backend)
Queremos un campo en el Backend para ver las veces a las que se la ha dado al boton que hemos creado en el Frontend
1.- Creamos el campo nuevo y lo declaramos como Integer
2.- Definiremos como lo queremos ver en /static/src/xml/fields.xml
    Asi lo añadimos al __manifest__.py
    'qweb': [
        'static/src/xml/field.xml',
    ],


(General)
En las vistas
    <template> es para el Frontend
    <record> es para el Backend
La <t> sirve tanto para las vistas de Backend como para las de Frontend

(Modificar un Widget existente)
"extend" crea una nueva instancia de un Widget
"include" Modificas un widget existente
Por lo tanto usaremos "include" para modificar el widget

