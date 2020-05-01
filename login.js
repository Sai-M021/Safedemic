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
          window.location = "https://neilr23.github.io/safedemic-lumiata/";
          document.getElementById("signoutdirect").style.visibility = "visible";
          document.getElementById("signoutdirect").disabled = false;
        }
      }
      else {
        document.getElementById("signoutdirect").style.visibility = "hidden";
        document.getElementById("signoutdirect").disabled = true;
      }
    });

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
  				window.location = "https://neilr23.github.io/safedemic-lumiata/";
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
    function signout(){
      if (firebase.auth().currentUser) {
          firebase.auth().signOut();
          window.location = "https://neilr23.github.io/safedemic-lumiata/";
        }
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