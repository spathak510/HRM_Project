function DeleteRecord(urlid, csrftoken, id)
{  
        swal({  
          title: "Are you sure you want to delete this?",   
          type: "warning",  
          showCancelButton: true,  
          confirmButtonColor: "#DD6B55",  
          confirmButtonText: "Yes",  
          cancelButtonText: "No",  
          closeOnConfirm: false,  
          closeOnCancel: false  
        },
        function(isConfirm)   
        {  
          if (isConfirm)  
          {  
              $.ajax({
                url: urlid,
                type: 'get',
                dataType: 'json',
                data: {id:id},
                async: false,
                cache: false,
                success: function (data)
                {
                  if(data.data == "1")
                  { 
                      $("#data_"+id).remove();
                      swal("Good job", "Data deleted Successfully.", "success");
                  }
                  else
                  {
                    swal("Cancelled", "Something went wrong", "error");
                  }
                }
              })  
          }
          else   
          {  
              swal("Cancelled", "You have Cancelled delete request.", "error");  
          }
        });
}


$("#id_country").change(function(){   
      $("#id_state").html('')
      country_id = $("#bind_country_state").val()
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url: country_id,
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

$("#id_country_map_city").change(function()
{
      $("#id_city").html('')
      $("#select_city").text('')
      country_id = $("#bind_country_state").val()
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url: country_id,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken, key: "map_city"},
        async: false,
        cache: false,
        success: function (data)
        {   
            if(data.data != ""){
                $("#id_city").html(data.data)
            }
            $('#id_city').fSelect()
            $("#id_city").fSelect("reload")
        }
      })
  })

$("#id_state").change(function(){
      $("#id_city").html('')
      bind_city_url = $("#bind_data_city").val()
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url: bind_city_url,
        type: 'post',
        dataType: 'json',
        data: {id:id,csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {
            if(data.data != ""){
                $("#id_city").html(data.data)
            }
            $('#id_city').fSelect()
            $("#id_city").fSelect("reload")
        }
      })
}) 


// Manage parent company and branches

$("#id_parent_com").change(function()
    {
    $("#id_head_office").html('')
      url_name = $("#bind_head_office_url").val()
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url: url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id,csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {
            if(data.data != "")
            {
                $("#id_head_office").html(data.data)
            }
        }
      })
    })

$("#id_head_office").change(function()
{
   $("#id_brach").html('')
   url_name = $("#bind_branches_url").val()
    id = $(this).val()
    csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url:url_name,
      type: 'post',
      dataType: 'json',
      data: {id:id, csrfmiddlewaretoken:csrftoken},
      async: false,
      cache: false,
      success: function (data)
      {   
          if(data.data != ""){
              $("#id_brach").html(data.data)
          }
          $("#id_brach").fSelect()
          $("#id_brach").fSelect("reload")
      }
    })
}) 


$("#user_id").change(function(){
      url_name = $("#bind_get_user_url").val()
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data){ 
            if(data.data != "")
            {
                $("#Department").val(data.user_department)
                $("#Designation").val(data.user_deg)
                $("#Responsibilities").val(data.user_res)
                $("#bind_branches_name").html(data.branches_name)
                $("#bind_branches_name").fSelect()
                $("#bind_branches_name").fSelect("reload")
                $("#city_ids").html(data.map_cities)
                $("#city_ids").fSelect()
                $("#city_ids").fSelect("reload")
                $("#product").val(data.client_prodcut)
                $("#client_type").val(data.client_type)
                $("#client_category").val(data.client_category)
            }
        }
    })
}) 


$("#id_user").change(function(){
      url_name = $("#bind_get_user_url").val()
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data){
          if(data.data != ""){
                $("#id_department").val(data.user_department)
                $("#id_designation").val(data.user_deg)
                $("#id_responsibility").val(data.user_res)
                $("#id_location").val()
          }
        }
      })
}) 


function get_all_confirm_again(urlid, csrftoken){     
      trHTML = ''
      url_name = $("#get_confirm_again").val()
      id = urlid
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {  
          $("#append_table").html(trHTML)
          trHTML += '<table class="table table-bordered table-hover"><thead><tr><th>Confirm Again Date </th><th> Comment </th></tr></thead>'
          $.each(data, function (i, item) {
              for (i = 0; i < item.length; i++) {
                trHTML += '<tr><td>' + new Date(item[i]['fields']['date_time_re']) + '</td><td>' + item[i]['fields']['comment'] + '</td></tr>';
            }
          });
          trHTML += "</table>"
          $("#append_table").html(trHTML)
         $("#myModal3").show()
          $("#myModal3").addClass('fade in')
        }
      })
}

function get_all_refollowups_again(urlid, csrftoken)
{     
      trHTML = ''
      url_name = $("#get_re_followups").val()
      id = urlid
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {  
          $("#append_table").html(trHTML)
          trHTML += '<table class="table table-bordered table-hover"><thead><tr><th> Name Of Person </th><th> Location </th><th> Date and Time </th><th> Comment </th></tr></thead>'
          $.each(data, function (i, item) {
              for (i = 0; i < item.length; i++) {
                trHTML += '<tr><td>' + item[i]['fields']['name_of_person'] + '</td><td>' + item[i]['fields']['location'] + '</td><td>' + new Date(item[i]['fields']['date_time_re']) + '</td><td>' + item[i]['fields']['comment'] + '</td></tr>';
            }
          });
          trHTML += "</table>"
        $("#append_table").html(trHTML)
        $("#myModal3").show()
        $("#myModal3").addClass('fade in')
        }
      })
}

