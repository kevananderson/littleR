var update_interval = 1000; // 1 second

function copy_to_clipboard(id) {
    var text = $(id).html();
    navigator.clipboard.writeText(text).then( 
        function(){},
        function(){
            text.select();
            document.execCommand('copy');
        }
    );
    $(id).html('&nbsp;Copied&nbsp;&nbsp;');
    setTimeout(function() {
        $(id).html(text);
    }, 1000);

}

function submit_form_on_path_change() {
    form = $('#req_path_form');
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data) {
            //clear any previous error messages
            $('#req_path_form > .error_message').remove();
            //add new error message if there is one
            if (!data['success']) {
                new_element = '<div class="error_message">'+data['message']+'</div>';
                $('#req_path_form').append(new_element);
            }

        },
        error: function() {
            //clear any previous error messages
            $('#req_path_form > .error_message').remove();
            //add new error message if there is one
            if (!data['success']) {
                new_element = '<div class="error_message">'+data['message']+'</div>';
                $('#req_path_form').append(new_element);
            }
        }
    });                
}

function add_new_req() {
    form = $('#req_path_form');
    $.ajax({
        type: 'post',
        url: "/viewR/ajax_add_req",
        data: form.serialize(),
        success: function(data) {
            //change to the new page
            window.location.href = data['new_req_url'];
        }
    });                
}

function simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
}

function save_form_input(form_id) {
    var form = $(form_id);
    var data = form.serialize();
    var hash = simpleHash(data);
    var last_hash_name = form_id + '_last_hash';
    var last_hash = window.localStorage.getItem(last_hash_name);
    if (hash == last_hash) {
        //no change, so don't save
        setTimeout(function() {save_form_input(form_id);}, update_interval);
        return;
    }
    //there was a change, so save it and submit
    window.localStorage.setItem(last_hash_name, hash);
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: data,
        complete: function() {
            //schedule next update
            setTimeout(function() {save_form_input(form_id);}, update_interval);
        }
    });       
}

function submit_form_on_change(form_id) {
    var form = $(form_id);
    if (form.length > 0) {
        var data = form.serialize();
        var hash = simpleHash(data);
        var last_hash_name = form_id + '_last_hash';
        window.localStorage.setItem(last_hash_name, hash);
        save_form_input(form_id);
    }
}

function delete_label(label) {
    var form = $('#delete_req_label_form')
    var data = form.serializeArray(); // convert form to array
    data.push({name: "label", value: label});
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: $.param(data),
        success: function(data) {
            if (data['success']) {
                $('#req_label').replaceWith(data['req_label']);

                //set up the click event for the delete label button
                $("button.delete-label").click(function() {
                    var label_text = $(this).attr('data-label');
                    delete_label(label_text);
                });
            }
        }
    });
}

function add_label() {
    var form = $('#add_req_label_form');
    var data = form.serialize();
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: data,
        success: function(data) {
            if (data['success']) {
                $('#req_label').replaceWith(data['req_label']);

                //clear the input field
                $('#id_new_label').val('');

                //set up the click event for the delete label button
                $("button.delete-label").click(function() {
                    var label_text = $(this).attr('data-label');
                    delete_label(label_text);
                });
            }
        }
    });
}

function delete_relation(index) {
    var form = $('#delete_req_relation_form')
    var data = form.serializeArray(); // convert form to array
    data.push({name: "delete", value: index});
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: $.param(data),
        success: function(data) {
            if (data['success']) {
                $('#req_relation').replaceWith(data['req_relation']);

                //set up the click event for the delete label button
                $("button.delete-relation").click(function() {
                    var data_index = $(this).attr('data-index');
                    delete_relation(data_index);
                });
            }
        }
    });
}

function add_relation() {
    var form = $('#add_req_relation_form');
    var data = form.serialize();
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: data,
        success: function(data) {
            if (data['success']) {
                $('#req_relation').replaceWith(data['req_relation']);

                //clear the input field
                $('#id_new_parent').val('');
                $('#id_new_child').val('');
                $('#id_new_related').val('');

                //set up the click event for the delete label button
                $("button.delete-relation").click(function() {
                    var data_index = $(this).attr('data-index');
                    delete_relation(data_index);
                });
            }
        }
    });
}


$(document).ready(function() {

    //set it up that any click on an index div will copy the text to the clipboard
    $("div.index").click(function() {
        var id = '#'+$(this).attr('id');
        copy_to_clipboard(id);
    });    

    //setup form submission for req_path_form when the path changes
    $('#id_path').change(function() {
        submit_form_on_path_change();
    });

    $("#add_new_req").click(function() {
        add_new_req();
    });    
    
    //set up the automatic saving for req_text_form
    if ( $('#req_text_form').length > 0 ) {
        save_form_input('#req_text_form');
    }

    //set up the click event for the delete label button
    $("button.delete-label").click(function() {
        var label_text = $(this).attr('data-label');
        delete_label(label_text);
    });
    
    //set up the form submit event for the add label button
    $("#add_req_label_form").submit(function(event) {
        event.preventDefault(); // Prevent default form submission    
        add_label();
    });

    //set up the click event for the delete relation button
    $("button.delete-relation").click(function() {
        var data_relation = $(this).attr('data-relation');
        var data_index = $(this).attr('data-index');
        delete_relation(data_relation, data_index);
    });
   
    //set up the form submit event for the add relation button
    $("#add_req_relation_form").submit(function(event) {
        event.preventDefault(); // Prevent default form submission    
        add_relation();
    });

    
});