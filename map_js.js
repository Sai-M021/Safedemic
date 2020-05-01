var basic_map, heatmap, markers,data_pred_lis;
function createMap() {
    basic_map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37, lng: -50},
        zoom: 3,
        styles: [
            {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
            {
                featureType: 'administrative.locality',
                elementType: 'labels.text.fill',
                stylers: [{color: '#d59563'}]
            },
            {
                featureType: 'poi',
                elementType: 'labels.text.fill',
                stylers: [{color: '#d59563'}]
            },
            {
                featureType: 'poi.park',
                elementType: 'geometry',
                stylers: [{color: '#263c3f'}]
            },
            {
                featureType: 'poi.park',
                elementType: 'labels.text.fill',
                stylers: [{color: '#6b9a76'}]
            },
            {
                featureType: 'road',
                elementType: 'geometry',
                stylers: [{color: '#38414e'}]
            },
            {
                featureType: 'road',
                elementType: 'geometry.stroke',
                stylers: [{color: '#212a37'}]
            },
            {
                featureType: 'road',
                elementType: 'labels.text.fill',
                stylers: [{color: '#9ca5b3'}]
            },
            {
                featureType: 'road.highway',
                elementType: 'geometry',
                stylers: [{color: '#746855'}]
            },
            {
                featureType: 'road.highway',
                elementType: 'geometry.stroke',
                stylers: [{color: '#1f2835'}]
            },
            {
                featureType: 'road.highway',
                elementType: 'labels.text.fill',
                stylers: [{color: '#f3d19c'}]
            },
            {
                featureType: 'transit',
                elementType: 'geometry',
                stylers: [{color: '#2f3948'}]
            },
            {
                featureType: 'transit.station',
                elementType: 'labels.text.fill',
                stylers: [{color: '#d59563'}]
            },
            {
                featureType: 'water',
                elementType: 'geometry',
                stylers: [{color: '#17263c'}]
            },
            {
                featureType: 'water',
                elementType: 'labels.text.fill',
                stylers: [{color: '#515c6d'}]
            },
            {
                featureType: 'water',
                elementType: 'labels.text.stroke',
                stylers: [{color: '#17263c'}]
            }
        ]
    });

    predictedMap();
}

function toggleHeatmap() {
    heatmap.setMap(heatmap.getMap() ? null : basic_map);
}
function toggleViolations() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
}

function calc_distance(lat1,lng1,lat2,lng2){
    return Math.sqrt(Math.pow(lat2-lat1,2)  + Math.pow(lng2-lng1,2),0.5);
}

function parse_preds(text){     //lat,lng,num, city
    var count = (text.match(/,zczz/g) || []).length;
    var data = new Array(count);
    var pos = 0;
    var tpos=0;
    for(var c=0; c< count;c++){
        pos = text.indexOf(',zczz');
        var temp = text.slice(0,pos);
        tpos = temp.indexOf(',');
        var lat = parseFloat(temp.slice(0,tpos));
        temp = temp.substr(tpos+1);

        tpos = temp.indexOf(',');
        var lng = parseFloat(temp.slice(0,tpos));
        temp = temp.substr(tpos+1);

        tpos = temp.indexOf(',');
        var n = parseInt(temp.slice(0,tpos));
        temp = temp.substr(tpos);
        var city = temp.substr(1);

        if(city.indexOf('\"') > -1){
            city = city.slice(1,-1);
        }

        var group = [0,lat,lng,n,city]; // 0 for sorted distance
        data[c] = group;
        text = text.substr(pos+5);
    }
    return data;
}

function sortArr(data){
    var min_index, temp;
    var len = data.length;
    for(var i = 0; i < len; i++){
        min_index = i;
        for(var  j = i+1; j<len; j++){
            if(data[j][0]<data[min_index][0]){
                min_index = j;
            }
        }
        temp = data[i];
        data[i] = data[min_index];
        data[min_index] = temp;
    }
}

function load_predictions(){                          // list of lists. [[lat,long,#,city]]
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", "csv_files/prediction_num_new_cases_global_v2.csv", false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                data_pred_lis = parse_preds(allText);
            }
        }
    }
    rawFile.send(null);
}

function get_pred(lat,lng){
    length = data_pred_lis.length;
    for(var i = 0; i < length; i++){
        c_lat = data_pred_lis[i][1];
        c_lng = data_pred_lis[i][2];
        data_pred_lis[i][0] = calc_distance(lat,lng,c_lat,c_lng);
    }
    sortArr(data_pred_lis);
}

function updatePredCirc() {
    console.log("hi");
    var radius = document.getElementById("myRange").valueAsNumber;
    var c1_one_day_pred = data_pred_lis[0][3];
    var c2_one_day_pred = data_pred_lis[1][3];
    var c3_one_day_pred = data_pred_lis[2][3];
    var c4_one_day_pred = data_pred_lis[3][3];
    var c5_one_day_pred = data_pred_lis[4][3];

    var city1 = data_pred_lis[0][4];
    var city2 = data_pred_lis[1][4];
    var city3 = data_pred_lis[2][4];
    var city4 = data_pred_lis[3][4];
    var city5 = data_pred_lis[4][4];

    var case_s = "cases";

    if(c1_one_day_pred == 1) {
        case_s = "case";
    }
    var contentString = "<b>Predictions cannot be made at this location.</b>"

    console.log(data_pred_lis.slice(0,5));

    if(data_pred_lis[0][0] < radius/69) {
        contentString = '<div id="content">' +
            '<b>' + city1 + ':</b>  ' + c1_one_day_pred + ' new '+case_s+' predicted tomorrow';
    }
    if(data_pred_lis[1][0] < radius/69) {
        contentString = contentString + '<p><b>' + city2 + ':</b> ' + c2_one_day_pred + '<br />';
        if(data_pred_lis[2][0] < radius/69) {
            contentString = contentString + '<b>' + city3 + ':</b> ' + c3_one_day_pred + '<br />';
        }
        if(data_pred_lis[3][0] < radius/69) {
            contentString = contentString + '<b>' + city4 + ':</b> ' + c4_one_day_pred + '<br />';
        }
        if(data_pred_lis[4][0] < radius/69) {
            contentString = contentString + '<b>' + city5 + ':</b> ' + c5_one_day_pred + '<br />';
        }
        contentString = contentString + '</p>';
    }
    contentString = contentString + '</div>';
    return contentString;

}

