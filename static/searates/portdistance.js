var bounds,
    geocoder,
    xhr,
    offsetId,
    directions = [],
    markers = {},
    lineEvents = {},
    markers_old = [],
    line =  {A: [], B: [], C: [], total: []},
    chart = {}, Time = {}, App = {},
    polyline = {A: [], B: [], C: []};

paceOptions = {
    ajax: {
        trackMethods: ['POST'],
        ignoreURLs: ['/port-list', '/explorer/traffic-history']
    },
    startOnPageLoad: false
}

function init_module() {

    tbl = new Table();
    geocoder = new google.maps.Geocoder();
    /* Reset Button*/
    var resetDiv = document.createElement('div');
    resetDiv.style.padding = '5px';
    var resetUI = document.createElement('div');
    resetUI.title = 'Reset bounds';
    resetUI.className = 'dropDownControl';
    resetUI.innerHTML = '<div class="icon-photo icon-screen"></div>';
    resetDiv.appendChild(resetUI);
    google.maps.event.addDomListener(resetUI, 'click', function() {
        if(bounds) map.fitBounds(bounds);
        else{
            map.setZoom(2);
        }
    });
    resetDiv.index = 2;
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(resetDiv);
    google.maps.event.addListener(map, 'zoom_changed', function() {
        var sel = $('.city_map');
        map.getZoom() > 5 ? sel.show() : sel.hide();
    });
    /*Settings Button*/
    var fsCogsDiv = document.createElement('div');
    fsCogsDiv.style.padding = '5px';
    var cogsUI = document.createElement('div');
    cogsUI.title = 'Settings';
    fsCogsDiv.appendChild(cogsUI);
    cogsUI.className = 'dropDownControl';
    cogsUI.innerHTML = 'Settings';
    google.maps.event.addDomListener(cogsUI, 'click', function() {
        $('#cog_form').toggle();
    });
    fsCogsDiv.index = 3;
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(fsCogsDiv);
    $(document)
        .on('click', '#li-A', function(){ lineEvents.A(); })
        .on('click', '#li-B', function(){ lineEvents.B(); })
        .on('click', '#li-C', function(){ lineEvents.C(); })
        .on('mouseover', '#li-A', function(){ line.A.setOptions({'strokeWeight': 6 }); })
        .on('mouseover', '#li-B', function(){ line.B.setOptions({'strokeWeight': 6 }); })
        .on('mouseover', '#li-C', function(){ line.C.setOptions({'strokeWeight': 6 }); })
        .on('mouseout', '#li-A', function(){ line.A.setOptions({'strokeWeight': 3 }); })
        .on('mouseout', '#li-B', function(){ line.B.setOptions({'strokeWeight': 3 }); })
        .on('mouseout', '#li-C', function(){ line.C.setOptions({'strokeWeight': 3 }); })
    ;

    /*
        @nick 14-01-2015
    */

    $( ".b-chart").draggable({ containment: "#map_canvas", scroll: false });
    $('.info-container').on('click', '#showChart', function(){
        if (chart.points[0] != parseInt($('#port_a').val()) && chart.points[1] != parseInt($('#port_b').val())) {
            $('#info-container-5').html(
                '<div class="chart-center-data"><i class="icon icon-circle-o-notch icon-spin"></i> loading</div></div>'
            );
            $.post('/explorer/explorer/traffic-history', 'pointA=' + $('#port_a').val() + '&pointB=' + $('#port_b').val(), function(data){
                if (data && data.history) {
                    chart.set(data.history);
                    chart.append();
                } else {
                    $('#info-container-5').html('<div class="chart-center-data">No data</div>');
                }
                chart.points = [$('#port_a').val(), $('#port_b').val()];
            });
        }
        $('.b-chart').toggle();
    });
    $('.b-chart .close').click(function(){
        $('.b-chart').hide();
    });
    chart = {
        data: [],
        points: [0, 0],
        set: function(traffic){
            this.data = traffic;
        },
        append: function(){
            if (this.data && this.data.length > 0) {
                var date = {},
                    line = {},
                    series = [],
                    DDSD = {},
                    drilldownSeries = [],
                    index = {},
                    locNms = '';
                $.each(this.data, function(key, row){
                    if (row.ports != null) {
                        index.a = row.ports.lastIndexOf(parseInt($('#port_a').val()));
                        index.b = $.inArray(parseInt($('#port_b').val()), row.ports);
                        date.a = new Date(row.dates[index.a].split(' ')[0]);
                        date.b = new Date(row.dates[index.b].split(' ')[0]);
                        if (date.a < date.b && index.a < index.b) {
                            var estimatedTm, currentTm, i, isNormalTm = false;
                            estimatedTm = Math.round(Time.ofSeaDistance()/60/60/24);
                            currentTm = Math.round((date.b - date.a)/1000/60/60/24);
                            i = Math.round(currentTm * 100/estimatedTm);

                            if (i >= 100 && i <= 300) {
                                isNormalTm = true;
                            } else if (i <= 100 && i >= 50) {
                                isNormalTm = true;
                            }

                            if (isNormalTm) {
                                if (row.names.length > 2 && index.b - index.a > 1) {
                                    var names = row.names.slice(index.a +1, index.b);
                                    var ports = [];
                                    $.each(names, function(i, location){
                                        if (i != 0) {
                                            if (location != names[i -1]) {
                                                ports.push(location);
                                            }
                                        } else {
                                            ports.push(location);
                                        }
                                    });
                                    locNms = 'POT: ' + ports.join(', ');
                                } else {
                                    locNms = 'POT undefined';
                                }
                                if (!DDSD[row.name]) {
                                    DDSD[row.name] = [];
                                }
                                DDSD[row.name].push([
                                    row.number + '<br>' + locNms + '<br>' + date.b.toLocaleDateString('en-US'),
                                    currentTm
                                ]);
                                if (!line[row.name]) {
                                    line[row.name] = {
                                        drilldown: row.id_sealine,
                                        name: row.name
                                    };
                                }
                            }
                        }
                    }
                });
                for (var Nm in DDSD) {
                    if (DDSD[Nm].length <= 1) {
                        delete line[Nm];
                    }
                    DDSD[Nm] = DDSD[Nm].reverse().slice(0, 10);
                }
                if (Object.keys(line).length > 0) {
                    $.each(line, function(name, item){
                        var total = 0;
                        $.each(DDSD[name], function(i, container){
                            total += parseInt(container[1]);
                        });
                        line[name].y = Math.round(total/DDSD[name].length);
                        series.push(line[name]);
                        drilldownSeries.push({id: item.drilldown, name: name, data: DDSD[name]});
                    });
                    $('#info-container-5').highcharts({
                        chart: {
                            type: 'column'
                        },
                        title: {
                            text: 'Actual Transit Time: ' + markers.B.city_name + ' - ' + markers.C.city_name
                        },
                        xAxis: {
                            type: 'category',
                            labels: {
                                enabled: false,
                                rotation: 0,
                                style: {
                                    fontSize: '6px',
                                    fontWeight: 'normal'
                                }
                            }
                        },
                        yAxis: {
                            title: {
                                text: 'Transit Time (days)'
                            }
                        },
                        legend: {
                            enabled: false
                        },
                        plotOptions: {
                            series: {
                                borderWidth: 0,
                                dataLabels: {
                                    enabled: true,
                                    format: '{point.y}'
                                }
                            }
                        },
                        tooltip: {
                            headerFormat: '',
                            pointFormat: '{point.name}',
                            backgroundColor: '#fff',
                            borderWidth: 0
                        },
                        series: [{
                            name: 'Lines',
                            colorByPoint: true,
                            data: series
                        }],
                        drilldown: {
                            series: drilldownSeries
                        }
                    });

                } else {
                    $('#info-container-5').html('<div class="chart-center-data">No data</div>');
                }
            } else {
                $('#info-container-5').html('<div class="chart-center-data">No data</div>');
            }
        }
    };
    Time = {
        ofSeaDistance: function(toText){
            var path, time = 24, speed = 14;
            path = Math.round(App.distance/1.852);// км в мили. получили 2187 nm вместо 2162 nm
            time += path/speed;
            var sec = Math.floor(time*60*60);
            return toText ? this.toText(sec) : sec;
        }
    };

    /**/

}


