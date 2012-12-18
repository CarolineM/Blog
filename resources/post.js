//post page setup
$(function() {
	$("#id_text_tbl").css("width", "100%")
});
$(function() {
	jQuery('#delete_image').click( function () {
		$.post("/delete_image", {post_id: '{{ id }}'},
	    	function(arg)
	    	{
	    		location.reload();
	    	}
		)
	} );
	});
$(function() {
	jQuery('#post').click( function () {
		$.get("/upload", function(data) {
			$("#posttype").val("POST");
	    	$("#main_form").attr('action', data);
	    	$("#main_form").submit();
		});
	});
});
$(function() {
	jQuery('#save').click( function () {
		$.get("/upload", function(data) {
			$("#posttype").val("SAVE");
	    	$("#main_form").attr('action', data);
	    	$("#main_form").submit();
		});
	});
});
var _validFileExtensions = [".jpg", ".jpeg", ".bmp", ".gif", ".png"];

function Validate(oForm) {
    var arrInputs = oForm.getElementsByTagName("input");
    for (var i = 0; i < arrInputs.length; i++) {
        var oInput = arrInputs[i];
        if (oInput.type == "file") {
            var sFileName = oInput.value;
            if (sFileName.length > 0) {
                var blnValid = false;
                for (var j = 0; j < _validFileExtensions.length; j++) {
                    var sCurExtension = _validFileExtensions[j];
                    if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                        blnValid = true;
                        break;
                    }
                }

                if (!blnValid) {
                    alert("Sorry, " + sFileName + " is invalid, allowed extensions are: " + _validFileExtensions.join(", "));
                    return false;
                }
            }
        }
    }

    return true;
}

$(function() {
	$("#datepicker").datepicker("setDate", new Date());
});