function view_all_meetings_again(urlid, csrftoken)
{     
      trHTML = ''
      url_name = $("#get_re_meetings").val()
      id = urlid
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {  
          $("#append_table").html(trHTML)
          trHTML += '<table class="table table-bordered table-hover"><thead><tr><th> Name Of Person </th><th> Location </th><th> Date and Time </th><th> Comment </th></tr></thead>'
          $.each(data, function (i, item) {
              for (i = 0; i < item.length; i++) {
                trHTML += '<tr><td>' + item[i]['fields']['name_of_person'] + '</td><td>' + item[i]['fields']['location'] + '</td><td>' + new Date(item[i]['fields']['date_time_re']) + '</td><td>' + item[i]['fields']['comment'] + '</td></tr>';
            }
          });
          trHTML += "</table>"
        $("#append_table").html(trHTML)
        $("#myModal3").show()
        $("#myModal3").addClass('fade in')
        }
      })
}


function view_all_cancelled_meetings(urlid, csrftoken)
{     
      trHTML = ''
      url_name = $("#get_meetgings_cancelled").val()
      id = urlid
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {  
          $("#append_table").html(trHTML)
          trHTML += '<table class="table table-bordered table-hover"><thead><tr><th> Meetging Cancelled Date Time </th></tr></thead>'
          $.each(data, function (i, item) {
              for (i = 0; i < item.length; i++) {
                trHTML += '<tr><td>' + item[i]['fields']['added'] + '</td></tr>';
            }
          });
          trHTML += "</table>"
        $("#append_table").html(trHTML)
        $("#myModal3").show()
        $("#myModal3").addClass('fade in')
        }
      })
}


  $("#id_data").change(function()
    {   
      
      drop_option = ''
      $("#id_number").html(drop_option)
      url_name = $("#get_all_data_data_from_master").val()
      get_text = $("#id_data option:selected").text();
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {get_text:get_text, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {  
          get_numner = JSON.parse(data['data'])
          var i;
          
          for (i = 0; i < get_numner.length; i++) { 
            drop_option += '<option value='+get_numner[i]+'>'+get_numner[i]+'</option>'
          }
          $("#id_number_sms_com").html(drop_option)
          $("#id_number_sms_com").fSelect()
          $("#id_number_sms_com").fSelect("reload")
          
        }
      })
})


  function SendMobileAPP(apk, csrftoken)
  {  
      url= $("#crm_web_send_mobile_app").val()
      $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: {link_url:apk, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {
          if(data.data == "1")
          { 
            swal("Good job", "Send Successfully.", "success");
          }
          else
          {
            swal("Cancelled", "Something went wrong", "error");
          }
        }
      })
  }

$("#id_email_data").change(function()
{
      drop_option = ''
      $("#id_number").html(drop_option)
      url_name = $("#crm_web_mail_all_data").val()
      get_text = $("#id_email_data option:selected").text();
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {get_text:get_text, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {  
          get_numner = JSON.parse(data['data'])
          var i;
          
          for (i = 0; i < get_numner.length; i++) { 
            drop_option += '<option value='+get_numner[i]+'>'+get_numner[i]+'</option>'
          }
          $("#id_email_sms_com").html(drop_option)
          $("#id_email_sms_com").fSelect()
          $("#id_email_sms_com").fSelect("reload")
        }
      })
})

$("#id_employee_id").change(function()
    {
      url_name = $("#crm_website_employeeservices_employeeregistration_updatedeaprtment_json").val()
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {   
            if(data.data != "")
            {
                $("#id_employee_name").val(data.data.employee_name).attr('readonly', true)
                $("#id_current_designation").val(data.data.designation).attr('readonly', true)
                $("#id_current_department").val(data.data.department).attr('readonly', true)
                $("#id_current_reporting_to").val(data.data.reporting_to).attr('readonly', true)
                $("#id_current_location").val(data.data.location).attr('readonly', false)
                $("#id_current_responsibilites").val(data.data.responsibilites).attr('readonly', true)
                $("#id_current_salary").val(data.data.current_sal).attr('readonly', true)
            }
        }
      })
})

$("#id_type_of_leave").change(function(){
      url_name = $("#crm_website_employeeservices_leaves_quota").val()
      id = $(this).val()
      user_id  = $("#id_employee_name").val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken,user_id:user_id},
        async: false,
        cache: false,
        success: function (data)
        {   
            if(data.data != "")
            {
                $("#id_leave_available").val(data.data.employee_quota).attr('readonly', true)
            }
        }
      })
})

$("#id_request_id").change(function(){
      url_name = $("#get_purchase_detail_data").val()
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {   
            if(data.data != "")
            {   
                $("#id_department").val(data.data.department)
                $("#id_service_type").val(data.data.service_type)
                $("#id_service_name").val(data.data.service_name)
                $("#id_service_details").val(data.data.service_details)
            }
        }
      })
})


$("#id_vendor_user").change(function(){
      url_name = $("#crm_vendorsupport_vendor_detail").val()
      id = $(this).val()
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {   
            if(data.data != "")
            {   
                $("#id_email_id").val(data.data.email)
                $("#id_contact_number").val(data.data.contact_no)
            }
        }
    })
})

$("#send_wish_to_attend").click(function(){
      url_name = $("#crm_vendorsupport_send_wish_to_attend").val()
      id = $(this).attr('data-attr')
      csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        url:url_name,
        type: 'post',
        dataType: 'json',
        data: {id:id, csrfmiddlewaretoken:csrftoken},
        async: false,
        cache: false,
        success: function (data)
        {   
          if(data.data != ""){   
              swal("Good job", "Send Successfully.", "success");
          }
          else{
              swal("Warning", "Already Send Request.", "warning");
          }
        }
      })
})