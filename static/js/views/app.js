var app = app || {};

$(function($) {
    app.AppView = Backbone.View.extend({
        el: '#app',

        events: {
            'keyup #edit': 'saveModel'
        },

        initialize: function() {
            var item = new app.Item();
            this.model = item;
            item.on('change', this.render, this);
            this.render();
        },

        render: function() {
            this.$input = this.$('#edit');
            this.$input.val(this.model.get('content'));
            this.$('#length').text(this.model.get('length'));
            return this;
        },

        saveModel: function() {
            this.model.save({content: this.$input.val()});
        }
    });
});
