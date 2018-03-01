$(document).ready(function() {
    $('#searchtable').DataTable( {
        "paging": false,
        "searching": false,
        "columnDefs": [
          { "width": "600px", "targets": 1 }
        ],
        "autoWidth": false,

    } );
} );

$('#id_q').focusout(function() {
    if ( typeof $('#id_q').val().length === 'undefined' || $('#id_q').val().length < 1 )
        $('#preview').removeClass("loader").html('')
});

$( '#id_q' ).autocomplete( {
	serviceUrl: "/ws/autocomplete-search/",
	type: 'GET',
	paramName: 'q',
	dataType: 'json',
	noCache: false,
    minChars: 3,
	showNoSuggestionNotice: true,
	noSuggestionNotice: 'Sorry, no matching results',
	onSearchStart: function ( e ) {
	    $('.search-field, #preview').addClass('loader');
	},
	onSelect: function ( suggestion ) {
	    fetch_details();
	},
	onSearchComplete: function ( query, suggestions ) {
        fetch_details();
    },
} );

function fetch_details() {
    $('.search-field').removeClass('loader');
    return true;
    $.ajax({
        type: "GET",
        url: "/ws/search-homepage/",
        data: {
            'q' : $('#id_q').val(),
            'category': $('#id_category').val(),
            'status': $('#id_status').val(),
            'csrfmiddlewaretoken' : getCookie('csrftoken')
        },
        success: function(data){
            var json = $.parseJSON(data);
            if ($('#id_q').val().length >= 3){
                $('#preview').removeClass("loader").html(json.result)
            }
        },
        fail: function(){
            $('#preview').removeClass("loader").html('');
        },
        dataType: 'html',
    });
}
