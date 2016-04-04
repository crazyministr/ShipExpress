var map;

$(function() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&language=en&sensor=false&callback=init';
    document.body.appendChild(script);


    /* Fullscreen START */
    var fullScreenApi = {
            supportsFullScreen: false,
            isFullScreen: function() { return false; },
            requestFullScreen: function() {},
            cancelFullScreen: function() {},
            fullScreenEventName: '',
            prefix: ''
        },
        browserPrefixes = 'webkit moz o ms khtml'.split(' ');

    // check for native support
    if (typeof document.cancelFullScreen != 'undefined') {
        fullScreenApi.supportsFullScreen = true;
    } else {
        // check for fullscreen support by vendor prefix
        for (var i = 0, il = browserPrefixes.length; i < il; i++ ) {
            fullScreenApi.prefix = browserPrefixes[i];
            if (typeof document[fullScreenApi.prefix + 'CancelFullScreen' ] != 'undefined' ) {
                fullScreenApi.supportsFullScreen = true;
                break;
            }
        }
    }

    // update methods to do something useful
    if (fullScreenApi.supportsFullScreen) {
        fullScreenApi.fullScreenEventName = fullScreenApi.prefix + 'fullscreenchange';
        fullScreenApi.isFullScreen = function() {
            switch (this.prefix) {
                case '':
                    return document.fullScreen;
                case 'webkit':
                    return document.webkitIsFullScreen;
                default:
                    return document[this.prefix + 'FullScreen'];
            }
        };
        fullScreenApi.requestFullScreen = function() {
            return (this.prefix === '') ? document.body.requestFullScreen() : document.body[this.prefix + 'RequestFullScreen']();
        };
        fullScreenApi.cancelFullScreen = function() {
            return (this.prefix === '') ? document.cancelFullScreen() : document[this.prefix + 'CancelFullScreen']();
        }
    }


    $.fn.requestFullScreen = function() {
        return this.each(function() {
            if (fullScreenApi.supportsFullScreen) {
                fullScreenApi.requestFullScreen($('body'));
            }
        });
    };

    // export api
    window.fullScreenApi = fullScreenApi;

    /* Fullscreen END */

});


function init() {

    google.maps.visualRefresh = true;

    map = new google.maps.Map(document.getElementById("map_canvas"), {
        zoom: 2,
        minZoom: 2,
        maxZoom: 15,
        scrollwheel: true,
        center: new google.maps.LatLng(40, 1),
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


    if (window.fullScreenApi.supportsFullScreen) {

        var fsControlDiv = document.createElement('div');
        fsControlDiv.style.padding = '5px';
        var controlUI = document.createElement('div');
        controlUI.title = 'Full screen';
        fsControlDiv.appendChild(controlUI);

        controlUI.className = 'dropDownControl';
        controlUI.innerHTML = '<div class="icon-arrows-alt icon-screen"></div>';

        google.maps.event.addDomListener(controlUI, 'click', function() {
            if (window.fullScreenApi.isFullScreen()) {
                window.fullScreenApi.cancelFullScreen();
            } else {
                window.fullScreenApi.requestFullScreen();
            }
        });

        fsControlDiv.index = 1;
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(fsControlDiv);
    }

    init_module();

}

$(document)
    .on("mouseover", ".port_label", function () {
        $(this).css('z-index', '999').css('background-color', 'rgba(255, 255, 255, 1)').find('.pl_more').css('display', 'block');
    })
    .on("click", ".port_label", function () {
        if ($(this).hasClass('pressed')) $(this).removeClass('pressed');
        else $(this).addClass('pressed');

        $(this).css('z-index', '999').find('.pl_more').css('display', 'block');
    })
    .on("mouseleave", ".port_label:not(.pressed)", function () {
        $(this).css('z-index', '50').css('background-color', 'rgba(255, 255, 255, 0.9)').find('.pl_more').hide(200);
    })
    .on("click", ".b_toggle", function () {
        var sel = $(this).next();
        if(sel.is(":visible")){
            $(this).find('i').removeAttr('class').addClass('icon-chevron-left');
            sel.hide(300);
        }else{
            $(this).find('i').removeAttr('class').addClass('icon-chevron-right');
            sel.show(300);
        }
    })
;


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