$(function() {

    $("#cog_form").draggable({ containment: "#map_canvas", scroll: false, cancel: 'table, select' });
    $("#place_a, #place_d").autocomplete({
        source: function(request, response) {

            var point = $(this.element).data('point');

            geocoder.geocode({
                'address': request.term
            }, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    response($.map(results, function(item) {
                        return {
                            address_components: item.address_components,
                            label: item.formatted_address,
                            value: item.formatted_address,
                            latitude: item.geometry.location.lat(),
                            longitude: item.geometry.location.lng(),
                            point: point
                        };
                    }));
                }
            });
        },
        messages: {
            noResults: '',
            results: function() {}
        },
        change:function() {
            if(!$("#place_a").val()){
                markers_old.push(markers.A);
                delete markers.A;
            }
            if(!$("#place_d").val()){
                markers_old.push(markers.D);
                delete markers.D;
            }
        },
        select: function(event, ui) {

            var a_c = ui.item.address_components;

            var country = a_c[a_c.length - 1];
            for (var i in a_c) {
                if($.inArray('country', a_c[i]['types']) != -1 && $.inArray('political', a_c[i]['types']) != -1) country = a_c[i];
            }

            if(markers[ui.item.point]) markers_old.push(markers[ui.item.point]);
            markers[ui.item.point] = new google.maps.Marker({
                position: new google.maps.LatLng(ui.item.latitude, ui.item.longitude),
                city_name: a_c[0].long_name,
                country_name: country.long_name,
                country_code: country.short_name,
                optimized: false
            });
        }
    });


    $('.select_country').on('change', function(){

        var c = $(this);
        var p = c.parent().next().find('select');
        var cval = c.val();

        if(cval) {
            p.attr('disabled', true).html("<option>loading...</option>");
            $.ajax({
                type: "post",
                url: "/port/port-list",
                data: { c: cval },

                success : function(r) {
                    var t="";
                    $.each(r.ports, function(i,item) {
                        t += "<option value='"+item.id+"'>"+item.name+"</option>";
                    });
                    p.html(t).removeAttr("disabled");
                }
            });
        }else{
            p.attr('disabled', true).html("<option>select port</option>");
        }
    });


});




