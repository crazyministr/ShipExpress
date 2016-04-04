$(document).ready(function() {
    $('#form').on('submit', function (event) {
        event.preventDefault();
        var data = $(this).serialize();
        var url = $(this).attr('action');
        var method = $(this).attr('method');
        $.ajax({
            url: url,
            data: data,
            type: method,
            dataType: 'json',
            success: function(res) {
                if (res['status'] == 'ok') {
                    $('#collapse_toggle').click();
                    specification(res['data']);
                } else {
                    alert(res['msg']);
                }
            },
            error: function(error, msg, status) {
                console.log('[FORM SEND ERROR]', msg, status);
                console.log(error);
            }
        });
    });
});
