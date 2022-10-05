// Registration form validation




function formValidation() {

  let password = document.registration.password;
  let repeat_password = document.registration.repeat_password;
  let username = document.registration.username;
  let email = document.registration.email;

  if (ValidateEmail(email)) {
    if (allLetter(username)) {
      if (password_validation(password, 7, 12)) {
        if (matchPassword(password, repeat_password)) {
          document.getElementById("register-btn").setAttribute("type", "submit")
        }
      }
    }

  }

  return false;



  function password_validation(password, minimum, maximum) {
    var password_length = password.value.length;
    if (password_length == 0 || password_length > maximum || password_length < minimum) {
      swal("Invalid", "Password length should be 7 to 12 characters", "error");
      password.focus();
      return false;
    }
    return true;
  }

  function allLetter(username) {
    var letters = /^[A-Za-z]+/;
    if (username.value.match(letters)) {
      return true;
    }
    else {
      swal("Invalid", "Username must have alphabet characters only", "error");
      username.focus();
      return false;
    }
  }


  function ValidateEmail(email) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (email.value.match(mailformat)) {
      return true;
    }
    else {

      swal("Invalid", "Enter valid email id", "error");

    }
  }
  function matchPassword(password, repeat_password) {
    if (password.value != repeat_password.value) {
      swal("Invalid", "Passwords did not match", "error");
    } else {

      return true
    }

  }

}
// ----------------------------------------------------------------

// registration password condditioned label 

function labelVisible() {
  document.getElementById("passwordLable").style.display = "inline";
}
function labelInvisible() {
  document.getElementById("passwordLable").style.display = "none";
}



// category adding input button hide and show
function categoryInput() {
  form = document.getElementById('category-form');
  if (form.style.display == "block") {
    form.style.display = "none";
  } else {
    form.style.display = "block";
  }
}



//  post clap
function like(postId) {
  const likeCount = document.getElementById(`likes-count-${postId}`);
  console.log(likeCount)
  const likeButton = document.getElementById(`like-button-${postId}`);
  console.log(likeButton)


  fetch(`/likepost/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      console.log(data)
      likeCount.innerHTML = data["likes"];
      if (data["liked"] === true) {
        likeButton.className = "fa-solid fa-hands-clapping text-primary fa-lg";
      } else {
        likeButton.className = "fa-solid fa-hands-clapping fa-lg";
      }
    })
}



    // profile updation email, username, password validation
// ----------------------------------------

function ValidateNewEmail() {
  var email = document.emailUpdate.newEmail;


  if (ValidatesEmail(email)) {
    document.getElementById("emailUpdate_").setAttribute("type", "submit")
  }

  return false;

  function ValidatesEmail(email) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (email.value.match(mailformat)) {
      return true;
    }
    else {

      swal("Invalid", "Enter valid email id", "error");

    }
  }

}

//-----------------------------------------------

function ValidateNewname() {
  var usernames = document.nameUpdate.newUser;


  if (allLetter(usernames)) {
    document.getElementById("newUsername").setAttribute("type", "submit")
  }

  return false;

  function allLetter(username) {
    var letters = /^[A-Za-z]+/;
    if (username.value.match(letters)) {
      return true;
    }
    else {
      swal("Invalid", "Username must have alphabet characters only", "error");
      username.focus();
      return false;
    }
  }
}
// --------------------------------------------------------------

function ValidateNewPass() {
  var password = document.passwordUpdation.newPassword;
  var repeat_password = document.passwordUpdation.repeat_password;


  if (password_validation(password, 7, 12)) {

    if (matchPassword(password, repeat_password)) {
      document.getElementById("newPassBtn").setAttribute("type", "submit")
    }
  }
  return false;


  function password_validation(password, minimum, maximum) {
    var password_length = password.value.length;
    if (password_length == 0 || password_length > maximum || password_length < minimum) {
      swal("Invalid", "Password length should be 7 to 12 characters", "error");
      password.focus();
      return false;
    }
    return true;
  }

  function matchPassword(password, repeat_password) {
    if (password.value != repeat_password.value) {
      swal("Invalid", "Passwords did not match", "error");
    } else {

      return true
    }

  }

}