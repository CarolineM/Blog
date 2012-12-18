$('.dropdown-toggle').dropdown();

$(function() {

	// Datepicker
	$('#datepicker').datepicker({
		inline : true
	});

	// hover states on the static widgets
	$('#dialog_link, ul#icons li').hover(function() {
		$(this).addClass('ui-state-hover');
	}, function() {
		$(this).removeClass('ui-state-hover');
	});

});

$(function() {
	$("input, textarea, select, button").uniform();
});
