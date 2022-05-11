$(document).ready(function(){
    url = 'http://127.0.0.1:8000/';

    var video = videojs('video');
    video.fill(true);

    $.ajax({
        url: url + 'timestamp_summaries',
        type: 'GET',
        dataType: 'json',
        success: function(data){
            console.log(data);
            video.markers({
                markerTip:{
                    display: true,
                    text: function(marker) {
                        return marker.text;
                    },
                    time: function(marker) {
                        return marker.time;
                    }},
                markers: data['0ERGF0SNWOCUSjecWZGJ82']})
        }
    });
});