getPath = function() {

    clear_map();

    delete markers.B;
    delete markers.C;

    var portB = $('#port_a').val();
    var portC = $('#port_b').val();

    var nameB = $( "#port_a option:selected" ).text();
    var countryNameB = $("#place_b_country option:selected").text();
    var countryCodeB =  $("#place_b_country").val();

    var nameC = $( "#port_b option:selected" ).text();
    var countryNameC = $("#place_c_country option:selected").text();
    var countryCodeC =  $("#place_c_country").val();

    polyline = {A: [], B: [], C: []};

    tbl.clear();

    bounds = new google.maps.LatLngBounds();

    if(portB != 0 && portC != 0 && portB == portC){

        alert('Ports should not match.');

    }else if((!markers.A || !markers.D) && portB == 0 && portC == 0){

        alert('Please enter at least 2 points.');

    }else if(markers.A && markers.D && portB == 0 && portC == 0){

        tbl.directionsIter++;

        var directionsService = new google.maps.DirectionsService();
        directionsService.route({
            origin: markers.A.getPosition(),
            destination: markers.D.getPosition(),
            travelMode: google.maps.TravelMode.WALKING
        }, function (result, status) {
            if (status == google.maps.DirectionsStatus.OK) {

                tbl.directionsIterSuccess++;

                $.each(result.routes[0].overview_path, function(i, item) { polyline.A.push(item); });

                var distance = result.routes[0].legs[0].distance.value;
                var duration = distance / (Number($('#speed_truck').val()) * 0.277778);

                tbl.found({distance: distance, duration: duration, segment: 'A'});
                result_show(false);

            }else{
                tbl.directionsIterSuccess++;
                result_show(false);
            }
        });

        set_markers(markers);

    }else{

        if(xhr && xhr.readystate != 4) xhr.abort();
        xhr = $.ajax({
            type: "post",
            url: "/port/port-to-port",
            data: { port_a: portB, port_b: portC },
            success: function(result) {

                // @nick 14-01-2015
                App.distance = Math.round(parseInt(result.dist));

                if(result.path.length > 0){
                    for(var i in result.path){
                        if(result.path[i][0] != null && result.path[i][1] != null){

                            var LatLng = new google.maps.LatLng(result.path[i][0], result.path[i][1]);
                            polyline.B.push(LatLng);
                            bounds.extend(LatLng);

                            if(i==0 || i==result.path.length-1){

                                if(i==0){
                                    markers.B = new google.maps.Marker({
                                        position: LatLng,
                                        city_name: nameB,
                                        country_name: countryNameB,
                                        country_code: countryCodeB,
                                        optimized: false
                                    });

                                    if(markers.A){

                                        tbl.directionsIter++;

                                        var directionsServiceA = new google.maps.DirectionsService();
                                        directionsServiceA.route({
                                            origin: markers.A.getPosition(),
                                            destination: LatLng,
                                            travelMode: google.maps.TravelMode.WALKING
                                        }, function (result, status) {
                                            if (status == google.maps.DirectionsStatus.OK) {

                                                tbl.directionsIterSuccess++;

                                                $.each(result.routes[0].overview_path, function(i, item) { polyline.A.push(item); });

                                                var distance = result.routes[0].legs[0].distance.value;
                                                var duration = distance / (Number($('#speed_truck').val()) * 0.277778);

                                                tbl.found({distance: distance, duration: duration, segment: 'A'});
                                                result_show();
                                            }else{
                                                tbl.directionsIterSuccess++;
                                                result_show();
                                            }
                                        });

                                    }


                                }else{
                                    markers.C = new google.maps.Marker({
                                        position: LatLng,
                                        city_name: nameC,
                                        country_name: countryNameC,
                                        country_code: countryCodeC,
                                        optimized: false
                                    });

                                    if(markers.D){

                                        tbl.directionsIter++;

                                        var directionsServiceD = new google.maps.DirectionsService();
                                        directionsServiceD.route({
                                            origin: LatLng,
                                            destination: markers.D.getPosition(),
                                            travelMode: google.maps.TravelMode.WALKING
                                        }, function (result, status) {
                                            if (status == google.maps.DirectionsStatus.OK) {

                                                tbl.directionsIterSuccess++;

                                                $.each(result.routes[0].overview_path, function(i, item) { polyline.C.push(item); });

                                                var distance = result.routes[0].legs[0].distance.value;
                                                var duration = distance / (Number($('#speed_truck').val()) * 0.277778);

                                                tbl.found({distance: distance, duration: duration, segment: 'C'});
                                                result_show();
                                            }else{
                                                tbl.directionsIterSuccess++;
                                                result_show();
                                            }
                                        });

                                    }
                                }

                            }
                        }
                    }

                    var distance = result.dist * 1000;
                    var duration = distance / 0.514444 / Number($('#speed').val());

                    tbl.found({distance: distance, duration: duration, segment: 'B'});
                    result_show();

                    set_markers(markers);
                }else{
                    alert('Not Found.');
                }
            }
        });
    }

};

