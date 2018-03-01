$(document).ready(function(){
    $('#bottom-link-block').removeClass('hidden');
    $(document).delegate( ".info-icon", "click", function() {
        copyToClipboard($(this).parent().parent().siblings("span.copy-email"));
    });
    function copyToClipboard(element) {
      var $temp = $("<input>");
      $("body").append($temp);
      $temp.val($(element).text()).select();
      document.execCommand("copy");
      $temp.remove();
    }

    $('#submit-id-submit').click(function(){
        $('#id_close_ticket').attr('checked', true);

    });

    $('#submit-id-save').click(function(){
        $('#id_close_ticket').attr('checked', false);
    });

    var values_array=[];
    var uploaded_value_array=[];
    var image_src_array = [];
    var uploaded_src_array=[];
    setInterval(function(){
     $(".qq-upload-file").each(function(){
        filename= $(this).html();
        if ($(this).parent().hasClass("uploaded")){
            if($.inArray(filename, uploaded_value_array) == -1){
                uploaded_value_array.push(filename);
            }
        }
        else if($.inArray(filename, values_array) == -1){
            values_array.push(filename);
        }
        console.log("uploaded array: "+uploaded_value_array);
        console.log("array: "+ values_array);
     });
     $(".qq-thumbnail-selector").each(function(){
        image_src=$(this).attr('src');
        if ($(this).parent().hasClass("uploaded")){
            if($.inArray(image_src, uploaded_src_array) == -1){
                uploaded_src_array.push(image_src);
            }
        }
        else if($.inArray(image_src, image_src_array) == -1){
            image_src_array.push(image_src);
        }
        console.log(uploaded_src_array);
        console.log(image_src_array);
     });

     }, 2000);
     setInterval(function(){
        if($(".qq-upload-list-selector li").length >= 1){
            $(".qq-upload-list-selector").removeClass("qq-hide");
        }else{
            $(".qq-upload-list-selector").addClass("qq-hide");
        }
        var value=$(".qq-uploader-selector").attr("qq-drop-area-text");
        console.log(value);
        if(value !== undefined){
            $(".qq-uploader-selector").addClass("border-class");
        }else{
            $(".qq-uploader-selector").removeClass("border-class");
        }
     },100);

    $('body').delegate(".qq-upload-cancel","click",function(){
        var name=$(this).parent().parent().find(".qq-upload-file").html();
        var src = $(this).parent().parent().find(".qq-thumbnail-selector").attr('src');
        $(this).parent().parent().remove();
        values_array.splice($.inArray(name, values_array),1);
        uploaded_value_array.splice($.inArray(name, uploaded_value_array),1);
        image_src_array.splice($.inArray(src, image_src_array),1);
        uploaded_src_array.splice($.inArray(src, uploaded_src_array),1);
        if($(".qq-upload-file").length == 0){
            $(".qq-uploader-selector").attr("qq-drop-area-text", "Drop Files Here");
            $(".qq-uploader-selector").addClass("border-class");
        }
        console.log(values_array);
        console.log(uploaded_value_array);

    });

    $("form").submit(function(){
        var arr_len = values_array.length;
        if(arr_len > 0){
            for(var x = 0; x < arr_len; x++){
            var value =values_array[x].split(' ').join('_')
                $('.answer_form').append('<input type="hidden" name="file_field" value='+value+'>');
                $('.answer_form').append('<input type="hidden" name ="file_src" value='+image_src_array[x]+'>');
            }
        }
        var ar_len= uploaded_value_array.length;
        if(ar_len > 0){
            for(var z=0; z< ar_len; z++){
                $('.answer_form').append('<input type="hidden" name="uploaded_files" value='+uploaded_value_array[z]+'>');
            }
        }else if(ar_len==0){
            $('.answer_form').append('<input type="hidden" name="uploaded_files" value="">');
        }
    });

});

$("#div_id_link_url").addClass("col-md-6");
$("#div_id_send_copy").addClass("col-md-6");

$('body').delegate("#ticket_edit_delete","click",function(e){
       $(this).parent().find(".function-list").toggle();
       e.stopPropagation();
});

$('body').delegate(".edit_delete_answer","click",function(e){
    $(this).parent().find(".function-list").toggle();
    e.stopPropagation();
});

$(document).click(function(){
    $(".function-list").hide();

});



$(".remove_file").click(function(){
   var id = $(this).attr("data-id");
   var csrf = getCookie('csrftoken');
   var ref = $(this)
   swal({
      title: "Are you sure?",
      text: "Delete this file.",
      icon: "warning",
      buttons: true,
      dangerMode: true,
   })
   .then((willDelete) => {
      if (willDelete) {
      $.ajax({
        type: "GET",
        url: "/ws/file/delete/"+ id ,
        data:{'csrfmiddlewaretoken':csrf}
           }).done(function(response){
               ref.parent().remove();

        });
        swal("File successfully deleted", {
          icon: "success",
        });
      } else {
        swal("File not removed");
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
