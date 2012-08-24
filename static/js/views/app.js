var app = app || {};

$(function($) {
	app.AppView = Backbone.View.extend({
		el: '#app',

		events: {
			'click #submit': 'talkToServer'
		},

		talkToServer: function() {
			var item = new app.Item();
			item.save();
		}
	});
});
