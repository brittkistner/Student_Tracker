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
                console.log("data please")
            }
        });
    }
//    function delete_student () {
//        $('.helpedButton').on('click', function(){
//            var student = $(this).prev().attr('href');
//            console.log(student);
//        });
////        $.ajax({
////            url: 'helpMe/',
////            type: 'GET',
////            dataType: 'json',
////            data: student,
////            success: function (data) {
////                $('.helpMe').html(data);
////                console.log("data please")
////            }
////        });
////    }
loadHelp();
setInterval(loadHelp, 5000)
});