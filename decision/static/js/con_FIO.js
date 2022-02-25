$(document).ready(function(){
    $("#btn_find_fio").click(function(){
        $.ajax({
        url:'add_decision',
        type:'GET',
        data:{

        input_text:$("#id_snils").serialize()
        },

        beforeSend:function(){
            $('.loader').show();
        },
        success:function(response){

        if (response.stat == 0)
        { alert("Ничего не найдено"),
        $('.loader').hide();

        }
        else{
        $("input[name *='usr_district_code' ]").val(response.ra),
        $("input[name *='fio' ]").val(response.fio),
        $("input[name *='adress' ]").val(response.adress),
        $("input[name *='appeal_date' ]").val(response.date_z),
        $("input[name *='statement_reg_num' ]").val(response.number_z),
        $('.loader').hide();
        }
         }
        });
        });
        });

