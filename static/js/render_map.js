accessToken = 'pk.eyJ1IjoicGFua2h1cmlrdW1hciIsImEiOiJjamZwbnV2OTcxdXB1MzBudnViY2p3aDEzIn0.Zf9ZkY05gz_Zsyen1W1FbA';
var coords, placeName, image;
var data = [];

var mymap = L.map('map').setView([30.52, 18.34], 2.5);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.satellite',
    accessToken: accessToken
}).addTo(mymap);

url_base = 'https://storage.googleapis.com/noah-water.appspot.com/intensityLayer/{z}/{x}/{y}.png';
image = L.tileLayer(url_base).setOpacity(0.7);
image.addTo(mymap);

var searchControl = L.Control.geocoder({
        defaultMarkGeocode: false
    }).on('markgeocode', function(e) {
        var bbox = e.geocode.bbox;
        var poly = L.polygon([
             bbox.getSouthEast(),
             bbox.getNorthEast(),
             bbox.getNorthWest(),
             bbox.getSouthWest()
        ]).addTo(mymap);
        mymap.fitBounds(poly.getBounds());
        mymap.flyTo([e.geocode.center.lat+1, e.geocode.center.lng], 8);
    });

document.getElementById('geocoder').appendChild(searchControl.onAdd(mymap));

function findClosest(lngLat) {
    lng = lngLat.lng;
    lat = lngLat.lat;

    lng_sign = (lng < 0) ? 'W' : 'E';
    lat_sign = (lat < 0) ? 'S' : 'N';
    lng = (lng < 0) ? lng*(-1) : lng;
    lat = (lat < 0) ? lat*(-1) : lat;

    x = Math.round(1 + (lng - 1.25)/2.5);
    y = Math.round(1 + (lat - 1.25)/2.5);

    recreated_lng = 1.25 + (x - 1) * 2.5;
    recreated_lat = 1.25 + (y - 1) * 2.5;

    coordData = {
        'lat': recreated_lat,
        'lng': recreated_lng,
        'latSign': lat_sign,
        'lngSign': lng_sign
    };

    $.ajax({
        url: "/onclick",
        type: 'GET',
        data: coordData,
        success: function (res) {
            new_res = res.replace(/'/g, '"');
            result = JSON.parse(new_res);
            $.get('https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=' + lngLat.lat + '&lon=' + lngLat.lng, function(geores) {
                console.log(geores);
                if (geores['display_name'])
                    placeName = "<br>" + geores['display_name'] + "<br>";
                else
                    placeName = "<br>";
                var marker = new L.Marker(coords)
                    .bindPopup('<div id="iri-graph"></div>', {maxWidth: "auto", offset: [-350, 0]})
                    .on('popupopen', function (e) {
                        Plotly.newPlot('iri-graph', [{
                            x: result['dates'],
                            y: result['data'],
                            name: 'Precipitation',
                            type: 'scatter'
                        }], {
                            title: 'Precipitation Data for ' + placeName + ' (' + recreated_lat + lat_sign + ", " + recreated_lng + lng_sign + ')',
                            xaxis: {title: 'Date Range'},
                            yaxis: {title: 'Precipitation Anomaly'},
                            height: 380
                        });
                    }).addTo(mymap);
                marker.openPopup();
            });
        }
    });
}

mymap.on('click', function(e) {
    console.log(e.latlng);
    coords = e.latlng;
    mymap.flyTo([e.latlng.lat+1, e.latlng.lng], 8);
    findClosest(e.latlng);

    $("#side-bar").dialog({ position: { my: "right top", at: "right top", of: window},
    						classes: {"ui-dialog": "add-margin"}});
    $("#side-bar").dialog('open');
});

$('#intro-bar').dialog({height: 350,
						width: 700,
						modal:true,
                        resizable: false});

document.getElementById('zoomButton').addEventListener('click', function () {
    mymap.flyTo([30.52, 18.34], 2.5);
    $(".leaflet-popup-close-button")[0].click();
    $('#side-bar').dialog('destroy');
    if (mymap.hasLayer(image)) {
		mymap.removeLayer(image);
	}
});