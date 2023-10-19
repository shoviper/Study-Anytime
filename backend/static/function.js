// //login page
// function studentlogin(){

// }

// function lecturerlogin(){

// }

//signup page
function signup() {
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirmpassword = document.getElementById("confirmpassword").value;

    if (password !== confirmpassword) {
        alert("Error, please fill the password correctly.");
        return;
    }

    var data = {
        username: username,
        email: email,
        password: password
    };

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/signup', true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.onload = function () {
        if (xhr.status === 200) {
            alert('Sign up successful');
        } else {
            alert('Sign up failed');
        }
    };
    xhr.send(JSON.stringify(data));
}


// //resetpassword page
// function resetpassword(){
    
// }
