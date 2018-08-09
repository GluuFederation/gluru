
// Helper FUnction For Issue Type Dynamic Logic
var availableCategoriesForIssue = {
    'outage': ['Outages',],
    'impaired': ['Outages', 'Maintenance', 'Identity Management', 'Single Sign-On', 'Authentication', 'Access Management', 'Upgrade','Log Out' ,'Other'],
    'pre_production': ['Outages', 'Maintenance', 'Customization', 'Feature Request', 'Identity Management', 'Single Sign-On', 'Authentication', 'Access Management', 'Installation', 'Upgrade','Log Out', 'Other'],
    'minor': ['Maintenance', 'Customization', 'Feature Request', 'Identity Management', 'Single Sign-On', 'Authentication', 'Access Management', 'Installation', 'Upgrade', 'Log Out','Other'],
    'new_development': ['Customization', 'Feature Request', 'Identity Management', 'Single Sign-On', 'Authentication', 'Access Management', 'Installation', 'Upgrade', 'Log Out', 'Other'],
};
var availableProductVersion = {
//    'GLUU':['3.0.2','3.0.1','2.4.4.3','2.4.4.2','2.4.4','2.4.3','2.4.2','Other'],
    'Oxd':['3.1.4','3.1.3','3.1.2','3.0.2','3.0.1'],
    'Super Gluu':['3.1.4','3.1.3','3.1.1'],
    'Cluster':['3.1.4','3.1.3','Alpha'],
    'Cred Manager':['3.1.4','3.1.3','3.1.2']
}

var availableOS = {
//    'GLUU':['Ubuntu','CentOS','RHEL','Debian'],
    'Oxd':['Ubuntu','CentOS','RHEL','Debian'],
    'Super Gluu':['Android','iOS','Both'],
    'Cluster':['Ubuntu','CentOS','RHEL','Debian'],
}

// Helper FUnction For Issue Type Dynamic Logic
function contains(a, obj) {
    for (var i = 0; i < a.length; i++) {
        if (a[i] === obj) {
            return true;
        }
    }
    return false;
}

// Helper Function For Issue Type Dynamic Logic
function gatherAllCategories(){
    allCategories = {};
    $('#id_ticket_category option').each(function(){
        allCategories[$(this).text().trim()] = $(this).val();
    });
    return allCategories;
}

function gatherAllProductVersion(){
    allProductVersions = {};
    $('#id_product_version option').each(function(){
        allProductVersions[$(this).text().trim()] = $(this).val();
    });
    return allProductVersions;
}

function gatherAllOS(){
    allOS ={};
    $('#id_product_os_version option').each(function(){
        allOS[$(this).text().trim()]=$(this).val();
    });
    return allOS;
}
// Helper Function For Creating Ticket on Behalf of Someone
function populateCompanyMembers(){
    var csrf = getCookie('csrftoken');
    var company_id = $('#id_company').find('option:selected').val();

    $.ajax({
        type: "GET",
        url: "/ws/inline/company/"+ company_id +"/",
        data:{'csrfmiddlewaretoken':csrf}
    }).done(function(response){
        users = response['users'];
        $('#id_created_for').find('option').remove();
        $('#id_created_for').append($('<option>', {
            value: 'N/A',
            text: 'Select a user in that company',
            selected: 'selected'
        }));
        for (var key in users){
            $('#id_created_for').append($('<option>', {
                value: key,
                text: users[key]
            }));
        }
    });
}

var ajaxRequest = null;

