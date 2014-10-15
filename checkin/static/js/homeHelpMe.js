/**
 * Created by GoldenGate on 10/14/14.
 */
$(document).ready(function() {

    function loadHelp () {
        $.ajax({
            url: 'helpMe/',
            type: 'GET',
            success: function (data) {
                $('.helpMe').html(data);
            }
        });
    }
loadHelp();
    setInterval(loadHelp, 1000)
});