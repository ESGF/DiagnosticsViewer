// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
        $(".alert").fadeOut(function(){
            $(this).detach();
        });
    }
});

/*
$(document).ajaxError(function(e, jqXHR) {
    console.log(jqXHR.responseJSON);
    var container = $("body > #wrap > .container");
    var error_msg = jqXHR.responseJSON.error;
    var error_div = $(document.createElement("div")).addClass("alert").addClass("alert-danger").attr("role", "alert").text(error_msg).hide();
    container.prepend(error_div);
    error_div.fadeIn();
});
*/