function populateTicketTitles(){
    var csrf=getCookie('csrftoken');
    var ticket_title = $('#id_title').val();
    var query_title = ticket_title.split(' ').join('+');

//    ajaxRequest.abort();
    ajaxRequest = $.ajax({
        type: "GET",
        url: "/ws/inline/ticket_title/",
        data: {
            'q' : ticket_title
        },
        beforeSend : function()    {
            if(ajaxRequest != null) {
                ajaxRequest.abort();
            }
        },
    }).done(function (response){
        $(".answers > ul").empty();
        $('#view_more_tickets').addClass("hidden");
        if (response.title.length > 0){
            for(i = 0; i < response.link.length; i++){
                $(".answers > ul").append("<li><a  href='"+response.link[i]+"' target='_blank'><span class='title' style='border-bottom:none;'>"+response.title[i]+"</span></a></li>");
                if (i == 9){
                    break;
                }
            }
            if (response.title.length > 5){
                $('#view_more_tickets').removeClass("hidden");
                $('#view_more_tickets').attr("href","../../search/?q="+query_title+"&category=");
            }else{
                $('#view_more_tickets').addClass("hidden");
            }

        }else{
            $(".answers > ul").append("<li><span>No relevant ticket found.</span></li>");
            $('#view_more_tickets').addClass("hidden");
        }

    });

}
function set_default_gluu_values(id){
    var csrf=getCookie('csrftoken');
    console.log(id);
    var user_id = id;
    $.ajax({
        type: "POST",
        url: "/ws/inline/gluu_default_values/",
        data : {'csrfmiddlewaretoken':csrf,"user_id":user_id}
    }).done(function(response){
       if (response.data[0]){
          if (response.data[0] == "Other"){
            $('#id_gluu_server_version').select2("val",response.data[0]);
            $('#id_os_version').select2("val",response.data[1]);
            $("#id_os_version_name").val(response.data[2]);
            $('#div_id_gluu_server_version_comments').removeClass('hidden');
            $('#div_id_gluu_server_version').removeClass("col-md-4");
            $('#div_id_gluu_server_version').addClass("col-md-3");
            $('#div_id_os_version').removeClass("col-md-4");
            $('#div_id_os_version').addClass("col-md-3");
            $('#div_id_os_version_name').removeClass("col-md-4");
            $('#div_id_os_version_name').addClass("col-md-3");
            $("#id_gluu_server_version_comments").val(response.data[3]);
          }else{
                $('#id_gluu_server_version').select2("val",response.data[0]);
                $('#id_os_version').select2("val",response.data[1]);
                $("#id_os_version_name").val(response.data[2]);
                $('#div_id_gluu_server_version_comments').addClass('hidden');
                $('#div_id_gluu_server_version').addClass("col-md-4");
                $('#div_id_gluu_server_version').removeClass("col-md-3");
                $('#div_id_os_version').addClass("col-md-4");
                $('#div_id_os_version').removeClass("col-md-3");
                $('#div_id_os_version_name').addClass("col-md-4");
                $('#div_id_os_version_name').removeClass("col-md-3");
          }
       }

    });
}

function populateTicketAttachments(id){
    var csrf=getCookie('csrftoken');
    var ticket_id = id;
    $.ajax({
        type: "POST",
        url: "/ws/inline/ticket_attachments/",
        data:{'csrfmiddlewaretoken':csrf, "ticket_id":ticket_id}
    }).done(function (response){
        $(".qq-uploader-selector").removeAttr("qq-drop-area-text");
        $(".qq-uploader-selector").removeClass("border-class");
        if(response.file_name.length>0){
            for(var z=0; z < response.file_name.length; z++){
                $(".qq-upload-list").append("<li class='qq-id-"+z+" qq-upload-success uploaded' qq-id='"+z+"'>"+
                "<div class='qq-progress-bar-container-selector qq-hide'> <div role='progressbar' aria-valuenow='100' aria-valuemin='0' aria-valuemax='100' class='qq-progress-bar-selector qq-progress-bar' style='width: 100%;'></div></div>"+
                "<span class='qq-upload-spinner-selector qq-upload-spinner qq-hide'></span>"+
                "<img class='qq-thumbnail-selector' name='image_src' qq-max-size='100' qq-server-scale='' src='"+response.file_src[z]+"'>"+
                "<span class='qq-upload-file-selector qq-upload-file' title='"+response.file_name[z]+"'>"+response.file_name[z]+"</span>"+
                "<span class='qq-edit-filename-icon-selector qq-edit-filename-icon' aria-label='Edit filename'></span>"+
                "<input class='qq-edit-filename-selector qq-edit-filename' tabindex='0' type='text'>"+
                "<div class='qq-hide qq-cancel'><button type='button' class='qq-btn  qq-upload-cancel'></button></div>"+
                "<button type='button' class='qq-btn qq-upload-retry-selector qq-upload-retry qq-hide'>Retry</button>"+
                "<span role='status' class='qq-upload-status-text-selector qq-upload-status-text'></span></li>");

            }

        }

    });
}

