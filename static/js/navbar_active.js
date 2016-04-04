$(document).ready(function() {
    var url = window.location.href;
    var li = url.split('/');
    $('#' + li[li.length - 2] + '_li').addClass('active');
});
