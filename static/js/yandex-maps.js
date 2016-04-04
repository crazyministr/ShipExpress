var myMap;
var balloons = {};
var SF_PRESET_OPTION = 'islands#nightCircleIcon';
var REQUIRED_PRESET_OPTION = 'islands#lightBlueCircleIcon';
var UNREQUIRED_PRESET_OPTION = 'islands#grayCircleIcon';

ymaps.ready(init);

function init() {
    myMap = new ymaps.Map('map', {
        center: [73.0, 110.0],
        controls: ['fullscreenControl', 'zoomControl'],
        zoom: 3
    });
}

function initMap() {
    myMap.geoObjects.removeAll();
    balloons = {};
}

function drawRoute(data) {
    initMap();
    createSimpleRoute(data);
    //createRoute(data);
    //addCoordsOfTurningPoints(data['ctp']);
}

function createRoute(data) {
    var route = [];
    for (var i = 0; i < data['way'].length; i++) {
        var portName = data['way'][i]['name'];
        var coords = data['way'][i]['coords'];
        route.push(portName);
        route.push({'type': 'wayPoint', point: coords});
    }
    console.log(route);
    ymaps.route(route, {
        mapStateAutoApply: true
    }).then(function(route) {
        console.log(route.getPaths());
        myMap.geoObjects.add(route);
    });
}

function createSimpleRoute(data) {
    for (var i = 0; i < data['way'].length; i++) {
        var portName = data['way'][i]['name'];
        var coords = data['way'][i]['coords'];
        var required = data['way'][i]['required'];

        if (balloons[portName])
            continue;

        var presetOption = UNREQUIRED_PRESET_OPTION;
        if (portName == data['start'] || portName == data['finish'])
            presetOption = SF_PRESET_OPTION;
        else if (required)
            presetOption = REQUIRED_PRESET_OPTION;

        balloons[portName] = new ymaps.Placemark(coords, {
            iconContent: portName,
            hintContent: portName,
            balloonContentHeader: portName,
            balloonContentBody: coords,
            balloonContentFooter: "<a href='#' name='" + portName + "'>подробнее...</a>"
        }, {
            preset: presetOption
        });
        myMap.geoObjects.add(balloons[portName]);
    }
    addEdges(data);
}

function addEdges(data) {
    var num = 1;
    window.setInterval(function() {
        if (num == data['way'].length)
            return;

        var port = data['way'][num];
        var prevPort = data['way'][num - 1];
        var lineGeoObject = new ymaps.GeoObject({
                // Описываем геометрию типа "Ломаная линия".
                geometry: {
                    type: "LineString",
                    coordinates: [
                        prevPort['coords'],
                        port['coords']
                    ]
                },
                // Описываем данные геообъекта.
                properties: {
                    hintContent: prevPort['name'] + ' - ' + port['name'],
                    balloonContentHeader: prevPort['name'] + ' - ' + port['name']
                }
            }, {
                // Включаем отображение в форме геодезических кривых.
                geodesic: true,
                // Задаем ширину в 5 пикселей.
                strokeWidth: 5,
                // Задаем цвет линии.
                strokeColor: "#1e4e88",
                strokeStyle: "shortdash"
            });
        // Добавляем геообъект на карту.
        myMap.geoObjects.add(lineGeoObject);
        num += 1;
    }, 300);
}

function addCoordsOfTurningPoints(ctp) {
    for (var i = 0; i < ctp.length; i++) {
        myMap.geoObjects.add(
            new ymaps.Placemark(ctp[i].coords,
                {},
                {preset: UNREQUIRED_PRESET_OPTION}
            ))
    }
}
