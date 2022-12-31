jQuery(function() {
    // Inputmask (Phone numbers)
    // $("input[name=phone]").inputmask("(+234) 999-9999999", {"onincomplete": function() {
    //     swal("Oops!", "Incomplete phone number, please review!", "info");
    //     return false;
    // }});

    // Characters remaining counter
    var start = 0;
    var limit = 1000;
    $("#id_body").keyup(function() {
        start = this.value.length
        if (start > limit) {
            return false;
        }
        else if (start == 1000) {
            $("#remainingCharacters").html("Characters remaining: " + (limit - start)).css('color', 'red');
            // swal("Oops!", "Characters limit exceeded!", "info");
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
    $("#id_file").bind('change', function() {
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

    // Convert Job to Uppercase
    $("input[name=job]").keyup(function () {
        this.value = this.value.toUpperCase();
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
    // Using jquery: var fullname = $("#id_fullname").val();
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
        // $("#id_email").val("");
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

// Clear contents in modal form when closed
$("#frontendModal").on('hidden.bs.modal', function() {
    $('#frontendModal form')[0].reset();
});

// Allow only letters in Fullname field
$("input[name=fullname]").keyup(function() {
    if (!/^[a-zA-Z _]*$/.test(this.value)) {
        this.value = this.value.split(/[^a-zA-Z _]/).join('');
    }
})

// Capitalize the first letter in each word in the fields)
$("input[name=fullname], input[name=firstname], input[name=lastname]").keyup(function () {
    var txt = $(this).val();
    $(this).val(txt.replace(/^(.)|\s(.)/g, function($1) {
        return $1.toUpperCase( );
    }))
});

// Allow only first and last name in Fullname field
$("input[name=fullname]").keyup(function () {
    var fullname = $("input[name=fullname]").val();
    if (fullname.split(' ').length == 3) {
        swal("Oops!", "Only first and last name required.", "info");
        // Clears the Fullname field
        // $("input[name=fullname]").val("");
        return false;
    }
});

// Prevent excess whitespace in the field(s)
$("input[name=fullname], input[name=firstname], input[name=lastname]").on('keydown', function() {
    var $this = $(this);
    $(this).val($this.val().replace(/(\s{2,})|[^a-zA-Z0-9_']/g, ' ').replace(/^\s*/, ''));
});

// Prevent starting whitespace in inputs
$("input[type='text'], input[type='tel'], textarea").on('keypress', function(e) {
    if (e.which === 32 && !this.value.length)
        e.preventDefault();
});

// Allow only numbers in Age field
$("input[name=age], .vacancy_input").keyup(function() {
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

// Hide/show password toggle
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
    $("#emptyMsg").text("No data found");
    $("#refresh").html('<i class="fas fa-sync-alt fa-3x"></i>');
}

// Inform the user about autologout 5mins from time
setTimeout(function() {
    var notice = document.querySelector("#autologoutWarning");
    if (notice) {
        notice.click();
    }    
}, 25 * 60000); // 25mins of no usage

// Autologout after 5mins elapses
setTimeout(function() {
    var action = document.querySelector("#autologoutInfo");
    if (action) {
        action.click();
    }    
}, 30 * 60000); // 30mins of no usage

// Copy the value being entered in an input into another input
// document.getElementById("title").onkeyup=function(){
//     document.getElementById("slug").value = document.getElementById("title").value.toLowerCase().replace(" ", "-");
// }

// Enable/Disable Professional Card. [X] I have experience
$(document).ready(function() {
    $(function() {
        Emp();
        $("#emp").click(Emp);
    });
    function Emp() {
        if (this.checked) {
            $("input.emp, textarea.emp").removeAttr("disabled");
        }
        else {
            $("input.emp, textarea.emp").attr("disabled", true);
        }
    }
});

// Enable/Disable Finished Date. 
// [X] I am employed = Disable
$(function () {
    Exp();
    $("#exp").click(Exp);
});
function Exp() {
    if (this.checked) {
        $("input#go").attr("disabled", true);
        $("#go").val(''); // clear existing data to prevent sending data
    }
    else {
        $("input#go").removeAttr("disabled");
    }
}

// Enable/Disable Finished date (Education)
// If course is completed, enable finished date
function statusCourse(edu) {
    var x = document.getElementsByName("finished_course");
    for(var j=0; j < x.length; j++) {
        x[j].disabled = !(edu.value == "I have completed the course")
        x[j].value = ''; // clear existing input
    }
}
