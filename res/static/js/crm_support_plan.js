
function addRow(key, value){

    return '<label class="info-left-result">'+ key +':</label>'+
           '<p class="info-right-result">'+ value +'</p>'+
           '<div class="clearfix"></div>';
}

$(document).ready(function(){

    var csrf = getCookie('csrftoken');
   
    $.ajax({
        type: 'GET',
        url: '/ws/inline/support-plan/' + id,
        data: 'csrfmiddlewaretoken='+csrf
    }).done(function(support_plan) {

        additionalMarkup = '';

        if(support_plan['support_plan']){
            additionalMarkup += addRow('Support Plan', support_plan['support_plan']);
        } else {
            additionalMarkup += addRow('Support Plan', 'n/a');
        }
        if(support_plan['managed_service']){
            additionalMarkup += addRow('Managed Service', support_plan['managed_service']);
        }
        if(support_plan['renewal_date']){
            additionalMarkup += addRow('Renewal', support_plan['renewal_date']);
        }
        $('#support-plan').html(additionalMarkup);


    }).fail(function() {
       
    });
});