$(document).ready(function(){
    $("#btn_changer").click(function(){
        $.ajax({
        url:'http://127.0.0.1:8000/Decision/edit_item/4',
        type:'GET',
        success:function(response){

        $("input[name *='actial_term' ]").val(response.actial_term)
        }

        });
        });
        });




