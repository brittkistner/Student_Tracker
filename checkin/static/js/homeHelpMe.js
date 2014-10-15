/**
 * Created by GoldenGate on 10/14/14.
 */
$(document).ready(function() {
    $.ajax({
        url: 'helpMe/',
        type: 'GET',
        success: function (data) {
            $('.helpMe').html(data);
        }
    });
//    $('#addMeButton').onclick(function)
});