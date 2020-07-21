

// $('#id_start_date').datetimepicker({
// 	timepicker:false,
// 	format: 'Y/m/d'

// });

// $('#id_end_date').datetimepicker({
// timepicker:false,
// 	format: 'Y/m/d'

// });




$(document).ready(function() {
    $("#parent_company_form").validate({
        rules: {
            company_id: {
                required: !0,
            },
            name: {
                required: !0,
            },
        },
        messages: {
            company_id: {
                required: "This field is required.",
            },
            name: {
                required: "This field is required.",
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#submitbtn").text("Please wait...")
            $('#submitbtn').attr('disabled', 'disabled');
            form.submit()
        }
    });

})



$("#id_country").change(function()
    {
        $("#id_state").html('')
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url: '/los/setup/manageparentcompany/binddata/',
        type: 'post',
        dataType: 'json',
        data: {id:id,csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {
            if(data.data != "")
            {
                $("#id_state").html(data.data)
            }
        }
      })
    })

$("#id_state").change(function()
    {
        $("#id_city").html('')
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url: '/los/setup/manageparentcompany/binddatacity/',
        type: 'post',
        dataType: 'json',
        data: {id:id,csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {
            if(data.data != "")
            {
                $("#id_city").html(data.data)
            }
        }
      })
    }) 

$("#id_type_of_borrower").change(function()

    {
        $("#id_category_of_borower").html('')
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({

        url: '/los/templatesetup/binddataborrower/',
        type: 'post',
        dataType: 'json',
        data: {id:id,csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {
            
            if(data.data != "")
            {
                $("#id_category_of_borower").html(data.data)
                $("#id_borrower_role").html('')

            }
        }
      })
    }) 


$("#id_category_of_borower").change(function()
    {
        $("#id_borrower_role").html('')
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url: '/los/templatesetup/binddataborrowerrole/',
        type: 'post',
        dataType: 'json',
        data: {id:id,csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {
            if(data.data != "")
            {
                $("#id_borrower_role").html(data.data)
            }
        }
      })
    }) 


$("#id_borrower_role").change(function()
    {
        $("#id_particulars").html('')
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url: '/los/templatesetup/binddataborrowerparticular/',
        type: 'post',
        dataType: 'json',
        data: {id:id,csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {
            if(data.data != "")
            {
                $("#id_particulars").html(data.data)
            }
        }
      })
    }) 



$("#id_existing_user").change(function(){  
      drop_option = ''
      url_name = $("#get_reallocate_user_existing_user").val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $("#id_escalation_to option").show();
      $("#id_new_user option").show();
      id = $(this).val()
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data){
          get_numner =data.data
          var i;
          for (i = 0; i < get_numner.length; i++) { 
                drop_option += '<option value='+get_numner[i].process_name_id+'>'+get_numner[i].process_name+'</option>'
            }
          $("#id_process_name").html(drop_option)
          $("#id_process_name").fSelect()
          $("#id_process_name").fSelect("reload")
          $("#id_new_user option[value='"+data.user_id.toString()+"']").hide();
          $("#id_escalation_to option[value='"+data.user_id.toString()+"']").hide();
        }
      })
})
