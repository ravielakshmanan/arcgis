accessToken = 'pk.eyJ1IjoicGFua2h1cmlrdW1hciIsImEiOiJjamZwbnV2OTcxdXB1MzBudnViY2p3aDEzIn0.Zf9ZkY05gz_Zsyen1W1FbA';
var zooming = false;
var coords, popup, placeName;
var data = [];

// d3.csv("static/data/transposed.csv", function(readdata) {
//     data = readdata;
//     console.log("Data Read!");
//     console.log(data.length);
// });

var mymap = L.map('map').setView([30.52, 18.34], 2.5);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.satellite',
    accessToken: accessToken
}).addTo(mymap);

var searchControl = L.Control.geocoder({
        defaultMarkGeocode: false
    })
    .on('markgeocode', function(e) {
        var bbox = e.geocode.bbox;
        var poly = L.polygon([
             bbox.getSouthEast(),
             bbox.getNorthEast(),
             bbox.getNorthWest(),
             bbox.getSouthWest()
        ]).addTo(mymap);
        mymap.fitBounds(poly.getBounds());
        });

document.getElementById('geocoder').appendChild(searchControl.onAdd(map));

// function createTable(recreated_lng, recreated_lat, lng_sign, lat_sign) {
//     lng = String(recreated_lng) + lng_sign;
//     lat = String(recreated_lat) + lat_sign;
//     var map_x = [];
//     var map_y = [];
//
//     var row;
//     console.log(lng, lat);
//     for(i = 0; i < data.length; i++) {
//         if(data[i].Longitude == lng && data[i].Latitude == lat) {
//             row = data[i];
//             time = row.Time.split(" 16 ");
//             map_x.push(time.splice(-1)[0]);
//             map_y.push(row["Precipitation Anomaly"]);
//         }
//     }
//
//     geocoder.mapboxClient.geocodeReverse({
//         latitude: coords.lngLat.lat,
//         longitude: coords.lngLat.lng
//     }, function(err, res) {
//     	found_flag = 0;
//     	if (res.features) {
//     		for (i = 0; i < res.features.length; i++) {
//     			var item = res.features[i];
//     			if (item['id'].includes('place')) {
//     				placeName = item['place_name'];
//     				found_flag = 1;
//     			}
//     		}
//     		if (found_flag == 0) {
//     			placeName = res.features[0]['place_name'];
//     		}
//     	} else{
//     		placeName = ""
//     	}
//
//     	var marker = L.marker(e.latlng)
//             .bindPopup("<div id='iri-graph'></div>")
//             .on('popupopen', function(e) {
//                 Plotly.newPlot('iri-graph', [{
//                     x: [0, 1], //map_x,
//                     y: [4, 6], //map_y,
//                     name: 'Precipitation',
//                     type: 'scatter'
//                 }], {
//                     title: 'Precipitation Data for ' // + placeName + ' (' + lng + ", " + lat + ')',
//                     width: 300,
//                     height: 150,
//                     margin: {
//                         l: 0,
//                         r: 0,
//                         b: 0,
//                         t: 0,
//                         pad: 0
//                     }
//                 });
//             }).addTo(mymap);
//     });
// }

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

    // createTable(recreated_lng, recreated_lat, lng_sign, lat_sign);
}

zoomlevel = 8.1;
mymap.on('click', function(e) {
    console.log(e.latlng);
    mymap.flyTo([e.latlng.lat, e.latlng.lng], 8);
    // findClosest(e.latlng);
    var marker = L.marker(e.latlng).addTo(mymap);
    var popUp = L.popup({ offset: [0, -40] })
       .setLatLng(e.latlng)
       .setContent("<div id='iri-graph'>YIKES!</div>")
       .addTo(mymap);
    $("#side-bar").dialog({ position: { my: "right top", at: "right top", of: window},
    						classes: {"ui-dialog": "add-margin"}});
});

$('#intro-bar').dialog({height: 380,
						width: 780,
						modal:true,
                        resizable: false});

document.getElementById('zoomButton').addEventListener('click', function () {
    mymap.flyTo([30.52, 18.34], 2.5);
    $(".leaflet-popup-close-button")[0].click();
    $('#side-bar').dialog('destroy');
});