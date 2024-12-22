var update_interval = 1000; // 1 second

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

$(document).ready(function() {
    //set up the automatic saving
    if ( $('#req_text_form').length > 0 ) {

        save_form_input('#req_text_form');
    }
});
        