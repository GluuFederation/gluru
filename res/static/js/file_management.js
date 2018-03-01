//$(document).ready(function() {
//
//    if (docs == 5){
//        $('#add_new_file').closest('.form-group').hide();
//    }
//
//    if (docs >= 4){
//        $('#add_new_file').hide();
//    }
//
//
//    i = docs;
//
//    $('.delete_file').click(function(e){
//
//        if (confirm('Are you sure that you want to delete this attachment?') === true){
//
//
//            docs = docs - 1;
//
//            if (docs < 5){
//                $('#add_new_file').closest('.form-group').show();
//            }
//
//            if (docs < 4){
//                $('#add_new_file').show();
//            }
//
//            _this = $(this);
//
//            doc = _this.attr('id');
//
//            var csrf = getCookie('csrftoken');
//
//            $.ajax({
//                type: "POST",
//                url: "/ws/file/delete/"+doc,
//                data:'csrfmiddlewaretoken=' + csrf
//            }).done(function( msg ) {
//                alert(msg['msg']);
//                _this.parent().parent().remove();
//                $('#id_file').parent().parent().parent().show();
//                i--;
//            });
//        }else{
//            return false;
//        }
//    });
//
//    $('#add_new_file').click(function(){
//        if (i >= 4) {
//            return;
//        }
//
//        var additionalAttachment ='<div class="input-group gluu-attachment">'+
//            '<input class="clearablefileinput gluu-file-input" name="file'+i+'" id="id_file_'+i+'" type="file" />'+
//            '<button class="btn btn-xs btn-danger pull-right" id="btn_file_'+i+'" type="button">X</button>'+
//            '</div>';
//        $(this).parent().after(additionalAttachment);
//        i++;
//    });
//
//    // Remove attached files that have not been uploaded yet
//    $('body').on('click', 'button[id^="btn_file_"]', function(){
//        fid = $(this).attr('id').split('_')[2];
//        $('input[id="id_file_'+fid+'"]').remove();
//        $(this).remove();
//        i--;
//    });
//
//});
