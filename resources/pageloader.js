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

//for mobile
$(function() {
	if(jQuery.browser.mobile) {
		var menu = document.getElementsByClassName('hitem');
		for(var i=0; i<menu.length; i++) {
			menu[i].style.background = 'black';
		}
		
		element = document.getElementById("pmarg");
		element.style.width = '100%';
		element.style.margin = '0 auto';
	}
});
