function specification(data) {
    var routeStepView = document.getElementById('route_step_view');
    var routeHTML = '';
    for (var i = 0; i < data['way'].length; i++) {
        if (i + 1 < data['way'].length) {
            routeHTML +=
                '<div class="route-step-view__details-axis-layout">' +
                    '<div class="route-step-view__details-axis"></div>' +
                        '<div class="route-step-view__item _clickable">' +
                            '<div class="route-step-view__icon _empty" style="margin-left: 2px;"></div>' +
                            '<div class="route-step-view__title">' +
                                data['way'][i]['name'] +
                            '</div>' +
                        '</div>' +
                        '<div class="route-step-view__details">' +
                            '<div class="route-step-view__details-info">' +
                                '<div class="route-step-view__details-info-right-content">' +
                                    'Скорость судна: ' + uzl_to_km_h(data['ship_speed'].speed_in_ballast) + ' км/ч' +
                                '</div><br>' +
                                '<div class="route-step-view__details-info-right-content">' +
                                    'Время в пути: ' + calc_time(data['way'][i]['dist'], data['ship_speed'].speed_in_ballast) +
                                '</div>' +
                                '<div class="route-step-view__details-info-left-content">' +
                                    km_to_mi(data['way'][i]['dist']) + ' миль' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>';
        } else {
            routeHTML +=
                '<div class="route-step-view__item _clickable">' +
                    '<div class="route-step-view__icon _empty" style="margin-left: 2px;"></div>' +
                    '<div class="route-step-view__title">' + data['way'][i]['name'] + '</div>' +
                '</div>';
        }
    }

    var img1 = document.getElementById('img1');
    var img2 = document.getElementById('img2');
    img1.src = '/static/img/way_screen/' + data['img_name'];
    img2.src = '/static/img/way_screen/' + data['way'][data['way'].length - 1]['id'] + '_' + data['way'][0]['id'] + '.png' ;
    img1.alt = data['way'][data['way'].length - 1]['name'] + ' -> ' + data['way'][0]['name'];
    img2.alt = data['way'][0]['name'] + ' -> ' + data['way'][data['way'].length - 1]['name'];
    routeStepView.innerHTML = routeHTML;
}

function km_to_mi(dist) {
    dist = dist * 0.621371192;
    return dist.toPrecision(6);
}

function uzl_to_km_h(speed) {
    speed = speed * 1.85200;
    return speed.toPrecision(5);
}

function calc_time(dist, speed) {
    var _time = dist / uzl_to_km_h(speed);
    var days = Math.floor(_time / 24);
    if (days > 0) {
        _time -= days * 24;
        return days + 'д ' + _time.toPrecision(5) + ' час(-ов)';
    }
    return _time.toPrecision(4) + ' час(-ов)';
}
