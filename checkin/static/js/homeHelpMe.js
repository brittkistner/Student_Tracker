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
                console.log("data please")
            }
        });
    }
    
//    function scroll
//    $("html, body").animate({ scrollTop: $('#title1').offset().top }, 1000);
loadHelp();
setInterval(loadHelp, 2000)

});