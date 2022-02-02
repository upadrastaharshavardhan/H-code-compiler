
var images = ["/static/css/images/1.jpg",
                "/static/css/images/2.jpg",
                "/static/css/images/3.jpg",
                "/static/css/images/4.jpg"
            ];

jQuery(document).ready(function() {
    $('#form-password-field').focusout(function() {
        //send password as soon as the focus is lost from password field
        //store password to django view
        var pass = $('#form-password-field').val();
        return $.ajax({
            method: 'POST',
            url: "receivePassword",
            data: {
                'pass': pass
            },
            success: function(data) {
                //this gets called when server returns an OK response
                //now remove menu item from tree
            },
            error: function(data) {
            }
        });
    });

    /*
        Fullscreen background
    */
	$.backstretch(images, {duration: 3000, fade: 1550});
	// $('#backstretch').addClass('dim');

    /*
        Form validation
    */
    $('.login-form input[type="text"], .login-form input[type="password"], .login-form textarea').on('focus', function() {
    	$(this).removeClass('input-error');
    });

    $('.login-form').on('submit', function(e) {

    	$(this).find('input[type="text"], input[type="password"], textarea').each(function(){
    		if( $(this).val() === "" ) {
    			e.preventDefault();
    			$(this).addClass('input-error');
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});

    });


});
