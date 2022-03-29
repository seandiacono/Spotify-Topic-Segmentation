
$(document).ready(function(){
    $("input:radio").change(function(){
        var value = $(this).val();
        if (value == 2){
            $("input.group1").prop("disabled", true);
            $("select.group1").prop("disabled", true);
        }
        else{
            $("input.group1").prop("disabled", false);
            $("select.group1").prop("disabled", false);
        }
    });
});



function getTranscript(){
    
    url = 'http://127.0.0.1:8000/segment_summary'

    var val = document.forms['segmentation-form']['segmentation-type'].value;

    console.log(val);
    
    if (val == 1){
        var w = document.forms['segmentation-form']['window-size'].value;
        var k = document.forms['segmentation-form']['block-size'].value;
        var sim_method = document.forms['segmentation-form']['similarity-method'].value;
        var smooth_width = document.forms['segmentation-form']['smoothing-width'].value;
        var smooth_rounds = document.forms['segmentation-form']['smoothing-rounds'].value;
        var cutoff = document.forms['segmentation-form']['cutoff-policy'].value;
    }

    console.log(JSON.stringify({
        'segmentation_type': val,
        'window_size': w,
        'block_size': k,
        'similarity_method': sim_method,
        'smoothing_width': smooth_width,
        'smoothing_rounds': smooth_rounds,
        'cutoff_policy': cutoff
    }));

    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        data: JSON.stringify({
            'segmentation_type': val,
            'window_size': w,
            'block_size': k,
            'similarity_method': sim_method,
            'smoothing_width': smooth_width,
            'smoothing_rounds': smooth_rounds,
            'cutoff_policy': cutoff
        }),
        contentType: 'application/json',
        beforeSend: function() {
            $('#loading-div').css('visibility', 'visible');
            document.getElementById('segment-area').innerHTML = '';
        },
        success: function(data){
            console.log(data);
            data['segments'].forEach(function(segment){
                document.getElementById('segment-area').innerHTML += "<h4 class=\"segment-title\">" + Object.keys(segment)[0] + "</h4> <div class='segment'>" + Object.values(segment)[0] + "</div>";
            });
        },
        complete: function(){
            $('#loading-div').css('visibility', 'hidden');
        }
    });
}