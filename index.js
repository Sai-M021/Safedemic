    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        var emailVerified = user.emailVerified;
        if (!emailVerified)
        {
          document.getElementById("signoutdirect").style.visibility = "hidden";
          document.getElementById("signoutdirect").disabled = true;
        }
        else
        {
            document.getElementById("signoutdirect").style.visibility = "visible";
            document.getElementById("signoutdirect").disabled = false;
        }
      }
      else {
        document.getElementById("signoutdirect").style.visibility = "hidden";
        document.getElementById("signoutdirect").disabled = true;
      }
    });

  var reportsRef = firebase.database().ref('reports');
  var selectedViol;
  var locationInfo;
  var addressInfo;
  $('#report_form').submit(function(e) {
    e.preventDefault();
    document.getElementsByName("viol_type").forEach(function(elm) {
      if (elm.checked) {
        selectedViol = elm.value;
      }
    })
    if (selectedViol == undefined)
    {
      alert('Complete form before submitting.');
    }
    else
    {
      if ($('#street_num').val() == "")
      {
        locationInfo = $('#street_num').val().concat($('#street_name').val(), ", ", $('#city').val(), ", ", $('#state').val(), ", ", $('#country').val());
        addressInfo = $('#street_num').val().concat($('#street_name').val());
      }
      else
      {
        locationInfo = $('#street_num').val().concat(" ", $('#street_name').val(), ", ", $('#city').val(), ", ", $('#state').val(), ", ", $('#country').val());
        addressInfo = $('#street_num').val().concat(" ", $('#street_name').val());
      }
      locationInfo = locationInfo.replace(/ /g,"+");
      var url = "https://maps.googleapis.com/maps/api/geocode/json?" +
          "address=" + locationInfo +
          "&key=AIzaSyBTrhGG7zVrT_eBVn_06khunxCMz23YXZs";
      var request = new Request(url);
      fetch(request).then(
          function(u){return u.json();}
      ).then(
          function (json) {
              var lat = json.results[0].geometry.location.lat;
              var lng = json.results[0].geometry.location.lng;
              var date = Date()
              if ((lat == null) || (lat == undefined) || (lng  == null) || (lng == undefined))
              {
                alert('Invalid Location');
              }
              else
              {
                var newReportsRef = reportsRef.push();
                newReportsRef.set({
                  address: addressInfo,
                  city: $('#city').val(),
                  state: $('#state').val(),
                  lat: lat,
                  long: lng,
                  num_ppl: $("#num_ppl").val(),
                  viol_type: selectedViol,
                  time: date.toString()
                });
                $('#report_form')[0].reset();
              }
          }
      )
    }
  });
  
    function signout(){
      if (firebase.auth().currentUser) {
          firebase.auth().signOut();
          window.location = "https://neilr23.github.io/Safedemic/";
        }
    }
    function openReportForm() { //Source: https://www.w3schools.com/howto/howto_css_modals.asp
        firebase.auth().onAuthStateChanged(function(user) {
          if (user) {
            var emailVerified = user.emailVerified;
            if (!emailVerified)
            {
              document.getElementById("signin_section").style.display = "block";
              alert('Email Verification Required'); 
            }
            else
            {
                document.getElementById("report_section").style.display = "block";
            }
          }
          else {
            document.getElementById("signin_section").style.display = "block";
          }
        });
    }
    function closeReportForm() { //Source: https://www.w3schools.com/howto/howto_css_modals.asp
      document.getElementById("report_section").style.display = "none";
    }
    // slide show tutorial https://www.w3schools.com/howto/howto_js_slideshow.asp
    // var slideIndex = 1;
    // showSlides(slideIndex);

    // function sideSlide(n) {
    //     showSlides(slideIndex += n);
    // }

    // function switchSlide(n) {
    //     showSlides(slideIndex = n);
    // }

    // function showSlides(n) {
    //     var slides = document.getElementsByClassName("panel");
    //     var dots = document.getElementsByClassName("page_icon");
    //     if (n > slides.length) {slideIndex = 1}
    //     if (n < 1) {slideIndex = slides.length}
    //     for (var i = 0; i < slides.length; i++) {
    //         slides[i].style.display = "none";
    //     }
    //     for (i = 0; i < dots.length; i++) {
    //         dots[i].className = dots[i].className.replace(" active", "");
    //     }
    //     slides[slideIndex-1].style.display = "block";
    //     dots[slideIndex-1].className += " active";
    // }
 function register(){

    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    if (password.length < 6) {  
      document.getElementById("login_status").innerHTML = 'Invalid password (less than 6 characters)';
      return;
    }
    firebase.auth().createUserWithEmailAndPassword(email, password).catch(function(error) {
      // Handle Errors here.
      var errorCode = error.code;
      var errorMessage = error.message;

      if (errorCode == 'auth/weak-password') {
        document.getElementById("login_status").innerHTML = 'Password is weak';
      }
      else
      {
        document.getElementById("login_status").innerHTML = errorMessage;
      }
    });
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        firebase.auth().currentUser.sendEmailVerification().then(function() {
          document.getElementById("login_status").innerHTML = "Verification Email Sent";
         });
      }
    });
  }
  function signin(){
    var continueLogin
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        if (user.emailVerified)
        {
          document.getElementById("signin_section").style.display = "none";
          return;
        }
      }
    });
      var email = document.getElementById("email").value;
      var password = document.getElementById("password").value;
      firebase.auth().signInWithEmailAndPassword(email, password).catch(function(error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;

        if (errorCode === 'auth/wrong-password') {
          document.getElementById("login_status").innerHTML = 'Invalid Password';
        }
        else {
          document.getElementById("login_status").innerHTML = errorMessage;
        }
      });
  }
  function resetpword(){
    var email = document.getElementById("email").value;
    firebase.auth().sendPasswordResetEmail(email).then(function() {
      document.getElementById("login_status").innerHTML = "Password Reset Email Sent";
    }).catch(function(error) {
      var errorCode = error.code;
      var errorMessage = error.message;
      if (errorCode == 'auth/invalid-email')
        document.getElementById("login_status").innerHTML = errorMessage;
      else if (errorCode == 'auth/user-not-found')
      {
        document.getElementById("login_status").innerHTML = errorMessage;
      }
    });
  }
    function verifyemail(){
      firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        firebase.auth().currentUser.sendEmailVerification().then(function() {
          document.getElementById("login_status").innerHTML = "Verficiation Email Sent";
         });
      }
    });
    }