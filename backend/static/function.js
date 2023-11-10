// //login page
// function studentlogin(){

// }

// function lecturerlogin(){

// }

//signup page

function signup() {
    // Get the form element
    const form = document.getElementById("signup-form");
    console.log("signup");
    // Create an XMLHttpRequest or use Fetch API to send the form data to the FastAPI route
    const formData = new FormData(form);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/user/signUp/", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Handle the response from the FastAPI route
                console.log(xhr.responseText);
            } else {
                // Handle errors
                console.error(xhr.statusText);
            }
        }
    };

    // Send the form data
    xhr.send(formData);
}

function login() {
   
}

// //resetpassword page
// function resetpassword(){
    
// }