function predictedMap() {

    var def_lat = 37;
    var def_lng = -50;
// Create the initial InfoWindow.
    var infoWindow = new google.maps.InfoWindow(
        {content: 'Click the map to get local predictions for new cases', position: {lat:37,lng:-50}});
    infoWindow.open(basic_map);

    var cityCircle = new google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: basic_map,
        center:  {lat:37,lng:-50},
        radius: 0
    });
     load_predictions();
	
  $(document).ready(function() {
        $('#myRange').change(function() {
            var radius = document.getElementById("myRange").valueAsNumber;
            document.getElementById("rangeLabel").innerText = "Radius: " + document.getElementById("myRange").value+" mi";
            get_pred(def_lat,def_lng);
            var contentString = updatePredCirc();

            cityCircle.setRadius(1609.3*radius);   //radius of 100 miles
            cityCircle.setCenter({lat:def_lat,lng:def_lng});

            infoWindow.close();
            infoWindow = new google.maps.InfoWindow({position: {lat:def_lat,lng:def_lng}});
            infoWindow.setContent(contentString);
            infoWindow.open(basic_map);
        });
    });


        basic_map.addListener('click', function(mapsMouseEvent)
        {

            var radius = document.getElementById("myRange").valueAsNumber;

            var lat_lng_s = mapsMouseEvent.latLng.toString();
            lat_lng_s = lat_lng_s.slice(1,-1);
            pos = lat_lng_s.indexOf(',');
            var lat = parseFloat(lat_lng_s.substring(0,pos-1));
            var lng = parseFloat(lat_lng_s.substring(pos+1));
            def_lat = lat;
            def_lng = lng;
            get_pred(lat,lng);

            var contentString = updatePredCirc();

            cityCircle.setRadius(1609.3*radius);   //radius of 100 miles
            cityCircle.setCenter(mapsMouseEvent.latLng);

            infoWindow.close();
            infoWindow = new google.maps.InfoWindow({position: mapsMouseEvent.latLng});
            infoWindow.setContent(contentString);
            infoWindow.open(basic_map);
        });


}

function violationMap() {
    
    var reportsRef = firebase.database().ref('reports');
    markers=[]
    reportsRef.on('value', function(e) {
    	e.forEach(function(ce) {
    		var reportData = ce.val();
		    var lat = reportData['lat'];
		    var lng = reportData['long'];
		    var violation = reportData['viol_type'];
		    var city = reportData['city'];
		    var state = reportData['state'];
		    var location = city+", "+ state;
		    var time = reportData['time'];
		    var address = reportData['address']
		    var full_address = address + ", " + location;

		    var contentString = '<div id="content">'+
		        '<div id="siteNotice">'+
		        '</div>'+
		        '<h1 id="firstHeading" class="firstHeading">' + location + '</h1>'+
		        '<div id="bodyContent">'+
		        '<p><b>Violation:</b> ' +violation + '<br />' +
		        '<b>Time:</b> '+ time + '<br />' +
		        '<b>Address:</b> '+full_address+ '<br />' +
		        '</p>'+
		        '</div>'+
		        '</div>';

		    var infowindow = new google.maps.InfoWindow({
		        content: contentString
		    });

		    var marker = new google.maps.Marker({
		        position: {lat:lat,lng:lng},
		        map: basic_map,
		        title: ''
		    });
		    markers.push(marker);
		    marker.addListener('click', function() {
		        infowindow.open(map, marker);
		    });
    	});
    });
}


function parse_csv(text) {
    var count = (text.match(/n/g) || []).length;

    var data = new Array(count);
    var pos = 0;
    var tpos=0;
    for(var c=0; c< count;c++){
        pos = text.indexOf('n');
        var temp = text.slice(0,pos-1);

        tpos = temp.indexOf(',');
        var lat = parseFloat(temp.slice(0,tpos));
        temp = temp.substr(tpos+1);

        tpos = temp.indexOf(',');
        var lng = parseFloat(temp.slice(0,tpos));
        temp = temp.substr(tpos+1);

        var n = parseInt(temp);
        var group = [lat,lng,n];
        data[c] = group;
        text = text.substr(pos+1);
    }
    return data;
}

function spreadMap() {
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", "data.csv", false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                var lat_long_freq = parse_csv(allText);
                var plot_points = [];
                for(var i = 0; i < lat_long_freq.length; i++){
                    var lat = lat_long_freq[i][0];
                    var long = lat_long_freq[i][1];
                    var count = lat_long_freq[i][2];
                    for(var c = 0; c < count; c++){
                        plot_points.push(new google.maps.LatLng(lat,long));
                    }
                }
                if(heatmap != null) {
                    heatmap.setMap(null);
                }
                heatmap = new google.maps.visualization.HeatmapLayer({
                    data: plot_points,
                    map: basic_map
                });
            }
        }
    }
    rawFile.send(null);
}

