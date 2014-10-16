/**
 * Created by GoldenGate on 10/14/14.
 */
$(document).ready(function() {


//   on click function scroll {scroll}
//    ajax url helpme
//    scroll()

    function loadHelp () {
        $.ajax({
            url: 'new_helpMe/',
            type: 'GET',
            success: function (data) {
                $('.helpMe').html(data);
//                on click (scroll())
                console.log("data please")
            }
        });
    }
loadHelp();

    $(".addMeButton").on("click", function(){
       console.log('click');
       student_id = $(this).attr('id');
        $.ajax({
            url: '/add_student/' + student_id + '/',
            type: 'GET',
            success: function(response){
                console.log(response);
                $('.helpMe').html(response);
            }
        })
    });

    $(".helpedButton").on("click", function () {
        console.log("helped student");
        help_id = $(this).attr('id');
        $.ajax({
            url: 'remove_help/' + help_id + '/',
            type: 'GET',
            success: function(response){
                console.log(response);
                $('.helpMe').html(response);
            }
        })
    })
});
