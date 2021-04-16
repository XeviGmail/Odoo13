odoo.define('Quiz.chatter_quiz_button', function (require) {
"use strict";

var Chatter = require('mail.Chatter');

Chatter.include({
    events: _.extend({}, Chatter.prototype.events, {
        'click .o_chatter_button_new_quest': '_onClickOpenQuiz',
        'click .o_chatter_button_question_type': '_onClickQuestionType',
    }),

    _onClickQuestionType(){

        this.do_action({
             views: [[false, 'form']],
             view_type: 'form',
             view_mode: 'form',
             res_model: 'question.type',
             type: 'ir.actions.act_window',
             target: 'current',
             res_id: this.record.data.type_ids.res_ids[0],
        });
    },

    _onClickOpenQuiz(){
        this.do_action({
             views: [[false, 'form']],
             view_type: 'form',
             view_mode: 'form',
             res_model: 'quiz.quiz',
             type: 'ir.actions.act_window',
             target: 'new',
        });
    },

});

});

/*
this.do_action({
             views: [[false, 'form']],
             view_type: 'form',
             view_mode: 'form',
             res_model: 'product.product',
             type: 'ir.actions.act_window',
             target: 'current',
             res_id: 4,
        });*/
