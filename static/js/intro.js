$(document).ready(function() {
    
    // Click login button
    $('#login-btn').click(function(e) {
        e.preventDefault();
        $('#signup-form-wrapper').fadeOut(300);
        setTimeout(function() {
            $('#login-form-wrapper').fadeIn(300);
        }, 300);
        $('#signup-btn').removeClass('disabled').addClass('enabled');
        $(this).removeClass('enabled').addClass('disabled');
    });

    // Click signup button
    $('#signup-btn').click(function(e) {
        e.preventDefault();
        $('#login-form-wrapper').fadeOut(300);
        setTimeout(function() {
            $('#signup-form-wrapper').fadeIn(300);
        }, 300);
        $('#login-btn').removeClass('disabled').addClass('enabled');
        $(this).removeClass('enabled').addClass('disabled');
    });

    // Submit login form
    $('#login-form').submit(function(e){
        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: '/account/login/',
            data: $(this).serialize(),
            success: function(data) {
                if (data == 'Success') {
                    location.reload();
                }
                else {
                    $('#login-form .error').html(data);
                }
            },
            error: function() {
                alert('Unable to reach server. Please check your internet connection and try again.');
            }
        });
    });

    // Submit signup form
    $('#signup-form').submit(function(e){
        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: '/account/create/',
            data: $(this).serialize(),
            success: function(data) {
                if (data == 'Success') {
                    location.reload();
                }
                else {
                    $('#signup-form .error').html(data);
                }
            },
            error: function() {
                alert('Unable to reach server. Please check your internet connection and try again.');
            }
        });
    });
});