$('#likes').on('click', function(event){
    event.preventDefault();
    var element = $(this);

    $.ajax({
        url : '/set_like/',
        type : 'POST',
        data : { key : $(this).attr("data-key")},

        success : function(data){
            data = data > 0 ? data : '';
            element.html('<i class="fa fa-heart fa-2x"></i> ' + data);
        }
    });
});

$('#remove-pic').on('click', function(){

    var confirmation = confirm("Вы действительно хотите удалить изображение?");

    if (confirmation) {
        $.ajax({
            url : '/del_image/',
            type : 'POST',
            data : { key : $(this).attr("data-key")},

            success : function(data){
                alert('Изображение удалено');
                window.location.replace("/");
            },
            error : function (data) {
                alert('Удаление не удалось');
                window.location.reload();
            }
        });
    }
});

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
    }
});