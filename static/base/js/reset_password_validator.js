$("input[type=password]").keyup(function () {
        var ucase = new RegExp("[A-Z]+");
        var lcase = new RegExp("[a-z]+");
        var num = new RegExp("[0-9]+");

        if ($("#id_new_password1").val().length >= 8) {
            $("#8char").addClass("password-check-icon");
        } else {
            $("#8char").removeClass("password-check-icon");
        }

        if (ucase.test($("#id_new_password1").val())) {
            $("#ucase").addClass("password-check-icon");
        } else {
            $("#ucase").removeClass("password-check-icon");
        }

        if (lcase.test($("#id_new_password1").val())) {
            $("#lcase").addClass("password-check-icon");
        } else {
            $("#lcase").removeClass("password-check-icon");
        }

        if (num.test($("#id_new_password1").val())) {
            $("#num").addClass("password-check-icon");
        } else {
            $("#num").removeClass("password-check-icon");
        }

        if (($("#id_new_password1").val() == $("#id_new_password2").val()) && ($("#id_new_password1").val().length > 0)) {
            $("#password_match").addClass("password-check-icon");
        } else {
            $("#password_match").removeClass("password-check-icon");
        }

        if (($("#id_new_password1").val() == $("#id_new_password2").val()) && ($("#id_new_password1").val().length > 0)) {
            $("#submitBtn").removeClass("disabled");
            $("#submitBtn").prop('disabled', false);
        } else {
            $("#submitBtn").addClass("disabled");
            $("#submitBtn").prop('disabled', true);
        }
    }
)