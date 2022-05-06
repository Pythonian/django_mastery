jQuery(function() {
    // Inputmask (Phone numbers)
    $("input[name=phone]").inputmask("(+234) 999-9999999", {"onincomplete": function() {
        swal("Oops!", "Incomplete phone number, please review!", "info");
        return false;
    }});

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
