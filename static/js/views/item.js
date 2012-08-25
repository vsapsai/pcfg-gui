var app = app || {};

$(function() {
    app.ItemView = Backbone.View.extend({
        template: _.template($('#item-template').html()),

        initialize: function() {
            this.model.on('change', this.render, this);
        },

        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            this.input = this.$('#edit');
            return this;
        },

        updateModel: function() {
            var value = this.input.val();
            this.model.save({content: value});
        }
    });
});
