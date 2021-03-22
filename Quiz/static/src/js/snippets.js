odoo.define('quiz.dynamic.snippet', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.quiz = publicWidget.Widget.extend({
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
            fields: ['name', 'date_release'],
            orderBy: [{ name: 'date_release', asc: false }],
            limit: parseInt(rows)
        }).then(function (data) {
            _.each(data, function (book) {
                self.$el.append(
                    $('<tr />').append(
                        $('<td />').text(book.name),
                        $('<td />').text(book.date_release)
                    ));
            });
        });
    },
});

});
