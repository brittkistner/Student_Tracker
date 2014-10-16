/**
 * Created by GoldenGate on 10/14/14.
 */
$(document).ready(function() {

   on click function scroll {scroll}
    ajax url helpme
    scroll()
    function loadHelp () {
        $.ajax({
            url: 'helpMe/',
            type: 'GET',
            success: function (data) {
                $('.helpMe').html(data);
                on click (scroll())
            }
        });
    }
loadHelp();
    setInterval(loadHelp, 1000)
});