function set_markers(markers){
    $.each(markers, function (m, marker) {

        marker.setIcon({
            url: m == 'A' ? '/images/marker-gr.png?v2' : (m == 'D' ? '/images/marker-yel.png?v2' : '/images/marker-blue.png?v2'),
            size: new google.maps.Size(20, 20),
            scaledSize: new google.maps.Size(20, 20),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(10, 10)
        });
        marker.setMap(map);

        google.maps.event.addListener(marker, 'click', function() {
            var z = map.getZoom();
            z = z < 7 ? 7 : z+1;
            map.setZoom(z);
            map.setCenter(marker.getPosition());
        });

        var label = new Label({ map: map });
        label.bindTo('position', marker, 'position');

        label.set('text', '<span title="' + marker.country_name + '"><span class="flag-icon-small flag-align-middle flag-icon-small-' + marker.country_code.toLowerCase() + '"></span></span> ' + marker.city_name +
            '<span class="pl_more"><hr>' + '<span class="w_prop">Country:</span> ' + marker.country_name + '</span>');

        bounds.extend(marker.getPosition());

    });

    bounds.extend(new google.maps.LatLng(bounds.getNorthEast().lat(), bounds.getNorthEast().lng() + 20));
    map.fitBounds(bounds, { padding: [10, 200] });
}

