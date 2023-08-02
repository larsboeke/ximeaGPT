
(function ($) {
    "use strict";


    /*==================================================================
    [ Focus input ]*/
    $('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })
  
  
    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }


        /*Username already exists*/
        if (check == true) {
            const submitBtn = document.querySelector("#submit-btn");
            const username = document.querySelector("#username");
            localStorage.setItem("username", username.value);
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        // [Checks if the input is empty]
        if($(input).val().trim() == ''){
            if($(input).attr('id') == 'username-register') {
                document.getElementById("divUsername").setAttribute("data-validate", "Enter username")
            } else if ($(input).attr('id') == 'username') {
            document.getElementById("divUsernameLogin").setAttribute("data-validate", "Enter username")
            }
            return false;
        } else {

            // [Function that checks if username is a XIMEA mail]
            if($(input).attr('type') == 'username' || $(input).attr('name') == 'username') {
                if($(input).val().trim().match(/@ximea\.com$/i) == null) {
                    document.getElementById("divUsername").setAttribute("data-validate", "Enter a XIMEA mail adress")
                    return false;
                }
            }
            
                // [Checks if the repeat password is the same]
            if($(input).attr('name') == 'pass-repeat') {
                if(document.getElementById("password-repeat-register").value != document.getElementById("password-register").value) {
                    return false;
                }
            }

        }
        
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        // [Shows error if username already exists]
        if (document.getElementById("divUsername").getAttribute("data-validate") == "Username already exists") {
            showValidate(document.getElementById("username-register"));
        }
        // [Shows error if username and password dont match]
        if (document.getElementById("divUsernameLogin").getAttribute("data-validate") == "Username and password dont match") {
            showValidate(document.getElementById("username"));
        }
    }, false);

    // [Shows error if one input is empty or wrong]
    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    // [Hides error if input is valide]
    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    /*==================================================================
    [ Show pass ]*/
    var showPass = 0;
    $('.btn-show-pass').on('click', function(){
        if(showPass == 0) {
            $(this).next('input').attr('type','text');
            $(this).addClass('active');
            showPass = 1;
        }
        else {
            $(this).next('input').attr('type','password');
            $(this).removeClass('active');
            showPass = 0;
        }
        
    });


})(jQuery);