function menu_feedback(text){
    //generate a random id for the feedback div
    var id = Math.random().toString(36).substring(7);

    //add a div with the feedback text to the menu
    var fb_element = '<div class="menu_feedback" id="'+id+'">'+text+'</div>';
    $('#menu_section').append(fb_element);

    //fade out the feedback div after 5 seconds
    setTimeout(function(){
        $('#'+id).fadeOut(1000, function() {
            $(this).remove();
        });
    }, 5000);
}

function write_pfd(action){
    //make ajax call to the action url
    $.ajax({
        type: 'POST',
        url: action,
        data: {},
        success: function(data) {
            menu_feedback(data['message']);
        },
        error: function() {
            menu_feedback("Error");
        }
    });
}

$(document).ready(function() {

    //set up the click event for the write_pfd buttons
    $("button.menu-button").click(function() {
        var action = $(this).attr('data-action');
        write_pfd(action);
    });
    
});