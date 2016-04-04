var gMap;
var gPolyline = [];
var markers = [];
var changeOffset;
var animateCircle;
var bounds;

$(function() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&language=en&sensor=false&callback=init';
    document.body.appendChild(script);
});

function init() {
    gMap = new google.maps.Map(document.getElementById("map"), {
        zoom: 3,
        minZoom: 2,
        maxZoom: 15,
        scrollwheel: true,
        center: new google.maps.LatLng(73.0, 110.0),
        styles: [
            {
                "featureType": "water",
                "stylers": [{"visibility": "simplified"}]
            },{
                "featureType": "administrative",
                "stylers": [{"lightness": 40}, {"weight": 0.2}]
            },{
                "featureType": "landscape",
                "stylers": [{"lightness": 65}]
            },{
                "featureType": "administrative",
                "elementType": "geometry.fill",
                "stylers": [
                    { "visibility": "off" }
                ]
            }
        ],
        panControl: true,
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        overviewMapControl: false,
        backgroundColor: '#fff',
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    Label.prototype = new google.maps.OverlayView;
    Label.prototype.onAdd = function() {
        var pane = this.getPanes().overlayImage;
        pane.appendChild(this.div_);
    };
    Label.prototype.draw = function() {
        var projection = this.getProjection();
        var position = projection.fromLatLngToDivPixel(this.get('position'));
        var div = this.div_;
        div.style.left = position.x + 'px';
        div.style.top = position.y + 'px';
        div.style.display = 'block';
        //div.style.zIndex = this.get('z-index');
        this.ddiv_.innerHTML = this.get('text').toString();
        $('.port_label').removeClass('pressed').css('background-color', 'rgba(255, 255, 255, 0.9)');
    };

}

function Label(opt_options, cl_name) {
    // Initialization
    this.setValues(opt_options);

    // Here go the label styles
    var ddiv = this.ddiv_ = document.createElement('div');
    ddiv.className = cl_name || 'port_label';
    ddiv.setAttribute('onclick', '');

    var div = this.div_ = document.createElement('div');
    div.appendChild(ddiv);
    div.style.cssText = 'position: absolute; display: none';
}

function clearMap() {
    clearInterval(changeOffset);

    if (animateCircle)
        animateCircle.setMap(null);

    $.each(markers, function(num, marker) {
        marker.setMap(null);
    });

    $.each(gPolyline, function(num, polyline) {
        polyline.setMap(null);
    });

    gPolyline = [];
    markers = [];
    bounds = new google.maps.LatLngBounds();
    google.maps.event.trigger(gMap, 'click'); // hide infoWindows
}

function drawRoute(data) {
    clearMap();

    for (var i = 0; i < data['way'].length; i++) {
        var portName = data['way'][i]['name'];
        var coords = data['way'][i]['coords'];
        var required = data['way'][i]['required'];
        var latLng = new google.maps.LatLng(coords[0], coords[1]);
        markers.push(new google.maps.Marker({
            position: latLng,
            title: portName,
            info: {
                title: portName,
                coords: coords,
                id: data['way'][i]['id']
            }
        }));
        if (i + 1 < data['way'].length) {
            var path = data['way'][i]['path'];
            var polyline = [latLng];
            for (var j = 0; j < path.length; j++) {
                polyline.push(new google.maps.LatLng(path[j][0], path[j][1]));
            }
            var nextPortCoords = data['way'][i + 1]['coords'];
            polyline.push(new google.maps.LatLng(nextPortCoords[0], nextPortCoords[1]));
            gPolyline.push(new google.maps.Polyline({
                path: polyline,
                info: {
                    from: portName,
                    to: data['way'][i + 1]['name'],
                    dist: data['way'][i]['dist']
                },
                strokeColor: '#3dcd1c',
                strokeWeight: 4,
                clickable: true,
                strokeOpacity: 1
            }));
        }
    }
    addMarkers();
    addPolyline();
    //createAnimateCircle();
}

function addMarkers() {
    var infoWindow = new google.maps.InfoWindow();
    $.each(markers, function(num, marker) {
        marker.setIcon({
            url: '/static/img/port_icon.png',
            size: new google.maps.Size(20, 20),
            scaledSize: new google.maps.Size(20, 20),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(10, 10)
        });

        marker.setMap(gMap);
        var content =
            '<div>' +
                '<div>' +
                    '<a href="/ports/' + marker.info.id + '">' + marker.info.title + '</a>' +
                '</div>' +
                '<div>' +
                    '<span class="glyphicon glyphicon-globe" aria-hidden="true"> ' +
                        marker.info.coords +
                    '</span> ' +
                '</div>' +
            '</div>';

        var label = new Label({ map: gMap });
        label.bindTo('position', marker, 'position');

        label.set('text', '<span style="border: solid 1px black;">' + marker.title + '</span>');

        google.maps.event.addListener(marker, 'click', function() {
            gMap.setCenter(marker.getPosition());
            infoWindow.setContent(content);
            infoWindow.open(gMap, marker);
        });
    });
    google.maps.event.addListener(gMap, "click", function () {
        infoWindow.close();
    });
}

function createAnimateCircle() {
    var fullPath = [];
    $.each(gPolyline, function(num, polyline) {
        var path = polyline.getPath()['j'];
        $.each(path, function(i, coords) {
            fullPath.push(coords);
            bounds.extend(coords);
        });
    });
    gMap.fitBounds(bounds);

    animateCircle = new google.maps.Polyline({
        path: fullPath,
        icons: [{
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 2.4,
                strokeColor: 'red',
                fillColor: 'greed',
                fillOpacity: 1
            },
            offset: '0%'
        }],
        strokeColor: "#fff",
        strokeWeight: 0,
        map: gMap
    });
    var count = 0;
    changeOffset = window.setInterval(function() {
        count = (count + 1) % 400;
        var icons = animateCircle.get('icons');
        icons[0].offset = (count / 4) + '%';
        animateCircle.set('icons', icons);
        if (count >= 400)
            count = 0;
    }, 50);
}

function addPolyline() {
    var infoWindow = new google.maps.InfoWindow();
    $.each(gPolyline, function(num, polyline) {
        polyline.setMap(gMap);
        var content =
            '<div>' +
                '<div>' +
                    polyline.info.from +
                    '<span class="glyphicon glyphicon-menu-right" aria-hidden="true"></span>' +
                    polyline.info.to + '</div>' +
                '<div>Расстояние: ' + polyline.info.dist + ' km</div>' +
            '</div>';

        google.maps.event.addListener(polyline, 'click', function(e) {
            var point = e.latLng;
            infoWindow.setContent(content);
            infoWindow.setPosition(point);
            infoWindow.open(gMap);
        });
        google.maps.event.addListener(polyline, 'mouseover', function(){
            polyline.setOptions({'strokeWeight': 6 });
        });
        google.maps.event.addListener(polyline, 'mouseout', function(){
            polyline.setOptions({'strokeWeight': 3 });
        });
    });

    google.maps.event.addListener(gMap, "click", function () {
        infoWindow.close();
    });
}
