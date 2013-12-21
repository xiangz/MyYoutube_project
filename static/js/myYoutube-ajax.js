$(document).ready(function(){




    $('.myYoutube-delete').click(function(){


        var key;
        key = $(this).attr("data-key");
        alert("delete "+key+"????");

        $.get('/myYoutube/deleteVideo/', {key: key}, function(data){


            $('#vedios').html(data);

                       });
    });


});
