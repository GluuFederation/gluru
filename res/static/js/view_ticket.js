$(document).ready(function(){
    $(this).scrollTop(0);
    $('#bottom-link-block').removeClass('hidden');
    $(document).delegate( ".info-icon", "click", function() {
        copyToClipboard($(this).parent().parent().siblings("span.copy-email"));
    });

    markdownToHtml();
    function copyToClipboard(element) {
      var $temp = $("<input>");
      $("body").append($temp);
      $temp.val($(element).text()).select();
      document.execCommand("copy");
      $temp.remove();
    }
	if($('#id_privacy').attr('disabled')){
        $(".answer_form").append('<input type="hidden" name="privacy" value="inherit">');
    }

    function markdownToHtml(){
        var ticket_description = $(".ticket-description").html();
        console.log(ticket_description);
        var result =  $.trim(ticket_description);
        result = result.replace(/\&gt;/g,">");
        result = result.replace(/\&lt;/g,"<");
        result = result.replace(/\&amp;/g,"&");
        $(".marked-description").html(marked(result));
        $(".answer-description").each(function(){
            var description = $(this).html();
            description = description.replace(/\&lt;/g,"<");
            description = description.replace(/\&gt;/g,">");
            description = description.replace(/\&amp;/g,"&");
            $(this).html(marked(description));
        });

    }
    simplemde.codemirror.on("keyup", function(cm, e){
        var x = e.keyCode;
        var y = e.shiftKey;
        if (x == 50 && y == true){
            $.ajax({
                type: "GET",
                url: "/ws/autocomplete-users/",
                data: {
                    'csrfmiddlewaretoken' : getCookie('csrftoken')
                }
            }).done(function (response){
                swal({
                    title: 'Tag A Staff Member',
                    type: 'question',
                    input: 'select',
                    inputOptions:response.suggestions,
                    inputPlaceholder: 'Staff Members',
                    showCancelButton: true,
                    inputValidator: function (value) {
                        return new Promise(function (resolve, reject) {
                            if (value !== '') {
                                resolve();
                            } else {
                                reject('You need to select a staff member');
                            }
                        });
                    }
                }).then(function (result) {
                    var name = result.split(",");
                    var description = simplemde.value();
                    simplemde.value(description+name[1].replace(' ','.'));


                });

            });

        }
    });


});

$(window).scroll(function() {
    if ( $(window).scrollTop() > 300 ) {
        $('#top-link-block').removeClass('hidden');
    } else {
        $('#top-link-block').addClass('hidden');
    }
});

$(window).scroll(function() {
    if ( $(window).scrollTop() < 300 ) {
        $('#bottom-link-block').removeClass('hidden');
    } else {
        $('#bottom-link-block').addClass('hidden');
    }
});

$('#top-link-block').on('click', function(){
    $("html, body").animate({scrollTop:0}, 1000);
});

$('#bottom-link-block').on('click', function(){
    $("html, body").animate({scrollTop:$('#last-answer-anchor').offset().top - 150}, 1000);
});

$("#submit-id-close").on('click',function(e){
    if($(this).val()== "Close")
    {
        e.preventDefault();
        if (confirm('Are you sure that you want to close this ticket?') == true)
        {
            window.location.href = $(".close_ticket").attr("href");
            return true;
        }
        else
        {
            return false;
        }
    }else
    {
        $('#id_close_ticket').attr('checked', true);
    }
});
$('#submit-id-save').click(function(){
    $('#id_close_ticket').attr('checked', false);
});
$("#id_answer").keyup(function(){
    $("#submit-id-close").val("Post & Close");
    if($(this).val().length <= 0)
    {
        $("#submit-id-close").val("Close");
    }
});