function Table() {}

Table.prototype.option = []; //m , s
Table.prototype.directionsIter = 0;
Table.prototype.directionsIterSuccess = 0;

Table.prototype.found = function(arr) {
    this.option.push(arr);
    this.option.sort(function(a,b){
        var nameA=a.segment.toLowerCase(), nameB=b.segment.toLowerCase();
        if (nameA < nameB) return -1;
        if (nameA > nameB) return 1;
        return 0;
    });
};

Table.prototype.clear = function() {
    this.option = [];
};

Table.prototype.isReceived = function() {
    return this.directionsIter == this.directionsIterSuccess;
};

function result_show(showTitle){

    if(tbl.isReceived()){
        var totalDistance = 0,
            totalDuration = 0,
            info = '',
            percentage = {A: 0, B: 0, C: 0},
            infoWindow = new google.maps.InfoWindow(),
            titles = {A: 'Door to Port', B: 'Port to Port', C: 'Port to Door'},
            color = {A: '#3dcd1c', B: '#008CDC', C: '#f0ad4e'};

        $.each(tbl.option, function (k, opt) {
            totalDistance = totalDistance + opt.distance;
            totalDuration = totalDuration + opt.duration;
        });

        $.each(tbl.option, function (k, opt) {
            percentage[opt.segment] = Math.round((opt.distance/totalDistance)*100);
        });

        $.each(tbl.option, function (k, opt) {

            var s = opt.segment;

            line[s] = new google.maps.Polyline({
                path: polyline[s],
                strokeColor: color[s],
                strokeWeight: 3,
                clickable: true,
                strokeOpacity: 1,
                map: map
            });

            var curDist = (opt.distance / 1000).toFixed(2) + 'km';
            var curDur = Math.floor(opt.duration / 86400) +' days(s) ' + Math.floor(opt.duration / 3600) % 24 + ' hours';

            info +=
                '<li><a href="javascript:void(0);" id="li-' + s + '" >';

            if(showTitle) info +=
                '<div class="clearfix">' +
                    '<span class="pull-left">' + titles[s] + '</span>' +
                    '<span class="pull-right">' + percentage[s] + '%</span>' +
                    '</div>';

            info += '<div class="progress progress-mini progress-striped">' +
                '<div class="progress-bar" style="width:' + percentage.A + '%;' + (s=='A' ? ' background-color: ' + color[s] + ';': '') + '"></div>' +
                '<div class="progress-bar" style="width:' + percentage.B + '%;' + (s=='B' ? ' background-color: ' + color[s] + ';': '') + '"></div>' +
                '<div class="progress-bar" style="width:' + percentage.C + '%;' + (s=='C' ? ' background-color: ' + color[s] + ';': '') + '"></div>' +
                '</div>' +

                '<div class="clearfix">' +
                '<span class="pull-left" style="color: #777">Distance: </span>' +
                '<span class="pull-right">' + curDist + '</span>' +
                '</div>' +

                '<div class="clearfix">' +
                '<span class="pull-left" style="color: #777">Transit Time: </span>' +
                '<span class="pull-right">' + curDur + '</span>' +
                '</div>' +

                '</a><hr/></li>';


            var content = '<div style="line-height:1.35;overflow:hidden;white-space:nowrap;">' +
                '<div style="font-weight: 400;">' + titles[s] + '</div>' +
                '<div>Distance: <span>'+ curDist +'</span></div>' +
                '<div>Transit Time: <span>'+ curDur + '</span></div>' +
                '</div>';

            lineEvents[s] = function(e){
                var middlePoint = parseInt(Math.round(line[s].getPath().length / 2)),
                    point;
                if (e) {
                    point = e.latLng;
                }else{
                    var bounds = new google.maps.LatLngBounds();
                    line[s].getPath().forEach(function(e, ind){
                        if(ind == middlePoint) point = e;
                        bounds.extend(e);
                    });
                    map.fitBounds(bounds);
                }

                infoWindow.setContent(content);
                infoWindow.setPosition(point);
                infoWindow.open(map);
            };

            google.maps.event.addListener(line[s], 'click', lineEvents[s]);
            google.maps.event.addListener(line[s], 'mouseover', function(){
                line[s].setOptions({'strokeWeight': 6 });
            });
            google.maps.event.addListener(line[s], 'mouseout', function(){
                line[s].setOptions({'strokeWeight': 3 });
            });

        });

        google.maps.event.addListener(map, "click", function () {
            infoWindow.close();
        });


        line.total = new google.maps.Polyline({
            path: polyline.A.concat(polyline.B.concat(polyline.C)),
            icons: [{
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 2.4,
                    strokeColor: 'red',
                    fillColor: 'red',
                    fillOpacity: 1
                },
                offset: '0%'
            }],
            strokeColor: "#fff",
            strokeWeight: 0,
            map: map
        });

        var count = 0;
        offsetId = window.setInterval(function() {
            count = (count + 1) % 400;
            var icons = line.total.get('icons');
            icons[0].offset = (count / 4) + '%';
            if(count/4 > 100) count = 0;
            line.total.set('icons', icons);
        }, 50);


        info = '<li><a href="javascript:void(0);" class="cdef">' +
            '<div class="clearfix">' +
            '<span class="pull-left">Total Distance</span>' +
            '<span class="pull-right">100%</span>' +
            '</div>' +

            '<div class="progress progress-mini progress-striped active">' +
            '<div class="progress-bar" style="width:100%; background-color: #d9534f"></div>' +
            '</div>' +

            '<div class="clearfix">' +
            '<span class="pull-left" style="color: #777">Distance: </span>' +
            '<span class="pull-right">' + (totalDistance / 1000).toFixed(2) + ' km</span>' +
            '</div>' +

            '<div class="clearfix">' +

            '<span class="pull-left" style="color: #777">Transit Time: </span>' +
            '<span class="pull-right">' + Math.floor(totalDuration / 86400) +' days(s) ' + Math.floor(totalDuration / 3600) % 24 + ' hours</span>' +
            '</div>' +

            '</a><hr/></li>' +

            info;

        info = '<ul class="dropdown-navbar">' + info + '</ul>';

        // @nick 14-01-2015
        info += '<a class="button29" id="showChart">Show statistics</a>';

        $('.info-container').html(info).show(300);
        $('.info-content').show();
    }

}

function clear_map() {

    // @nick 14-01-2015
    $('#info-container-5').html('<div class="chart-no-data">No data</div>');
    $('.b-chart').hide();
    if (chart) {
        chart.points = [0, 0];
    }

    $('.info-container').html('').hide();
    $('.info-contant, #cog_form').hide();
    $('.port_label').parent().remove();

    google.maps.event.trigger(map, 'click'); //hide infowindows

    $.each(markers, function (m, mrk) {
        if(mrk) mrk.setMap(null);
    });

    $.each(markers_old, function (m, mrk) {
        if(mrk) mrk.setMap(null);
    });

    $.each(directions, function (d, dir) {
        if(dir) dir.setMap(null);
    });

    if (line.total.length !== 0) {
        clearInterval(offsetId);
        line.total.setMap(null);
    }
    if (line.A.length !== 0) line.A.setMap(null);
    if (line.B.length !== 0) line.B.setMap(null);
    if (line.C.length !== 0) line.C.setMap(null);

    line =  {A: [], B: [], C: [], total: []};

    bounds = null;
}
