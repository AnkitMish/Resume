// Change the current window whown by toggling the active class

$( '.main-menu a').on('click', function(){

    var activeClass = $(this).attr('href').substring(1);

    setTimeout(function() {

        $( '.content.active' ).removeClass( 'active' );
        $( '.' + activeClass ).addClass( 'active' );

        $('html, body').animate({
            scrollTop: $($('.' + activeClass)).offset().top
        }, 500);

    }, 300);

    if (activeClass === 'portfolio') {
        setTimeout(function() {
            $('filter-controls li')[0].click();
        },300);
    }

})

var type = window.location.hash.substring(1);

if (type) {

    $('.content.active').removeClass( 'active' );

    $( '.' + type ).addClass('active')

}

// Adds active class to the current portfolio item selected
$('.filter-controls li').on('click', function(){
    if (! $(this).hasClass('active')) {
        $('.filter-controls li.active').removeClass('active');
        $(this).addClass('active');
    }
})


function validateForm() {
    var name =  document.getElementById('name').value;
    console.log('name', name);
    if (name == "") {
        document.querySelector('.status').innerHTML = "Name cannot be empty";
        return false;
    }
    var email =  document.getElementById('email').value;
    console.log('email', email);
    if (email == "") {
        document.querySelector('.status').innerHTML = "Email cannot be empty";
        return false;
    } else {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(!re.test(email)){
            document.querySelector('.status').innerHTML = "Email format invalid";
            return false;
        }
    }
    var subject =  document.getElementById('subject').value;
    console.log('subject', subject);
    if (subject == "") {
        document.querySelector('.status').innerHTML = "Subject cannot be empty";
        return false;
    }
    var message =  document.getElementById('message').value;
    console.log('message', message);
    if (message == "") {
        document.getElementsByClassName('status').innerHTML = "Message cannot be empty";
        return false;
    }
    document.getElementsByClassName('status').innerHTML = "Sending...";
  }

// Form asynchronous sending
document.getElementsByClassName('status').innerHTML = "Sending...";
formData = {
    'name'     : $('input[name=name]').val(),
    'email'    : $('input[name=email]').val(),
    'subject'  : $('input[name=subject]').val(),
    'message'  : $('textarea[name=message]').val()
};


$.ajax({
    url : "mail.php",
    type: "POST",
    data : formData,
    success: function(data, textStatus, jqXHR)
    {

        $('#status').text(data.message);
        if (data.code) //If mail was sent successfully, reset the form.
        $('#contact-form').closest('form').find("input[type=text], textarea").val("");
    },
    error: function (jqXHR, textStatus, errorThrown)
    {
        $('#status').text(jqXHR);
    }
});

// Filterizr
var options = {};
var filterizr = new Filterizr('.filter-container', options);

$( '.popup-link' ).magnificPopup({
    type: 'image'
});