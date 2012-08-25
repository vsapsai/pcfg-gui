var app = app || {};

$(function($) {
    app.AppView = Backbone.View.extend({
        el: '#app',

        events: {
            'click #submit': 'talkToServer'
        },

        initialize: function() {
            var item = new app.Item();
            app.itemView = new app.ItemView({model: item});
            $('#item-placeholder').append(app.itemView.render().el);
        },

        talkToServer: function() {
            app.itemView.updateModel();
        }
    });
});
