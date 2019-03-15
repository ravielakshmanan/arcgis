accessToken = 'pk.eyJ1IjoicGFua2h1cmlrdW1hciIsImEiOiJjamZwbnV2OTcxdXB1MzBudnViY2p3aDEzIn0.Zf9ZkY05gz_Zsyen1W1FbA';
var coords, placeName, image;
var data = [];
layer = 1

var mymap = L.map('map').setView([30.52, 18.34], 2.5);

baseLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: accessToken
}).addTo(mymap);
turnLayers();

function turnLayers() {
	if (layer > 0) {
		mymap.removeLayer(baseLayer)
		baseLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		    maxZoom: 18,
		    id: 'mapbox.streets',
		    accessToken: accessToken
		}).addTo(mymap);
		url_base = 'https://storage.googleapis.com/noah-water.appspot.com/intensityLayer/{z}/{x}/{-y}.png';
		tileImage = L.tileLayer(url_base).setOpacity(0.7);
		tileImage.addTo(mymap);
	} else {
		mymap.removeLayer(baseLayer)
		baseLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		    maxZoom: 18,
		    id: 'mapbox.satellite',
		    accessToken: accessToken
		}).addTo(mymap);
		url_base = 'https://storage.googleapis.com/noah-water.appspot.com/intensityLayer/{z}/{x}/{-y}.png';
		tileImage = L.tileLayer(url_base).setOpacity(0.7);
		tileImage.addTo(mymap);
	}
		
}

