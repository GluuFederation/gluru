show_table = false;
cur_page = '';
docs = 0;
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
App = {
    initialise : function()
    {
        if (typeof this.initors[this.pageName] == 'function') {
            App.initors[this.pageName]();
        }
        $('body').tooltip({
            selector: '[data-toggle="tooltip"]',
            html: true,
            placement: 'top auto'
        });

        $('.icon').tooltip({
            html: true,
            placement: 'top auto',
            delay: { "show": 50, "hide": 5000 }
        });

        $( window ).scroll(function() {
            $( ".icon" ).tooltip("hide");
        });
        $(document).click(function(){
            $( ".icon" ).tooltip("hide");
        });
    },
}

/**
 *  Initors
 */
App.initors = {
    'dashboard' : function() {
        var qs = '';
        if (window.location.href.indexOf('?') != -1)
        {
            qs = '?' + window.location.href.slice(window.location.href.indexOf('?') + 1);
        }
        var table = $('#dashboardtable').DataTable({
            "serverSide": true,
            "processing": true,
            "ajax": {
                    url: '/dashboard/' + cur_page + '/' + qs,
                    type: 'POST',
                    dataType: 'json',
                    "data": function ( d ) {
                      return $.extend( {}, d, {
                        "csrfmiddlewaretoken": getCookie('csrftoken')
                      } );
                    }
                },
            "paging":   true,
            "autoWidth": true,
            "responsive": true,
            "ordering": true,
            "info":     true,
            "searching": true,
            "scrollX": false,
            "scrollY": false,
            "aaSorting" : [[0, 'desc']],
        });
        table.on('page.dt', function() {
          $("html, body").animate({ scrollTop: 0 },"fast");
          $("th:first-child").focus();
        });
        $('#dashboardtable').find('tr').on('hover', function(){
            $(this).css({'color':'#c9c9c9', 'opacity':'0.7'});
        });
        $('#check_uncheck_all').unbind().click(function(){
            var is_checked = $(this).is(':checked');
            $('.check_all_ids').each(function(){
                if (is_checked == true)
                {
                    $(this).prop('checked',true);
                }else{
                    $(this).prop('checked',false);
                }
            });
        });
        $("#id_created_date").datepicker({ dateFormat: "yy-mm-dd" });
        $('.dashboard_filer_button').on('click', function(){
            if ($(".dashboard_filter_form").is(':visible'))
            {
                $(this).html('<span class="glyphicon glyphicon-plus-sign"></span> Show advanced filters');
            } else {
                $(this).html('<span class="glyphicon glyphicon-minus-sign"></span> Hide advanced filters');
            }
            $(".dashboard_filter_form").animate({
                height: 'toggle',
                opacity: "show"
            }, 500, "linear");
        });
        $(".cstmchosen").chosen({width: "200px", max_selected_options: 1});
        $(".chosen-select").chosen({width: "200px"});
        $('#filter_reset').on('click', function(){
            $("#id_named").attr( "checked", false );
            $("#id_created_date").val("");
            $("select",'.dashboard_filter_form').each(function(){
                $(this).find('option:selected').removeAttr('selected');
                $(this).trigger("chosen:updated");
            });
        });
        $(document).on('change', '.dashboard_assign_staff', function() {
            var u_name = $(this).find("option:selected").text();
            var t = $(this).data("ticket");
            if (confirm('Staff '+ u_name +' will be assigned to ticket. Continue?') == true)
            {
                var u = $(this).val();
                var csrf = getCookie('csrftoken');
                $.ajax({
                    type: "POST",
                    url: "/ws/inline_assign/",
                    data:{'csrfmiddlewaretoken':csrf,
                            'uid':u, 'tid':t}
                }).done(function(msg) {
                    alert(msg['msg']);
                });
            }
        });
    },
    'view_ticket': function() {

        $('.copy_answer_poss').on('click', function(){
            $('.form-copy-answer').remove();
            var aid = $(this).data("pk");
            if (!window.location.origin){
              window.location.origin = window.location.protocol + "//" + (window.location.port ? ':' + window.location.port : '');
            }
            var cur_loc = window.location.origin + window.location.pathname;
            var new_input_copy = $('<input type="text" class="form-copy-answer" value="' + cur_loc + '#at' + aid + '" />');
            $(this).before(new_input_copy);
            new_input_copy.select();
        });
        $("#id_due_date").datepicker({ dateFormat: "yy-mm-dd" });
        $('#id_assigned_to').select2();
        $('#id_assigned_to_answer').select2();


        $('.inline_edit').on('click', function(e){
            var aid = $(this).data("pk");
            var csrf = getCookie('csrftoken');
            var acnt_elem = $('.inline-' + aid);
            var acnt = acnt_elem.html();
            $.ajax({
                type: "GET",
                url: "/ws/inline/get/"+aid
            }).done(function( msg ) {
                acnt_elem.html('<textarea id="inline-'+aid+'">'+msg['html']+'</textarea>');
                $('#inline-' + aid).markdown({
                        autofocus:false,
                        savable:true,
                        resize:true,
                        onCancel: function(e) {
                            e.cancelEditor();
                            acnt_elem.html(acnt);
                        },
                        onSave: function(e) {
                            if (confirm('Are you sure you want to save the changes?') == true){
                                $.ajax({
                                    type: "POST",
                                    url: "/ws/inline/edit",
                                    data: {"id":aid,
                                        "answer":e.getContent(),
                                        "csrfmiddlewaretoken":csrf
                                    }
                                }).done(function( msg ) {
                                    e.cancelEditor();
                                    acnt_elem.html(msg['html']);
                                }).fail(function() {
                                    alert(msg['msg']);
                                });
                            }else{
                               e.cancelEditor();
                               acnt_elem.html(acnt);
                            }
                        },
                });
            }).fail(function() {
                alert(msg['msg']);
            });
        });
        $('.inline_delete').on('click', function(e){
            var aid = $(this).data("pk");
            if (confirm('Are you sure that you want to delete this answer?') == true)
            {
                $('.answer-'+aid).addClass('overlay');
                $.ajax({
                    type: "GET",
                    url: "/ws/inline/delete/"+aid
                }).done(function( msg ) {
                    if ($('div[class*="answer-"]').length == 1)
                    {
                        $('.answer-'+aid).before('<div role="alert" class="alert alert-warning">No answers for this question!</div>');
                    }
                    $('.answer-'+aid).remove();
                    $('.answer-no').text(parseInt($('.answer-no').text())-1);
                }).fail(function() {
                    alert(msg['msg']);
                });
            }else{
                return false;
            }
        });

        $('#send_alerts').click(function(e){
            var tid = $(this).data("pk");
            var csrf = getCookie('csrftoken');
            $.ajax({
                type: "POST",
                url: "/ws/alerts/"+tid,
                data: "csrfmiddlewaretoken="+csrf
            }).done(function( msg ) {
                $('#send_alerts').html(msg['msg_html']);
                alert(msg['msg']);
            });
        });
    }
}

/**
 *  Initialize
 */
jQuery(document).ready(function()
{
    App.initialise();

});
