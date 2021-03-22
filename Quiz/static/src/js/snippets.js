odoo.define('question.dynamic.snippet', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.question = publicWidget.Widget.extend({
    selector: '.question_snippet',
    disabledInEditableMode: false,
    start: function () {
        var self = this;
        var rows = this.$el[0].dataset.numberOfQuestions || '5';
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
    },
});

});
