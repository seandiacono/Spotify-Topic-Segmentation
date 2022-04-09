
$(document).ready(function(){
    $("[name='segmentation-type']").change(function(){
        var value = $(this).val();
        if (value == 2){
            $("input.group1").prop("disabled", true);
            $("select.group1").prop("disabled", true);
            $("input.group2").prop("disabled", false);
        }
        else{
            $("input.group1").prop("disabled", false);
            $("select.group1").prop("disabled", false);
            $("input.group2").prop("disabled", true);
        }
    });
});


function getSummaries(segments) {

    url = 'http://127.0.0.1:8000/';

    var summarization_val = document.forms['segmentation-form']['summarization-type'].value;
    var num_segments = document.forms['segmentation-form']['num-segments'].value;

    if (summarization_val == 1){
        $.ajax({
            url: url + 't5_summarization',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'segments': segments,
                'num_segments': num_segments,
            }),
            contentType: 'application/json',
            success: function(data){
                document.getElementById('segment-area').innerHTML = '';
                data['segments'].forEach(function(segment){
                    document.getElementById('segment-area').innerHTML += "<h4 class=\"segment-title\">" + Object.keys(segment)[0] + "</h4> <div class='segment'>" + Object.values(segment)[0] + "</div>";
                });
            },
        });
    } else if (summarization_val == 2){
        $.ajax({
            url: url + 'pegasus_summarization',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'segments': segments,
                'num_segments': num_segments,
            }),
            contentType: 'application/json',
            success: function(data){
                document.getElementById('segment-area').innerHTML = '';
                data['segments'].forEach(function(segment){
                    document.getElementById('segment-area').innerHTML += "<h4 class=\"segment-title\">" + Object.keys(segment)[0] + "</h4> <div class='segment'>" + Object.values(segment)[0] + "</div>";
                });
            },
        });
    } else if (summarization_val == 3){
        $.ajax({
            url: url + 'bart_summarization',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'segments': segments,
                'num_segments': num_segments,
            }),
            contentType: 'application/json',
            success: function(data){
                document.getElementById('segment-area').innerHTML = '';
                data['segments'].forEach(function(segment){
                    document.getElementById('segment-area').innerHTML += "<h4 class=\"segment-title\">" + Object.keys(segment)[0] + "</h4> <div class='segment'>" + Object.values(segment)[0] + "</div>";
                });
            },
        });
    }

}




function getSegments(){

    url = 'http://127.0.0.1:8000/'

    var segmentation_val = document.forms['segmentation-form']['segmentation-type'].value;
    var podcast_index = document.forms['segmentation-form']['podcast-index'].value;
    
    if (segmentation_val == 1){
        var w = document.forms['segmentation-form']['window-size'].value;
        var k = document.forms['segmentation-form']['block-size'].value;
        var smooth_width = document.forms['segmentation-form']['smoothing-width'].value;
        var smooth_rounds = document.forms['segmentation-form']['smoothing-rounds'].value;
        var cutoff = document.forms['segmentation-form']['cutoff-policy'].value;

        $.ajax({
            url: url + 'text_tiling',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'podcast_index': podcast_index,
                'window_size': w,
                'block_size': k,
                'smoothing_width': smooth_width,
                'smoothing_rounds': smooth_rounds,
                'cutoff_policy': cutoff,
                'split_penalty': split_penalty 
            }),
            contentType: 'application/json',
            beforeSend: function() {
                document.getElementById('segment-area').innerHTML = '<div class="d-flex justify-content-center"><img id="loading" src="assets/loading.gif" alt="loading" /> </div>';
            },
            success: function(data){
                getSummaries(data);
            },
        });

    }else{
        var split_penalty = document.forms['segmentation-form']['split-penalty'].value;

        $.ajax({
            url: url + 'text_split',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'podcast_index': podcast_index,
                'split_penalty': split_penalty 
            }),
            contentType: 'application/json',
            beforeSend: function() {
                document.getElementById('segment-area').innerHTML = '<div class="d-flex justify-content-center"><img id="loading" src="assets/loading.gif" alt="loading" /> </div>';
            },
            success: function(data){
                getSummaries(data);
            },
        });
    }


}