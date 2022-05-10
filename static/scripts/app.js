jQuery(function() {
    // Inputmask (Phone numbers)
    $("input[name=phone]").inputmask("(+234) 999-9999999", {"onincomplete": function() {
        swal("Oops!", "Incomplete phone number, please review!", "info");
        return false;
    }});

    // Characters remaining counter
    var start = 0;
    var limit = 1000;
    $("#id_message").keyup(function() {
        start = this.value.length
        if (start > limit) {
            return false;
        }
        else if (start == 1000) {
            $("#remainingCharacters").html("Characters remaining: " + (limit - start)).css('color', 'red');
            swal("Oops!", "Characters limit exceeded!", "info");
        }
        else if (start > 984) {
            $("#remainingCharacters").html("Characters remaining: " + (limit - start)).css('color', 'red');
        }
        else if (start < 1000) {
            $("#remainingCharacters").html("Characters remaining: " + (limit - start)).css('color', 'black');
        }
        else {
            $("#remainingCharacters").html("Characters remaining: " + (limit - start)).css('color', 'black');
        }
    });

    // File size limit
    $("#id_file, #id_file2").bind('change', function() {
        var a = (this.files[0].size);
        if (a > 2 * 1048576) {
            swal("Attention!", "Maximum allowed size is 2MB.", "info");
            this.value = "";
        }
    });

    // Convert email to Lowercase
    $("input[name=email]").keyup(function() {
        this.value = this.value.toLowerCase();
    });

    // Enable/Disable select options
    $('#id_person').on('change', function() {
        var value = $(this).val();
        $('#id_subject option[value="Update resume"]').prop('disabled', ($(this).val() == 'Employee'));
        $('#id_subject option[value="I lost my account"]').prop('disabled', ($(this).val() == 'Candidate'));
        $('#id_subject option[value="My password does not work"]').prop('disabled', ($(this).val() == 'Candidate'));
    });
    $('#id_person').trigger('change');

    // Hide offcanvas when Support button is clicked
    $("#offcanvasRight, .offcanvas-body a").click(function() {
        $('.offcanvas').offcanvas('hide');
    });

});