var searchControl = L.Control.geocoder({
        defaultMarkGeocode: false
    }).on('markgeocode', function(e) {
        console.log(e.geocode);
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

function round(value, step) {
    step || (step = 1.0);
    var inv = 1.0 / step;
    return Math.round(value * inv) / inv;
}

function findClosestLatitude(lat) {
    res = lat.toString().split(".");
    decimal = parseInt(res[1].substr(0, 3))

    switch (true) {
        case (decimal < 500):
            decimal = 225;
            break;
        case (decimal >= 500 && decimal < 999):
            decimal = 575;
            break;
    }

    new_lat = res[0] + "." + decimal;
    new_lat = parseFloat(new_lat);

    return new_lat;
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

    recreated_lng_trend = round(recreated_lng, 0.05);
    recreated_lat_trend = findClosestLatitude(lat);
    
    coordData = {
        'lat': recreated_lat,
        'lng': recreated_lng,
        'latT': recreated_lat_trend,
        'lngT': recreated_lng_trend,
        'latSign': lat_sign,
        'lngSign': lng_sign
    };

    renderGraph(lngLat, coordData);
}

function renderGraph(lngLat, coordData) {

    $.ajax({
        url: "/onclick",
        type: 'GET',
        data: coordData,
        success: function (res) {
            data_array = res.split("_");
            iri_data = data_array[0];
            trend_data = data_array[1];

            iri_data = iri_data.replace(/'/g, '"');
            iri_data = JSON.parse(iri_data);

            trend_data = trend_data.replace(/'/g, '"');
            trend_data = JSON.parse(trend_data);
            console.log(trend_data);

            $.get('https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=' + lngLat.lat + '&lon=' + lngLat.lng, function(geores) {
                console.log(geores);
                loc = geores['display_name'];
                loc_array = loc.split(", ");
                place = loc_array[1];
                country = loc_array[loc_array.length-1];
                if (geores['display_name'])
                    placeName = "<br>" + place + ", " + country + "<br>";
                else
                    placeName = "<br>";
                var marker = new L.Marker(coords)
                    .bindPopup('<div style="height:900px"><div id="iri-graph"></div><div id="trend-graph"></div></div>',
                        {'maxWidth': "auto", offset: [-350, 0], 'maxHeight': "400"})
                    .on('popupopen', function (e) {
                        Plotly.newPlot('iri-graph', [{
                            x: iri_data['dates'],
                            y: iri_data['data'],
                            name: 'Precipitation (mm)',
                            type: 'scatter'
                        }], {
                            title: 'Precipitation Data for ' + placeName + ' (' + recreated_lat + lat_sign + ", " + recreated_lng + lng_sign + ')',
                            xaxis: {
                                title: 'Date Range',
                                tickangle: 45
                            },
                            yaxis: {title: 'Precipitation Anomaly (mm)'},
                            height: 380
                        });

                        var prec = {
                          x: trend_data['dates'],
                          y: trend_data['prec'],
                          name: 'Precipitation (mm/year)',
                          type: 'scatter',
                          connectgaps: true,
                          mode: 'lines+markers',
                          line: {
                            color: 'rgb(31, 119, 180)',
                            width: 3
                          }
                        };
                        
                        var smoothed = {
                          x: trend_data['dates'],
                          y: trend_data['smoothed'],
                          name: 'Smoothed Precipitation (mm/year)',
                          yaxis: 'y2',
                          type: 'scatter',
                          connectgaps: true,
                          mode: 'lines+markers',
                            line: {
                                dash: 'dashdot',
                                color: 'rgb(255, 127, 14)',
                                width: 3
                            }
                        };

                        var trend = {
                          x: trend_data['dates'],
                          y: trend_data['trend'],
                          name: 'Precipitation Trend (mm/year)',
                          yaxis: 'y3',
                          type: 'scatter',
                          connectgaps: true,
                          mode: 'lines+markers',
                            line: {
                                dash: 'dot',
                                color: 'rgb(61, 229, 109)',
                                width: 3
                            }
                        };

                        var data = [prec, smoothed];

                        Plotly.newPlot('trend-graph', data, {
                            title: 'Average Annual Precipitation Shifts for ' + placeName + ' (' + recreated_lat + lat_sign + ", " + recreated_lng + lng_sign + ')',
                            xaxis: {
                                title: 'Year',
                                tickangle: 45
                            },
                            yaxis: {
                                title: 'Average Annual Precipitation (mm/year)',
                                tickfont: {color: '#1f77b4'},
                                showgrid: true
                            },
                            yaxis2: {
                                tickfont: {color: '#ff7f0e'},
                                overlaying: 'y',
                                anchor: 'x',
                                side: 'right',
                                position: 0.85,
                                showticklabels: true,
                                showgrid: false
                            },
                            // yaxis3: {
                            //     tickfont: {color: '#3de56d'},
                            //     overlaying: 'y',
                            //     anchor: 'free',
                            //     side: 'right',
                            //     position: 1.7,
                            //     showticklabels: true,
                            //     showgrid: false
                            // },
                            legend: {
                                "orientation": "h",
                                x: 0,
                                y: -0.5
                            },
                            height: 550
                        });
                    }).addTo(mymap);
                marker.getPopup().update();
                marker.openPopup();
            });
        }
    });
}

mymap.on('click', function(e) {
    console.log("Click event triggered!");
    console.log(e.latlng);
    coords = e.latlng;
    mymap.flyTo([e.latlng.lat+1, e.latlng.lng], 8);
    findClosest(e.latlng);

    $("#side-bar").dialog({ height: 750,
    						position: { my: "right top", at: "right top", of: window},
    						classes: {"ui-dialog": "add-margin"}});
    $('#side-bar').scrollTop(0);
    $(window).scrollTop(0);
    // $("#side-bar").dialog('open');
});

$('#intro-bar').dialog({height: 450,
						width: 700,
						modal:true,
                        resizable: false});

document.getElementById('layerButton').addEventListener('click', function() {
	layer = layer * (-1);
	turnLayers();
})

document.getElementById('zoomButton').addEventListener('click', function () {
    mymap.flyTo([30.52, 18.34], 2.5);
    $('#side-bar').dialog('destroy');
    if ($("#leaflet-popup")) {
        $(".leaflet-popup-close-button")[0].click();
    }
});