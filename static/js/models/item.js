var app = app || {};

(function() {
    app.Item = Backbone.Model.extend({
        defaults: {
            content: '',
            length: 0
        },

        urlRoot: '/app/items'
    });
}());
