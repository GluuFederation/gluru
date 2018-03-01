(function($) {
setTimeout(function(){ $(".activate_ticket").on("click",function(){
        alert("Are you sure you want to activate this ticket!");
        var id = $(this).attr("data-id");
        var csrf = getCookie('csrftoken');
        var action = "activate_ticket";
        var data = {"id":id, "action":action, "csrfmiddlewaretoken":csrf};
        $.ajax({
            type:"POST",
            url:"/tickets/activate/"+id+"/",
            data: data,
            success: function(data){
                location.reload();
            }

        })

    });
    },2000);

    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
})(grp.jQuery);