// Frontend Email validation
function validateEmail(email) {
    const regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

// Frontend Form Validation
function validateFrontendForm() {
    const fullname = document.getElementById("id_fullname").value;
    const age = document.getElementById("id_age").value;
    const email = document.getElementById("id_email").value;
    const phone = document.getElementById("id_phone").value;
    const address = document.getElementById("id_address").value;
    const experience = document.getElementById("id_experience").value;
    const skills = document.getElementById("id_skills").value;
    const file = document.getElementById("id_file").value;

    // Prevent bad word filter
    var badwords = new Array("Fuck you", "Kiss my ass");
    var regex = new RegExp('\\b(' + badwords.join('|') + ')\\b', 'i');
    var text = document.frontend.experience.value;

    if (fullname == "") {
        swal("Oops!", "Fullname field cannot be empty.", "error");
        return false;
    }
    else if (fullname == fullname.toUpperCase()) {
        document.getElementById("id_fullname").value="";
        swal("Oops!", "Fullname field cannot be UPPERCASE.", "info");
        return false;
    }
    else if (fullname.split(' ').length < 2) {
        swal("Oops!", "Your first and last name is required.", "info");
        return false;
    }
    else if (age == "") {
        swal("Oops!", "Age field cannot be empty.", "error");
        return false;
    }
    else if ((age < 18) || (age > 60)) {
        document.getElementById("id_age").value="";
        swal("Oops!", "Age between 18 and 60.", "info");
        return false;
    }
    else if (email == "") {
        swal("Oops!", "Email field cannot be empty.", "error");
        return false;
    }
    else if (!(validateEmail(email))) {
        document.getElementById("id_email").value="";
        swal("Oops!", "Enter a valid email address.", "error");
        return false;
    }
    else if (phone == "") {
        swal("Oops!", "Phone field cannot be empty.", "error");
        return false;
    }
    else if (address == "") {
        swal("Oops!", "Address field cannot be empty.", "error");
        return false;
    }
    else if (experience == "") {
        swal("Oops!", "Experience field cannot be empty.", "error");
        return false;
    }
    else if (regex.test(text)) {
        swal("Oops!", "Your experience field contains bad words.", "error");
        return false;    
    }
    else if (skills == "") {
        swal("Oops!", "Skills field cannot be empty.", "error");
        return false;
    }
    else if (file == "") {
        swal("Oops!", "File field cannot be empty.", "error");
        return false;
    }
    else {
        return true;
    }
}

// Backend Email validation
function validateEmail(email) {
    const regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

// Backend Form Validation
function validateBackendForm() {
    const fullname = document.getElementById("id_fullname2").value;
    const age = document.getElementById("id_age2").value;
    const email = document.getElementById("id_email2").value;
    const phone = document.getElementById("id_phone2").value;
    const address = document.getElementById("id_address2").value;
    const experience = document.getElementById("id_experience2").value;
    const skills = document.getElementById("id_skills2").value;
    const file = document.getElementById("id_file2").value;

    if (fullname == "") {
        swal("Oops!", "Fullname field cannot be empty.", "error");
        return false;
    }
    else if (fullname == fullname.toUpperCase()) {
        document.getElementById("id_fullname").value="";
        swal("Oops!", "Fullname field cannot be UPPERCASE.", "info");
        return false;
    }
    else if (fullname.split(' ').length < 2) {
        swal("Oops!", "Your first and last name is required.", "info");
        return false;
    }
    else if (age == "") {
        swal("Oops!", "Age field cannot be empty.", "error");
        return false;
    }
    else if ((age < 18) || (age > 60)) {
        document.getElementById("id_age").value="";
        swal("Oops!", "Age between 18 and 60.", "info");
        return false;
    }
    else if (email == "") {
        swal("Oops!", "Email field cannot be empty.", "error");
        return false;
    }
    else if (!(validateEmail(email))) {
        document.getElementById("id_email").value="";
        swal("Oops!", "Enter a valid email address.", "error");
        return false;
    }
    else if (phone == "") {
        swal("Oops!", "Phone field cannot be empty.", "error");
        return false;
    }
    else if (address == "") {
        swal("Oops!", "Address field cannot be empty.", "error");
        return false;
    }
    else if (experience == "") {
        swal("Oops!", "Experience field cannot be empty.", "error");
        return false;
    }
    else if (skills == "") {
        swal("Oops!", "Skills field cannot be empty.", "error");
        return false;
    }
    else if (file == "") {
        swal("Oops!", "File field cannot be empty.", "error");
        return false;
    }
    else {
        return true;
    }
}

// Clear modal form when closed
$("#frontendModal, #backendModal").on('hidden.bs.modal', function() {
    $('#frontendModal form')[0].reset();
    $('#backendModal form')[0].reset();
});

// Allow only letters in Fullname field
$("input[name=fullname]").keyup(function() {
    if (!/^[a-zA-Z _]*$/.test(this.value)) {
        this.value = this.value.split(/[^a-zA-Z _]/).join('');
    }
})

// Prevent excess whitespace in Fullname field
$("input[name=fullname]").on('keydown', function() {
    var $this = $(this);
    $(this).val($this.val().replace(/(\s{2,})|[^a-zA-Z0-9_']/g, ' ').replace(/^\s*/, ''));
});

// Prevent starting whitespace in inputs
$("input[type='text'], input[type='tel'], textarea").on('keypress', function(e) {
    if (e.which === 32 && !this.value.length)
        e.preventDefault();
});

// Allow only numbers in Age field
$("input[name=age]").keyup(function() {
    if (!/^[0-9]*$/.test(this.value)) {
        this.value = this.value.split(/[^0-9]/).join('');
    }
});

// Prevent starting by Zero in Age field
$("input[name=age]").on("input", function() {
    if(/^0/.test(this.value)) {
        this.value = this.value.replace(/^0/, "")
    }
});

// Hide/show passwordt toggle
function togglePassword() {
    var p = document.getElementById("id_password");
    if (p.type === 'password') {
        p.type = "text";
    } else {
        p.type = "password";
    }
}

// Dependent select option
function dependentSelect() {
    // if ($("#id_person").value != '')
    //     $("#id_subject").prop('disabled', false);
    // else
    //     $("#id_subject").prop('disabled', 'disabled');
    if (document.getElementById("id_person").value != '')
        document.getElementById("id_subject").disabled = false;
    else
        document.getElementById("id_subject").disabled = true;
}

// Create Text pulse
(function pulse() {
    $('.text-pulse').fadeOut(1000).fadeIn(1000, pulse);
})();

// Live Time
setInterval(function() {
    var date = new Date();
    $("#clock").html(
        (date.getHours() < 10 ? '0' : '') + date.getHours() + ':' + 
        (date.getMinutes() < 10 ? '0' : '') + date.getMinutes() + ':' + 
        (date.getSeconds() < 10 ? '0' : '') + date.getSeconds()
    );
}, 500);


// Refresh window at (00:00 - 12 Midnight)
function autoRefresh(hours, minutes, seconds){
    var now = new Date(), then = new Date();
    then.setHours(hours, minutes, seconds, 0);
    if (then.getTime() < now.getTime()) {
        then.setDate(now.getDate() + 1);
    }
    var timeout = (then.getTime() - now.getTime());
    setTimeout(function() {
        window.location.reload(true);
    }, timeout);
}
autoRefresh(0,0,0)

// Hide all contents, if no Messages
var verify = $("#check_td").length;
if (verify == 0) {
    $(".hide").css("display", "none");
    $("#emptyMsg").text("No message found");
    $("#refresh").html('<i class="fas fa-sync-alt fa-3x"></i>');
}
