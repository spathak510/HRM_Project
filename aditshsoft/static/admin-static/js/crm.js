$(document).ready(function () 
{
    $.validator.addMethod("greaterThanEqualYear", function (value, element, param) {
        var $otherElement = $(param);
        return parseInt(value) >= parseInt($otherElement.val());
    });
    $.validator.addMethod("greaterThanEqualMonth", function (value, element, param) {
        var $otherElement = $(param);
        return parseInt(value) >= parseInt($otherElement.val());
    });


    $.validator.addMethod("pwcheck", function (value) {
        return /[\@\#\$\%\^\&\*\(\)\_\+\!]/.test(value) && /[a-z]/.test(value) && /[0-9]/.test(value) && /[A-Z]/.test(value)
    });

    // Reporting currency & Local Currency
    $.validator.addMethod("holidays_weekly_working_fun",function(value, element){
        get_text = $("#weekly_working_days option:selected").map(function () {
            return $(this).val();
        }).get().join(', ')
        var newArray = get_text.split(',').filter(function(v){return v!==''});
        return newArray.length > 0;
    });

    $.validator.addMethod("holidays_weekly_off_fun",function(value, element){
        get_text = $("#weekly_off_working_days option:selected").map(function () {
            return $(this).val();
        }).get().join(', ')
        var newArray = get_text.split(',').filter(function(v){return v!==''});
        return newArray.length > 0;
    });

    $.validator.addMethod("holidays_weekly_half_days_fun",function(value, element){
        get_text = $("#half_days option:selected").map(function () {
            return $(this).val();
        }).get().join(', ')
        var newArray = get_text.split(',').filter(function(v){return v!==''});
        return newArray.length > 0;
    });


    $.validator.addMethod("map_branch_with_cities_fun",function(value, element){
        get_text = $("#id_brach option:selected").map(function () {
            return $(this).val();
        }).get().join(', ')
        var newArray = get_text.split(',').filter(function(v){return v!==''});
        return newArray.length > 0;
    });


    $("#employee_management_define_deduction").validate({
        rules: {
            minimum: {
                required: !0,
            },
            maximum: {
                required: !0,
                greaterThanEqualMonth: "#id_minimum"
            },
        },
        messages: {
            minimum: {
                required: "This field is required.",
            },
            maximum: {
                required: "This field is required.",
                greaterThanEqualMonth : "Maximum should be greater than or equal to minimum."
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

    $("#financial_form").validate({
        rules: {
            from_month: {
                required: !0,
            },
            to_month: {
                required: !0,
            },
            from_year: {
                required: !0,
            },
            to_year: {
                required: !0,
            },
            maximum_salary: {
                required: !0,
                greaterThanEqualYear: "#id_start_salary"
            },
        },
        messages: {
            from_month: {
                required: "This field is required.",
            },
            to_month: {
                required: "This field is required.",
            },
            from_year: {
                required: "This field is required.",
            },
            to_year: {
                required: "This field is required.",
            },
            maximum_salary: {
                required: "This field is required.",
                greaterThanEqualYear : "Maximum salary should be greater than or equal to salary Range."
            },
            
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#to_year-error").val('')
            var GivenDate = $("#from_year").val()+'-'+$("#from_month").val();
            GivenDate = new Date(GivenDate);
            CurrentDate = new Date($("#to_year").val()+'-'+$("#to_month").val());
            if(GivenDate < CurrentDate){ 
                console.log()
            }
            else{
                $("#to_year-error").show()
                $("#to_year-error").text('To date is greater than the from date.')
                return false;
            }
            $("#financial_form_btn").text("Please wait...")
            $('#financial_form_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    $("#financial_report_form").validate({
        rules: {
            from_month: {
                required: !0,
            },
            to_month: {
                required: !0,
                greaterThanEqualMonth: "#from_month"
            },
            from_year: {
                required: !0,
            },
            to_year: {
                required: !0,
                greaterThanEqualYear: "#from_year"
            },
        },
        messages: {
            from_month: {
                required: "This field is required.",
            },
            to_month: {
                required: "This field is required.",
                greaterThanEqualMonth : "To month should be greater tham or equal to From month."
            },
            from_year: {
                required: "This field is required.",
            },
            to_year: {
                required: "This field is required.",
                greaterThanEqualYear : "To year should be greater than or equal to From year."
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#to_year-error").val('')
            var GivenDate = $("#from_year").val()+'-'+$("#from_month").val();
            GivenDate = new Date(GivenDate);
            CurrentDate = new Date($("#to_year").val()+'-'+$("#to_month").val());
            if(GivenDate < CurrentDate){ 
                console.log()
            }
            else{
                $("#to_year-error").show()
                $("#to_year-error").text('To date is greater than the from date.')
                return false;
            }
            $("#financial_report_btn").text("Please wait...")
            $('#financial_report_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    $("#working_hours_form").validate({
        rules: {
            working_hours: {
                required: !0,
            },
            start_date_time: {
                required: !0,
            },
            end_date_time: {
                required: !0,
            },
            lunch_break: {
                required: !0,
            },
        },
        messages: {
            working_hours: {
                required: "This field is required.",
            },
            start_date_time: {
                required: "This field is required.",
            },
            end_date_time: {
                required: "This field is required.",
            },
            lunch_break: {
                required: "This field is required.",
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#working_hours_btn").text("Please wait...")
            $('#working_hours_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    $("#response_form_id_map_city").validate({
        rules: {
            contry: {
                required: !0,
            },
            state: {
                required: !0,
            },
            city: {
                required: false,
            },
            parent_company: {
                required: !0,
            },
            head_offce: {
                required: !0,
            },
            branch_name: {
                required: !0,
            },
        },
        messages: {
            contry: {
                required: "This field is required.",
            },
            state: {
                required: "This field is required.",
            },
            city: {
                required: "This field is required.",
            },
            parent_company: {
                required: "This field is required.",
            },
            head_offce: {
                required: "This field is required.",
            },
            branch_name: {
                required: "This field is required.",
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            if($("#id_city").val().length == 0){
                $('.multi_select_va').text("This field is required.")
                $('.multi_select_va').show()
                return false
            }
            if($("#id_brach").val() == ""){
                $('.multi_select_va1').text("This field is required.")
                $('.multi_select_va1').show()
                return false
            }
            $('.multi_select_va').hide()
            $('.multi_select_va1').hide()

            $("#working_hours_btn").text("Please wait...")
            $('#working_hours_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    $("#working_days_form").validate({
        rules: {
            weekly_working_days: {
                required: !0,
            },
            weekly_off_working_days: {
                required: !0,
            },
        },
        messages: {
            working_hours: {
                required: "This field is required.",
            },
            start_date_time: {
                required: "This field is required.",
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#working_days_btn").text("Please wait...")
            $('#working_days_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    $("#holidays_form").validate({
        rules: {
            holidays_type: {
                required: !0,
            },
            holiday_year: {
                required: !0,
            },
            holiday_month: {
                required: !0,
            },
            applicable_to: {
                required: !0,
            },
            implact_on_salry: {
                required: !0,
            },
            holidays_date: {
                required: !0,
            },
            
        },
        messages: {
            holidays_type: {
                required: "This field is required.",
            },
            holiday_year: {
                required: "This field is required.",
            },
            holiday_month: {
                required: "This field is required.",
            },
            applicable_to: {
                required: "This field is required.",
            },
            implact_on_salry: {
                required: "This field is required.",
            },
            holidays_date: {
                required: "This field is required.",
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#holidays_btn").text("Please wait...")
            $('#holidays_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    $("#overtime_form").validate({
        rules: {
            start_date_time: {
                required: !0,
            },
            end_date_time: {
                required: !0,
            },
            implact_on_salry: {
                required: !0,
            },
            over_time_days: {
                required: !0,
            },
            over_time_applicable: {
                required: !0,
            },
        },
        messages: {
            start_date_time: {
                required: "This field is required.",
            },
            end_date_time: {
                required: "This field is required.",
            },
            implact_on_salry: {
                required: "This field is required.",
            },
            over_time_days: {
                required: "This field is required.",
            },
            over_time_applicable: {
                required: "This field is required.",
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#overtime_btn").text("Please wait...")
            $('#overtime_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    $("#response_form_id").validate({
        rules: {
            response_name: {
                required: !0,
            },
            response_type: {
                required: !0,
            },
            response_description: {
                required: !0,
            },
            response_impact_on_data: {
                required: !0,
            },
        },
        messages: {
            response_name: {
                required: "This field is required.",
            },
            response_type: {
                required: "This field is required.",
            },
            response_description: {
                required: "This field is required.",
            },
            response_impact_on_data: {
                required: "This field is required.",
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#response_form_btn").text("Please wait...")
            $('#response_form_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    $("#define_client_form_id").validate({
        rules: {
            define_client_type: {
                required: !0,
            },
            define_client_category: {
                required: !0,
            },
            define_lead_values: {
                required: !0,
            },
            define_type_of_Data: {
                required: !0,
            },
        },
        messages: {
            define_client_type: {
                required: "This field is required.",
            },
            define_client_category: {
                required: "This field is required.",
            },
            define_lead_values: {
                required: "This field is required.",
            },
            define_type_of_Data: {
                required: "This field is required.",
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#define_client_form_btn").text("Please wait...")
            $('#define_client_form_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });
    
    $("#upload_bulk_from_id").validate({
        rules: {
            upload_bulk_data: {
                required: !0,
            },
        },
        messages: {
            upload_bulk_data: {
                required: "This field is required.",
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#upload_bulk_from_btn").text("Please wait...")
            $('#upload_bulk_from_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    // ************************** WebSite Change Pasword ***************
    $("#adminchangepassword").validate({
        rules: {
            oldpassword: {
                required: !0,
            },
            newpassword: {
                required: !0,
                minlength: 10,
                maxlength: 20,
                pwcheck: !0
            },
            confirmpassword: {
                required: !0,
                equalTo: "#newpassword"
            },
        },
        messages: {
            oldpassword: {
                required: "This field is required.",
            },
            newpassword: {
                required: "This field is required.",
                password_strength: "Password should be a minimum of eight characters in length, and should contain at least one letter, one number and one special character.",
                minlength: "Password should be minimum of 10 characters.",
                maxlength: "Password should be maximum of 20 characters.",
                pwcheck:  "Password Strength  should be Combination of Upper case, Lower case, Numerical and Special Characters ",
            },
            confirmpassword: {
                required: "This field is required.",
                equalTo: "Password and confirm password does not match."
            }
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#adminchangepasswordbtn").text("Please wait..")
            $('#adminchangepasswordbtn').attr('disabled', 'disabled');
            form.submit()
        }
    });
    // On change image functionality
    $(document).on("change", '.upload_bulk_data', function() {
        var fileSize = 0;
        var fileExtension = ['csv'];
        if ($.inArray($(this).val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            swal("Invalid file.Please upload csv file.")
            $(this).val('')
            return !1
        }
    });


    check_user_name_email = $("#get_user_exists").val()
    check_user_name_phone = $("#get_phone_exists").val()

    $.validator.addMethod("pan_card_check",function(value){
        return  /[A-Z]{5}\d{4}[A-Z]{1}/.test(value);
    });

    $.validator.addMethod("pin_code_check",function(value){
        return   /^[0-9a-zA-Z]{6,}/.test(value);
    });

    $.validator.addMethod("gstin_check",function(value){
        return  /\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}/.test(value);
    });

    $.validator.addMethod("tan_no_check",function(value){
        return  /^[A-Z]{4}[0-9]{5}[A-Z]{1}/.test(value);
    });

    $.validator.addMethod("email_check",function(value){
        return  /[\w.+\-]+@[a-zA-Z]+\.[a-zA-Z]{2,}/.test(value);
    });

    // Reporting currency & Local Currency
    $.validator.addMethod("reporting_curr_fun",function(value, element){
        get_text = $("#id_reporting_currency option:selected").map(function () {
            return $(this).val();
        }).get().join(', ')
        var newArray = get_text.split(',').filter(function(v){return v!==''});
        return newArray.length > 0;
    });

    $.validator.addMethod("local_currency_fun",function(value, element){
        get_text = $("#id_local_currency option:selected").map(function () {
            return $(this).val();
        }).get().join(', ')
        var newArray = get_text.split(',').filter(function(v){return v!==''});
        return newArray.length > 0;
    });
    $.validator.addMethod("user_role_fun",function(value, element){
        get_text = $("#id_user_role option:selected").map(function () {
            return $(this).val();
        }).get().join(', ')
        var newArray = get_text.split(',').filter(function(v){return v!==''});
        return newArray.length > 0;
    });

    $.validator.addMethod("city_validation_fun",function(value, element){
        get_text = $("#id_city option:selected").map(function () {
            return $(this).val();
        }).get().join(', ')
        var newArray = get_text.split(',').filter(function(v){return v!==''});
        return newArray.length > 0;
    });

    $.validator.addMethod("adhar_no_check",function(value){
        return  /^[0-9]{4}[0-9]{4}[0-9]{4}/.test(value);
    });

    $("#parent_company_form").validate({
        rules: {
            company_id: {
                required: !0,
            },
            email: {
                required: !0,
                email_check : !0,
                remote: {
                        url: check_user_name_email,
                        type: "get",
                        data: {
                              email_id: function() {
                                return $( "#id_email" ).val();
                              },
                              id: function() {
                                return $( "#user_id" ).val();
                              },
                        }
                    },
            },
            mobile_no: {
                required: !0,
                remote: {
                        url: check_user_name_phone,
                        type: "get",
                        data: {
                            mobile_no: function() {
                            return $( "#id_mobile_no" ).val();
                            },
                            id: function() {
                            return $( "#user_id" ).val();
                            },
                        }
                    },
            },
            city:{
                required: false,
                city_validation_fun: false,
            },
            gen_password:{
                pwcheck: !0
            },
            pan_card:{
                pan_card_check: !0,
            },
            pincode:{
                pin_code_check: !0,
            },
            gst_no:{
                gstin_check: !0,
            },
            tan_no:{
                tan_no_check: !0,
            },
            website:{
                 required: true,
                 url: true
            },
            template_type:{
                required: !0,
            },
            template_name:{
                required: !0,
            },
            purpose:{
                required: !0,
            },
            notification_method:{
                required: !0,
            },
            notification_type:{
                required: !0,
            },
            local_currency:{
                local_currency_fun: !0,
            },
            reporting_currency:{
                reporting_curr_fun: !0,
            }, 
            user_role:{
                user_role_fun: !0,
            },
        },
        ignore: ':hidden:not("#id_local_currency, #id_reporting_currency, #id_user_role, #id_city")',
        messages: {
            company_id: {
                required: "This field is required.",
            },
            name: {
                required: "This field is required.",
            },
            city:{
               required: "This field is required.",
               city_validation_fun: "This field is required.",
            },
            gen_password:{
                pwcheck:  "Password Strength  should be Combination of Upper case, Lower case, Numerical and Special Characters ",
            },
            pan_card:{
                pan_card_check:"Invalid Pan Card Number !"
            },
            pincode:{
                pin_code_check:"Invalid Pin Code !"
            },
            gst_no:{
                gstin_check:"Invalid GST Number !"
            },
            tan_no:{
                tan_no_check:"Invalid TAN Number !"
            },
            contact_no:{
                mobile_no_check:"Invalid MObile Number !"
            },
            mobile_no:{
                mobile_no_check:"Invalid Mobile Number !"
            },
            email:{
                required: "This field is required.",
                email_check:"Invalid Email Address !"
            },
            template_type:{
                required:"This Field is required ."
            },
            template_name:{
                required:"This Field is required ."
            },
            purpose:{
                required:"This Field is required ."
            },
            notification_method:{
                required: "This Field is required ."
            },
            notification_type:{
                required: "This Field is required ."
            },
            local_currency:{
                local_currency_fun:"This Field is required."
            },
            reporting_currency:{
                reporting_curr_fun:"This Field is required."
            },
            user_role:{
                user_role_fun: "This Field is required."
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
    
    $("#allow_cation_set_up_form").validate({
        rules: {
            user: {
                required: !0,
            },
            type_of_data_allocation: {
                required: false,
            },
        },
        messages: {
            user: {
                required: "This field is required.",
            },
            type_of_data_allocation: {
                required: false,
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            $("#allow_cation_set_up_btn").text("Please wait...")
            $('#allow_cation_set_up_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    $("#response_form_id_map_city").validate({
        rules: {
            contry: {
                required: !0,
            },
            state: {
                required: !0,
            },
            city: {
                required: !0,
            },
            parent_company: {
                required: !0,
            },
            head_offce: {
                required: !0,
            },
            branch_name: {
                map_branch_with_cities_fun: !0,
            },
        },
        ignore: ':hidden:not("#id_brach")',
        messages: {
            contry: {
                required: "This field is required.",
            },
            state: {
                required: "This field is required.",
            },
            city: {
                required: "This field is required.",
            },
            parent_company: {
                required: "This field is required.",
            },
            head_offce: {
                required: "This field is required.",
            },
            branch_name: {
                map_branch_with_cities_fun: "This field is required.",
            },
        },
        highlight: function(element) {
            $(element).children().addClass('error')
        },
        submitHandler: function(form) {
            if($("#id_city").val().length == 0){
                $('.multi_select_va').text("This field is required.")
                $('.multi_select_va').show()
                return false
            }
            $('.multi_select_va').hide()
            $('.multi_select_va1').hide()
            $("#working_hours_btn").text("Please wait...")
            $('#working_hours_btn').attr('disabled', 'disabled');
            form.submit()
        }
    });

    
    $("#add_edit_consultant").validate({
        rules: {
            pan_card:{
                pan_card_check: !0,
            },
            pincode:{
                pin_code_check: !0,
            },
            gst_registration:{
                gstin_check: !0,
            },
        },
        messages: {
            pan_card:{
                pan_card_check:"Invalid Pan Card Number !"
            },
            pincode:{
                pin_code_check:"Invalid Pin Code !"
            },
            gst_registration:{
                gstin_check:"Invalid GST Number !"
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
    $("#user_registration_personal_details").validate({

        rules: {
            pan_card:{
                pan_card_check: !0,
            },
            adhar_card:{
                adhar_no_check: !0,
            },
        },
        messages: {
            pan_card:{
                pan_card_check:"Invalid Pan Card Number !"
            },
            adhar_card:{
                adhar_no_check:"Invalid Adhar Card Number!"
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




$(document).ready(function () {
    //this calculates values automatically 
    sum();
    $("#num1, #num2").on("keydown keyup", function () {
        sum();
    });
});

function sum() {
    var num1 = document.getElementById('num1').value;
    var num2 = document.getElementById('num2').value;
    var result = parseInt(num1) + parseInt(num2);
  
    if (!isNaN(result)) {
        document.getElementById('sum').value = result;
        
    }
}
// 

$(document).ready(function () {
    //this calculates values automatically 
    sum1();
    $("#num3,#num4,#num5,#num6,#num7 ").on("keydown keyup", function () {
        sum1();
    });
});

function sum1() {
    var num3 = document.getElementById('num3').value;
    var num4 = document.getElementById('num4').value;
    var num5 = document.getElementById('num5').value;
    var num6 = document.getElementById('num6').value;
    var num7 = document.getElementById('num7').value;
    var result = parseInt(num3) + parseInt(num4) + parseInt(num5) + parseInt(num6) + parseInt(num7);

    if (!isNaN(result)) {
        document.getElementById('sum1').value = result;

    }
}

/*******************************************/ 
// function s2() {
//     var num10 = document.getElementById('num10').value;
//     var num11 = document.getElementById('num11').value;
//     var num12 = document.getElementById('num12').value;
//     var num13 = document.getElementById('num13').value;
//     var num14 = document.getElementById('num14').value;
//     var num15 = document.getElementById('num15').value;
//     var num16 = document.getElementById('num16').value;
//     var result = parseInt(num10) + parseInt(num11) + parseInt(num12) + parseInt(num13) + parseInt(num14) + parseInt(num15) + parseInt(num16);

//     if (!isNaN(result)) {
//         document.getElementById('s2').value = result;

//     }
// }
