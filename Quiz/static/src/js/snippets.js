// Paso 4
odoo.define('question.dynamic.snippet', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

// Paso 5
publicWidget.registry.question = publicWidget.Widget.extend({
    selector: '.question_snippet',
    disabledInEditableMode: false,
    start: function () {
        var self = this;
        var rows = this.$el[0].dataset.numberOfQuestions || '5';
        console.log(this.$el[0])
        this.$el.find('td').parents('tr').remove();
        this._rpc({
            model: 'quiz.question',
            method: 'search_read',
            domain: [],
            fields: ['name', 'answer', 'create_date'],
            orderBy: [{ name: 'create_date', asc: false }],
            limit: parseInt(rows)
        }).then(function (data) {
            _.each(data, function (question) {
                self.$el.append(
                    $('<tr />').append(
                        $('<td />').text(question.name),
                        $('<td />').text(question.answer)
                    ));
            });
        });
        document.querySelector(".btn").addEventListener("click", function () {
            console.log(self.$el);
            console.log('rows: ', rows)
        });
    },
});

document.querySelector(".btn").addEventListener("click", function () {
  console.log("button clicked");
});

});
