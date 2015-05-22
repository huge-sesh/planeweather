$(document).ready(function() {
    map = function() {
        var start = document.getElementById('start').value;
        var dest  = document.getElementById('dest').value;
        var datetime = document.getElementById('datetime').value;
        var speed   = document.getElementById('speed').value;
        var timestep = document.getElementById('timestep').value;

        $.getJSON('/forecast/'+[start, dest, datetime, speed, timestep].join('/')).done(function(response) {
            var forecast = response.forecast;
            var middle = forecast[Math.floor(forecast.length / 2)];
            var map = new google.maps.Map(document.getElementById('map'), {
              zoom: 2,
              center: new google.maps.LatLng(middle.location[0], middle.location[1]),
              mapTypeId: google.maps.MapTypeId.ROADMAP
            });
            var infowindow = new google.maps.InfoWindow();
            var marker, i;
            for (i = 0; i < forecast.length; i++) {  
                f = forecast[i];
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(forecast[i].location[0], forecast[i].location[1]),
                    map: map
                });
                google.maps.event.addListener(marker, 'click', (function(marker, i) {
                    f = forecast[i];
                    return function() {
                        infowindow.setContent("humidity: "+f.humidity+"<br>temperature: "+f.temperature+"<br>wind speed: "+f.wind_speed);
                        infowindow.open(map, marker);
                    }
                })(marker, i));
            }
        });
    };
    var currentDate = new Date();
    var timezoneOffset = currentDate.getTimezoneOffset() * 60 * 1000;
    var localDate = new Date(currentDate.getTime() - timezoneOffset);
    var localDateISOString = localDate.toISOString().replace('Z', '');
    document.getElementById('datetime').value = localDateISOString;
    map();
});