$(document).ready(function() {
    var check = 1;
    $('.has-popover').popover({'trigger':'hover'});
    // Add Style to Dropdowns and Markdown Field
    $('#id_description').markdown({});
    $('#id_assigned_to').select2();
    if($("#div_id_company").is(":visible")){
        $('#id_company').select2();
    }
    $('#id_created_for').select2();
    $('#id_gluu_server_version').select2();
    $('#id_os_version').select2();
    $('.product').select2();
    $('.product_version').select2();
    $('.product_os_version').select2();
    $('#id_issue_type').select2();
    $('#id_ticket_category').select2();
    $('#id_status').select2();

    if ($("#id_gluu_server_version").val()=="Other"){
            $('#div_id_gluu_server_version_comments').removeClass('hidden');
            $('#div_id_gluu_server_version').removeClass("col-md-4");
            $('#div_id_gluu_server_version').addClass("col-md-3");
            $('#div_id_os_version').removeClass("col-md-4");
            $('#div_id_os_version').addClass("col-md-3");
            $('#div_id_os_version_name').removeClass("col-md-4");
            $('#div_id_os_version_name').addClass("col-md-3");
        }

    if(window.location.href.indexOf("add") > -1 || window.location.href.indexOf("edit") > -1) {
       $('body').addClass('form-section-page');
    }
    if(window.location.href.indexOf("edit") > -1) {
//        $( ".product_layout_div" ).wrapAll( "<div class='main_product_div'></div>" );
        
        $('#div_id_set_default_gluu').removeClass('hidden');
        $('.add-product').removeClass('hidden');

        if ($("#id_gluu_server_version").val()=="Other"){
            $('#div_id_gluu_server_version_comments').removeClass('hidden');
            $('#div_id_gluu_server_version').removeClass("col-md-4");
            $('#div_id_gluu_server_version').addClass("col-md-3");
            $('#div_id_os_version').removeClass("col-md-4");
            $('#div_id_os_version').addClass("col-md-3");
            $('#div_id_os_version_name').removeClass("col-md-4");
            $('#div_id_os_version_name').addClass("col-md-3");
        }

        var id= $("#ticket-id").val();
        populateTicketAttachments(id);

        var a = $('.product_layout_div').length;

        if(a >= 2){
           $('.product_layout_div').each(function(){
                if(!$(this).children().find('#id_product option').filter(":selected").val()){
                    $(this).remove();
                }
           });
        }

    }
    $('.div_set_default').parent().parent().parent().addClass('col-md-6');
    $('#div_id_is_private').addClass('col-md-6');
    $('#div_id_send_copy').addClass('col-md-6');
    $('#div_id_os_type').parent().addClass('col-md-6');
    $('#div_id_ram').parent().addClass('col-md-6');
    $('#div_id_attachment').addClass('col-md-10');
    $('.os_version_icon > label').append("<span class='glyphicon glyphicon-info-sign' data-toggle='tooltip' title= 'Enter the OS version number that you are using. e.g. 1.2'></span>");
    $('#div_id_is_private > label').append("<span class='glyphicon glyphicon-info-sign' data-toggle='tooltip' title= 'Mark your ticket as private / public'></span>");
    $('#div_id_send_copy > label').append("<span class='glyphicon glyphicon-info-sign' data-toggle='tooltip' title= 'Send a copy of this ticket to colleagues'></span>");
    $('#div_id_set_default > label').append("<span class='glyphicon glyphicon-info-sign' data-toggle='tooltip' title= 'This is static text.'></span>");
    $('.add_product_btn').attr("data-toggle","tooltip");
    $('.add_product_btn').attr("title","Add gluu associated products which you are using");
    // Dynamic Logic For Fields "Issue Type" and "Category"
    allCategories = gatherAllCategories();
    allProductVersions = gatherAllProductVersion();
    allOS = gatherAllOS();
    $('#id_description').keyup(function(){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        var shift = event.shiftKey;
        if(keycode == '50' && shift == true){
            alert("Don't Press Shift+2");
            $(this).append("<ul><li>Appended item</li></ul>");
        }
    });
    $(".add_product_btn").click(function(){
        $(".main_product_div").removeClass("hidden");
        if (check == 1){
            $("#div_id_product").removeClass("hidden");
            $(".delete_product_row").removeClass("hidden")
        }
        if(check > 1){
            var c = $(this).parent().parent().parent().parent().find(".product_layout_div").length;
            if (c == 1) {
                $(this).addClass("hidden");

            }
            var first = $(this).parent().parent().parent().parent().find(".product_layout_div").first();
            var last = $(this).parent().parent().parent().parent().find(".product_layout_div").last();
//            if(!first.find("#div_id_product_os_version_name").hasClass("col-md-2")){
//                first.find("#div_id_product_os_version_name").removeClass("col-md-3").addClass("col-md-2");
//            }
            var clone = first.clone();
            clone.find(".help-block").remove();
            clone.find("#id_product").children().removeAttr("selected");
            clone.find("#id_product_version").children().removeAttr("selected");
            clone.find("#id_product_os_version").children().removeAttr("selected");
            clone.find(".select2-container").remove();
            clone.find(".product").select2();
            clone.find(".product_version").select2();
            clone.find(".product_os_version").select2();
            clone.find(".select2-container").show();
            clone.find("#div_id_product").removeClass("has-error");
            clone.find("#div_id_product_version").removeClass("has-error");
            clone.find("#div_id_product_os_version").removeClass("has-error");
            clone.find("#div_id_product_os_version_name").removeClass("has-error");
            clone.find("#div_id_ios_version_name").removeClass("has-error");
//            clone.find("#div_id_product_version").addClass("hidden");
//            clone.find("#div_id_product_os_version").addClass("hidden");
//            clone.find("#div_id_product_os_version_name").addClass("hidden");
//            clone.find("#div_id_ios_version_name").addClass("hidden");
            clone.find("#div_id_product_version").removeClass("col-md-2");
            clone.find("#div_id_product_version").addClass("col-md-3");
            clone.find("#div_id_product_os_version").removeClass("col-md-2");
            clone.find("#div_id_product_os_version").addClass("col-md-3");
            clone.find("#div_id_product_os_version_name > label").html("OS Version <span class='glyphicon glyphicon-info-sign' data-toggle='tooltip' title='' data-original-title='Enter the OS version number that you are using. e.g. 1.2'></span>");
            clone.find("#id_product_os_version_name").val("");
            clone.find("#div_id_ios_version_name").addClass("hidden");
//            clone.find("#id_product_version").attr("disabled","disabled");
//            clone.find("#id_product_os_version").attr("disabled","disabled");
            last.after(clone);
            c++;
        }
        check++;
    });

    $('body').delegate(".delete_product_row", "click",function(){

        if($(".product_layout_div").length == 1){
            $(".main_product_div").addClass("hidden");
//            $(this).parent().parent().find("#div_id_product").addClass("hidden");
//            $(this).parent().parent().find("#div_id_product_version").addClass("hidden");
            $(this).parent().parent().find("#div_id_product_version").removeClass("col-md-2");
            $(this).parent().parent().find("#div_id_product_version").addClass("col-md-3");
//            $(this).parent().parent().find("#div_id_product_os_version").addClass("hidden");
            $(this).parent().parent().find("#div_id_product_os_version").removeClass("col-md-2");
            $(this).parent().parent().find("#div_id_product_os_version").addClass("col-md-3");
            $(this).parent().parent().find("#div_id_product_os_version_name > label").html("OS Version <span class='glyphicon glyphicon-info-sign' data-toggle='tooltip' title='' data-original-title='Enter the OS version number that you are using. e.g. 1.2'></span>");
//            $(this).parent().parent().find("#div_id_product_os_version_name").addClass("hidden");
            $(this).parent().parent().find("#div_id_ios_version_name").addClass("hidden");
            $(".product").select2("val","");
            $(".product_version").select2("val","");
            $(".product_os_version").select2("val","");
            $("#id_product").children().removeAttr("selected");
            $("#id_product_version").children().removeAttr("selected");
            $("#id_product_os_version").children().removeAttr("selected");
            $("#id_product_os_version_name").val("");
            $("#id_ios_version_name").val("");
            $("#div_id_set_default_product").addClass("hidden");
            $(this).addClass("hidden");

            check=1;
        }
        if($(".product_layout_div").length == 2){
            $(this).parent().parent().remove();
        }
        if($(".product_layout_div").length < 2){
            $(".add_product_btn").removeClass("hidden");
        }

    });

    $('#id_issue_type').change(function(){

        selectedIssueValue = $(this).find('option:selected').val();
		$("#id_ticket_category").select2("val","");
        if (selectedIssueValue == 'outage'){
            $('#div_id_ticket_category').addClass('hidden');
            if(selectedIssueValue == 'outage'){
                $("#id_ticket_category option[value='"+allCategories['Outages']+"']").prop('selected', true);
            }
        }else{

            $('#div_id_ticket_category').removeClass('hidden');
            allowedCategories = availableCategoriesForIssue[selectedIssueValue];

            if (allowedCategories !== undefined){

                $('#id_ticket_category').find('option').remove();
                $('#id_ticket_category').append($('<option>', {
                    value: '',
                    text: 'Choose a category',
                    selected: 'selected'
                }));
                for (var key in allCategories){
                    if (contains(allowedCategories, key)){
                        $('#id_ticket_category').append($('<option>', {
                            value: allCategories[key],
                            text: key
                        }));
                    }
                }
            }
        }
    });

    $('body').delegate("#id_product", "change",function(){
        var ref = $(this).parent().parent().parent();
        selectedProduct = ref.find('option:selected').val();
        allowedProductVersion = availableProductVersion[selectedProduct];
        if(selectedProduct != ""){
            ref.find('#div_id_product_version').removeClass('hidden');
            if(allowedProductVersion !== undefined){
                ref.find('#id_product_version').find('option').remove();
                ref.find('#id_product_version').append($('<option>',{
                    value:'',
                    text: 'Select Product Version',
                    selected: 'selected'
                }));
                for (var key in allProductVersions){
                    if(contains(allowedProductVersion,key)){
                        ref.find('#id_product_version').append($('<option>',{
                            value: allProductVersions[key],
                            text:key
                        }));

                    }
                }
            }
        }
//        else{
//            ref.find('#div_id_product_version').addClass('hidden');
//            ref.find('#div_id_product_os_version_name').addClass('hidden');
//
//        }

    });
    $('body').delegate("#id_product", "change",function(){
        var refer = $(this).parent().parent().parent();
        selectedProduct = refer.find('option:selected').val();
        allowedOS = availableOS[selectedProduct];
        refer.find("#div_id_ios_version_name").addClass("hidden");
        refer.find("#div_id_product_os_version").addClass("col-md-3");
        refer.find("#div_id_product_os_version").removeClass("col-md-2");
        refer.find("#div_id_product_version").addClass("col-md-3");
        refer.find("#div_id_product_version").removeClass("col-md-2");
        refer.find("#div_id_product_os_version_name").removeAttr("style");
        refer.find("#id_product_os_version_name").val("");
        refer.find("#div_id_product_os_version_name > label").html("OS Version <span class='glyphicon glyphicon-info-sign' data-toggle='tooltip' title='' data-original-title='Enter the OS version number that you are using. e.g. 1.2'></span>");
        refer.find("#div_id_ios_version_name").removeAttr("style");
        refer.find("#id_ios_version_name").val("");
        if(selectedProduct != ""){

            if(allowedOS !== undefined){
                refer.find('#id_product_os_version').find('option').remove();
                refer.find('#id_product_os_version').append($('<option>',{
                    value:'',
                    text: 'Select Operating System',
                    selected: 'selected'
                }));

                for (var key in allOS){
                    if(contains(allowedOS,key)){
                        refer.find('#id_product_os_version').append($('<option>',{
                            value: allOS[key],
                            text:key
                        }));

                    }
                }
            }
        }
//        else{
//
//        }

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
     });

     }, 2000);
     setInterval(function(){
        if($(".qq-upload-list-selector li").length >= 1){
            $(".qq-upload-list-selector").removeClass("qq-hide");
        }else{
            $(".qq-upload-list-selector").addClass("qq-hide");
        }
        var value=$(".qq-uploader-selector").attr("qq-drop-area-text");
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

    });

    $('body').delegate("#id_product_version", "change",function(){
        var refer = $(this).parent().parent().parent();
        selectedProduct = refer.find('#id_product_version').val();
        if(selectedProduct != ""){
           refer.find('#div_id_product_os_version').removeClass('hidden');
        }
//        else{
//            refer.find('#div_id_product_os_version').addClass('hidden');
//        }
    });
    $('body').delegate("#id_product_os_version", "change",function(){
        var refer = $(this).parent().parent().parent();
        selectedProduct = refer.find('#id_product_os_version').val();
        if(selectedProduct != ""){
           refer.find('#div_id_product_os_version_name').removeClass('hidden');
           refer.find('#id_product_os_version_name').val("");
           if(selectedProduct == "Both"){
             refer.find("#div_id_product_os_version").removeClass("col-md-3");
             refer.find("#div_id_product_os_version").addClass("col-md-2");
             refer.find("#div_id_product_version").removeClass("col-md-3");
             refer.find("#div_id_product_version").addClass("col-md-2");
             refer.find("#div_id_ios_version_name").removeClass("hidden");
             refer.find("#div_id_product_os_version_name").attr("style","width:128px;");
             refer.find("#div_id_product_os_version_name > label").html("Android Version <span class='glyphicon glyphicon-info-sign' data-toggle='tooltip' title='' data-original-title='Enter the OS version number that you are using. e.g. 1.2'></span>");
             refer.find("#div_id_ios_version_name").attr("style","width:100px;");
           }else{
             refer.find("#div_id_ios_version_name").addClass("hidden");
             refer.find("#div_id_product_os_version").addClass("col-md-3");
             refer.find("#div_id_product_os_version").removeClass("col-md-2");
             refer.find("#div_id_product_version").addClass("col-md-3");
             refer.find("#div_id_product_version").removeClass("col-md-2");
             refer.find("#div_id_product_os_version_name").removeAttr("style");
             refer.find("#div_id_product_os_version_name > label").html("OS Version <span class='glyphicon glyphicon-info-sign' data-toggle='tooltip' title='' data-original-title='Enter the OS version number that you are using. e.g. 1.2'></span>");
             refer.find("#div_id_ios_version_name").removeAttr("style");
           }
        }
//        else{
//            refer.find('#div_id_product_os_version_name').addClass('hidden');
//
//        }
    });
    // Dynamic Logic For "Other" Gluu Server Version
    $('body').delegate('#id_created_for',"change",function(){
        var user_id = $('#id_created_for').find('option:selected').val();
        if (user_id != "N/A"){
           set_default_gluu_values(user_id);
        }
    });


    if ($('#id_gluu_server_version').find('option:selected').val() == 'Other'){
        $('#div_id_gluu_server_version_comments').removeClass('hidden');
    }

    $('#id_gluu_server_version').change(function(){
        if ($(this).find('option:selected').val() == 'Other'){
            $('#div_id_gluu_server_version_comments').removeClass('hidden');
            $('#id_gluu_server_version_comments').attr('placeholder', 'Which Gluu Server version are you using?');
            $('#div_id_gluu_server_version').removeClass("col-md-4");
            $('#div_id_gluu_server_version').addClass("col-md-3");
            $('#div_id_os_version').removeClass("col-md-4");
            $('#div_id_os_version').addClass("col-md-3");
            $('#div_id_os_version_name').removeClass("col-md-4");
            $('#div_id_os_version_name').addClass("col-md-3");
        }
        else{
            $('#div_id_gluu_server_version').removeClass("col-md-3");
            $('#div_id_gluu_server_version').addClass("col-md-4");
            $('#div_id_os_version').removeClass("col-md-3");
            $('#div_id_os_version').addClass("col-md-4");
            $('#div_id_os_version_name').removeClass("col-md-3");
            $('#div_id_os_version_name').addClass("col-md-4");
            $('#div_id_gluu_server_version_comments').addClass('hidden');
            $("#id_gluu_server_version_comments").val("");
        }

    });
    $('#id_title').keyup(function(){
        if ($(this).val().length > 2){
            populateTicketTitles();
        }else{
            $(".answers > ul").empty();
            $("#view_more_tickets").addClass("hidden");
            $(".answers > ul").append("<li><span>Enter a title to check relevant tickets</span></li>");
        }

    });
    // Dynamic Logic For "Other" OS Version for live
    if (
        typeof $('#id_os_version').find('option:selected').val().length !== "undefiend" &&
        $('#id_os_version').find('option:selected').val().length
    ){
        $('#div_id_os_version_name').removeClass('hidden');
    }

    $('#id_os_version').change(function(){
        if (
            typeof $(this).find('option:selected').val().length !== 'undefined' &&
            $(this).find('option:selected').val().length
        ){
            $('#div_id_os_version_name').removeClass('hidden');
            $('#id_os_version_name').attr('placeholder', 'Which OS are you using?');
        }
        else{
            $('#div_id_os_version_name').addClass('hidden');
        }
    });


    // Dynamic Logic For "Other" OS Version

    if ($('#id_os_version').find('option:selected').val() == 'Other'){
        $('#div_id_os_version_comments').removeClass('hidden');
    }

    $('#id_gluu_server_version').change(function(){

        if ($(this).find('option:selected').val() != ''){
            $('#div_id_os_version').removeClass('hidden');
        }
        else{
//            $('#div_id_os_version').addClass('hidden');
            $('#id_os_version').children().removeAttr('selected');
//            $('#div_id_os_version_name').addClass('hidden');
            $('#id_os_version_name').val("");
        }

    });

    $('#id_os_version').change(function(){

        if ($(this).find('option:selected').val() != ''){
            $('#div_id_os_version_name').removeClass('hidden');
            $('#id_os_version_name').val("");
        }
//        else{
//            $('#div_id_os_version_name').addClass('hidden');
//        }

    });

    $('#id_os_version_name').keyup(function(){
        if($("#id_os_version_name").val() != ''){
            $('.default_product_div').removeClass('hidden');
            $('#div_id_set_default_gluu').removeClass('hidden');
            $('.add-product').removeClass('hidden');
        }
//        else{
//            $('.default_product_div').addClass('hidden');
//            $('#div_id_set_default_gluu').addClass('hidden');
//            $('.add-product').addClass('hidden');
//        }
    });



    // Dynamic Logic For Cancel Modal

    $("form :input").change(function() {
        $('#cancelButton').attr('data-target', '#cancelModal');
        $('#cancelButton').attr('data-toggle', 'modal');
        $('#cancelButton').attr('href', '');
    });

    var eTop = $('#id_title').offset().top; //get the offset top of the element
    var nav_height = $(".navbar-fixed-top").height();
    var breadcrumb_height = $(".breadcrumb").height();


    $(window).scroll(function(){
        if($(this).scrollTop() > 325){
            $(".answers").addClass("fixSide-bar");
            var height = ($(this).scrollTop() + (nav_height + breadcrumb_height));
	    if($('#view_more_tickets').is(':visible')){
		var node = $('#id_send_copy').length && $('#id_send_copy').is(':visible') ? '#id_send_copy' : '#id_link_url';
	    	
            }else{
	    	var node = $('.qq-upload-list-selector.qq-upload-list').length && $('.qq-upload-list-selector.qq-upload-list').is(':visible') ? '.qq-upload-list-selector.qq-upload-list' : '#id_link_url';
            }
            
            if( height > $(node).offset().top && $('.gluu-info-box.answers ul li').length > 1 ){
                $(".answers").addClass("scrollSide-bar");
            } else {
                $(".answers").removeClass("scrollSide-bar");
            }
        }
        else if($(this).scrollTop() < 325){
            $(".answers").removeClass("scrollSide-bar");
            if($(this).scrollTop() < 850){
                $(".answers").removeClass("fixSide-bar");
            }
        }

});

    // Dynamic Logic For Creating Ticket On Behalf of Someone

    if ($('#id_company').length && $('#id_created_for').length) {

        if ($('#id_company').find('option:selected').html().trim() != 'Select a company'){
            if($('#id_created_for').find('option:selected').html() === undefined){
                populateCompanyMembers();
            }
            $('#div_id_created_for').removeClass('hidden');
        }

        $('#id_company').change(function(){
            if ($(this).find('option:selected').html().trim() == 'Select a company')
            {
                $('#id_created_for').find('option').remove();
                $('#id_created_for').select2("val","");
            }else{
                populateCompanyMembers();
                $('#id_created_for').select2("val","");
            }
        });

        $("form").submit(function(){
            if ($('#id_company').find('option:selected').html().trim() != 'Select a company' &&
                $('#id_created_for').find('option:selected').val() == 'N/A')
            {
                alert('Please specify a user in the company you want to create an account for.');
                event.preventDefault();
            }

        });
    }

    $("#submit-id-save").click(function(e){
        e.preventDefault();
        var all_ok = true;
        var check = 0;
        if($("#id_gluu_server_version").val()==""){
           $("#id_gluu_server_version").parent().parent().addClass("has-error");
           $("#id_gluu_server_version").parent().parent().find(".controls > .help-block").remove();
           $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($("#id_gluu_server_version").parent().parent().find(".controls"));
           $("#id_gluu_server_version").focus();
           all_ok = false;
           check =1;
        }
        else{
            $("#id_gluu_server_version").parent().parent().removeClass("has-error");
            $("#id_gluu_server_version").parent().parent().find(".controls > .help-block").remove();
        }
        if($("#div_id_gluu_server_version_comments").is(":visible")){
           if ($("#id_gluu_server_version_comments").val()==""){
               $("#id_gluu_server_version_comments").parent().parent().addClass("has-error");
               $("#id_gluu_server_version_comments").parent().parent().find(".controls > .help-block").remove();
               $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($("#id_gluu_server_version_comments").parent().parent().find(".controls"));
               $("#id_gluu_server_version_comments").focus();
               all_ok = false;
               check =2;
           }

        }
        else{
            $("#id_gluu_server_version_comments").parent().parent().removeClass("has-error");
            $("#id_gluu_server_version_comments").parent().parent().find(".controls > .help-block").remove();
        }
        if($("#id_os_version").val()==""){
           $("#id_os_version").parent().parent().addClass("has-error");
           $("#id_os_version").parent().parent().find(".controls > .help-block").remove();
           $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($("#id_os_version").parent().parent().find(".controls"));
           $("#id_os_version").focus();
           all_ok = false;
           check =3;
        }
        else{
            $("#id_os_version").parent().parent().removeClass("has-error");
            $("#id_os_version").parent().parent().find(".controls > .help-block").remove();
        }

        if($("#id_os_version_name").val()==""){
           $("#id_os_version_name").parent().parent().addClass("has-error");
           $("#id_os_version_name").parent().parent().find(".controls > .help-block").remove();
           $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($("#id_os_version_name").parent().parent().find(".controls"));
           $("#id_os_version_name").focus();
           all_ok = false;
           check =4;
        }
        else{
            $("#id_os_version_name").parent().parent().removeClass("has-error");
            $("#id_os_version_name").parent().parent().find(".controls > .help-block").remove();
        }

        if($("#div_id_product").is(":visible")){
            $("select.product").each(function(){
                if($(this).val()==""){
                   $(this).parent().parent().addClass("has-error");
                   $(this).parent().parent().find(".controls > .help-block").remove();
                   $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($(this).parent().parent().find(".controls"));
                   $(this).focus();
                   all_ok = false;
                   check =5;
                }
                else{
                    $(this).parent().parent().removeClass("has-error");
                    $(this).parent().parent().find(".controls > .help-block").remove();
                }
            });
            $("select.product_version").each(function(){
                if($(this).val()==""){
                   $(this).parent().parent().addClass("has-error");
                   $(this).parent().parent().find(".controls > .help-block").remove();
                   $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($(this).parent().parent().find(".controls"));
                   $(this).focus();
                   all_ok = false;
                   check =6;
                }
                else{
                    $(this).parent().parent().removeClass("has-error");
                    $(this).parent().parent().find(".controls > .help-block").remove();
                }
            });
            $("select.product_os_version").each(function(){
                if($(this).val()==""){
                   $(this).parent().parent().addClass("has-error");
                   $(this).parent().parent().find(".controls > .help-block").remove();
                   $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($(this).parent().parent().find(".controls"));
                   $(this).focus();
                   all_ok = false;
                   check =7;
                }
                else{
                    $(this).parent().parent().removeClass("has-error");
                    $(this).parent().parent().find(".controls > .help-block").remove();
                }
            });
            $(".product_os_version_name").each(function(){
                if($(this).val()==""){
                   $(this).parent().parent().addClass("has-error");
                   $(this).parent().parent().find(".controls > .help-block").remove();
                   $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($(this).parent().parent().find(".controls"));
                   $(this).focus();
                   all_ok = false;
                   check =8;
                }
                else{
                    $(this).parent().parent().removeClass("has-error");
                    $(this).parent().parent().find(".controls > .help-block").remove();
                }
            });

            $(".ios_version_name").each(function(){
                if($(this).val()=="" && $(this).parent().parent().is(":visible")){
                   $(this).parent().parent().addClass("has-error");
                   $(this).parent().parent().find(".controls > .help-block").remove();
                   $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($(this).parent().parent().find(".controls"));
                   $(this).focus();
                   all_ok = false;
                   check =9;
                }
                else{
                    $(this).parent().parent().removeClass("has-error");
                    $(this).parent().parent().find(".controls > .help-block").remove();
                }
            });

        }
        if($("#id_issue_type").val()=="" && $("#div_id_issue_type").is(":visible")){
           $("#id_issue_type").parent().parent().addClass("has-error");
           $("#id_issue_type").parent().parent().find(".controls > .help-block").remove();
           $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($("#id_issue_type").parent().parent().find(".controls"));
           $("#id_issue_type").focus();
           all_ok = false;
           check =10;
        }
        else{
            $("#id_issue_type").parent().parent().removeClass("has-error");
            $("#id_issue_type").parent().parent().find(".controls > .help-block").remove();
        }
        if($("#id_ticket_category").val()==""){
           $("#id_ticket_category").parent().parent().addClass("has-error");
           $("#id_ticket_category").parent().parent().find(".controls > .help-block").remove();
           $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($("#id_ticket_category").parent().parent().find(".controls"));
           $("#id_ticket_category").focus();
           all_ok = false;
           check =11;
        }
        else{
            $("#id_ticket_category").parent().parent().removeClass("has-error");
            $("#id_ticket_category").parent().parent().find(".controls > .help-block").remove();
        }
        if($("#id_title").val()==""){
           $("#id_title").parent().parent().addClass("has-error");
           $("#id_title").parent().parent().find(".controls > .help-block").remove();
           $('<p  class="help-block"><strong>This field is required.</strong></p>').appendTo($("#id_title").parent().parent().find(".controls"));
           $("#id_title").focus();
           all_ok = false;
           check =12;
        }
        else{
            $("#id_title").parent().parent().removeClass("has-error");
            $("#id_title").parent().parent().find(".controls > .help-block").remove();
        }
        if(simplemde.value()==""){
           $("#id_description").parent().parent().addClass("has-error");
           $("#id_description").parent().parent().parent().find(".controls > .help-block").remove();
           $('<span id="hint_id_description" class="help-block">This field supports <a target="_blank" href="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet">markdown formatting.</a></span><p class="help-block"><strong>This field is required.</strong></p>').appendTo($("#id_description").parent().parent().parent().find(".controls"));
           $("#id_description").focus();
           all_ok = false;
           check =13;
        }
        else{
            $("#id_description").parent().parent().removeClass("has-error");
            $("#id_description").parent().parent().parent().find(".controls > .help-block").remove();
            $('<span id="hint_id_description" class="help-block">This field supports <a target="_blank" href="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet">markdown formatting.</a></span>').appendTo($("#id_description").parent().parent().parent().find(".controls"));
        }
        if($(".qq-upload-file").length > 4){
            alert("Sorry! You can not upload more than 4 files.");
            all_ok=false;
            check =14;
        }
        if(all_ok){
            $("#submit-id-save").attr("disabled","disabled");
            var arr_len = values_array.length;
            if(arr_len > 0){
                for(var x = 0; x < arr_len; x++){
                var value =values_array[x].split(' ').join('_')
                    $('.ticket_form').append('<input type="hidden" name="file_field" value='+value+'>');
                    $('.ticket_form').append('<input type="hidden" name ="file_src" value='+image_src_array[x]+'>');
                }
            }
            var ar_len= uploaded_value_array.length;
            if(ar_len > 0){
                for(var z=0; z< ar_len; z++){
                    $('.ticket_form').append('<input type="hidden" name="uploaded_files" value='+uploaded_value_array[z]+'>');
                }
            }else if(ar_len==0){
                $('.ticket_form').append('<input type="hidden" name="uploaded_files" value="">');
            }

            $(".ticket_form").submit();
        }
    });


});
