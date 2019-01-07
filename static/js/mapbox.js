mapboxgl.accessToken = 'pk.eyJ1IjoicGFua2h1cmlrdW1hciIsImEiOiJjamZwbnV2OTcxdXB1MzBudnViY2p3aDEzIn0.Zf9ZkY05gz_Zsyen1W1FbA';
var zooming = false;
var coords, popup;
var data = [];

// d3.csv("https://storage.googleapis.com/iridatacsv/transposed.csv", function(readdata) {
//     data = readdata;
//     console.log("Data Read!");
//     console.log(data.length);
// });

const map = new mapboxgl.Map({
	container: 'map',
	style: 'mapbox://styles/pankhurikumar/cjnb7luyx5iu62rrw4fpyyz9f'
});

var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken
});

document.getElementById('geocoder').appendChild(geocoder.onAdd(map));

function createTable(recreated_lng, recreated_lat, lng_sign, lat_sign) {
    lng = String(recreated_lng) + lng_sign;
    lat = String(recreated_lat) + lat_sign;
    var map_x = [];
    var map_y = [];

    var row;
    console.log(lng, lat);
    for(i = 0; i < data.length; i++) {
        if(data[i].Longitude == lng && data[i].Latitude == lat) {
            row = data[i];
            time = row.Time.split(" 16 ");
            map_x.push(time.splice(-1)[0]);
            map_y.push(row["Precipitation Anomaly"]);
        }
    }
    popup = new mapboxgl.Popup({offset:30})
	            .setLngLat(coords.lngLat)
                .setHTML("<div id='foo'></div>")
	            .addTo(map);

    popup.on('open', function() {
        Plotly.newPlot('foo', [{
                x: map_x,
                y: map_y,
                name: 'Precipitation',
                type: 'scatter'
            }], {
            title: 'Precipitation Data for (' + lng + ", " + lat + ')',
            height: 380
        });
    }).addTo(map);

    new mapboxgl.Marker()
    	.setLngLat(coords.lngLat)
    	.addTo(map);
}

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

    createTable(recreated_lng, recreated_lat, lng_sign, lat_sign);
}

//zstart is defined by me, .fire() calls this function in map.on()
map.on('zstart', function(){
	zooming = true;
});

//zend in defined by me, called at the end of the zoom to set zooming value
map.on('zend', function(){
	zooming = false;
});

//zoomend is predefined, function called automatically when zoom ends
map.on('zoomend', function(){
	if(zooming) {
	    findClosest(coords.lngLat);
	    map.fire('zend');
  	}
});

zoomlevel = 8.1;
map.on('load', function() {

    map.on('click', function(e) {
    	// console.log(e.features[0].geometry.coordinates);
    	if (zoomlevel == 8)
    		zoomlevel = 8.1;
    	else
    		zoomlevel = 8;
    	coords = e;
    	map.setCenter(e.lngLat);
    	// console.log(e.lngLat);
    	map.zoomTo(zoomlevel);
    	$("#side-bar").dialog({ position: { my: "right top", at: "right top", of: window},
    							classes: {"ui-dialog": "add-margin"}});
    	map.fire('zstart');
    })
});

$('#intro-bar').dialog({height: 380,
						width: 780,
						modal:true,
                        resizable: false});

document.getElementById('zoomButton').addEventListener('click', function () {
    map.setCenter([12.919578242062556, 38.92232061838632]);
    popup.remove();
    $('#side-bar').dialog('destroy');
    map.zoomTo(1.8);
});