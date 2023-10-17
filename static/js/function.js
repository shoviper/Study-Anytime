// //login page
// function studentlogin(){

// }

// function lecturerlogin(){

// }

//signup page
function signup(){
    var username = document.getElementById("username");
    var email = document.getElementById("email");
    var password = document.getElementById("password");
    var confirmpassword = document.getElementById("confirmpassword");

    if(password != confirmpassword){
        alert("Error, please fill the password correctly.");
        return;
    }
    
}

// //resetpassword page
// function resetpassword(){
    
// }


//test
function studentlogin() {
    if (isStudentSignedUp()) {
        alert("Login as a student successful!");
    } else {
        alert("You need to sign up as a student first!");
    }
}

function lecturerlogin() {
    if (isLecturerSignedUp()) {
        alert("Login as a lecturer successful!");
    } else {
        alert("You need to sign up as a lecturer first!");
    }
}

function isStudentSignedUp() {
    // Implement your logic to check if the user is signed up as a student
    // For example, you can check if the user's email exists in a student database
    var studentemail = document.getElementById("email").value; // Get the entered email
    // Add your logic to check if the email exists in the student database
    // For now, let's assume a simple check that the email contains "student"
    return studentemail.includes("student");
}

function isLecturerSignedUp() {
    // Implement your logic to check if the user is signed up as a lecturer
    // Similar to the isStudentSignedUp function
    var lectureremail = document.getElementById("email").value; // Get the entered email
    // Add your logic to check if the email exists in the lecturer database
    // For now, let's assume a simple check that the email contains "lecturer"
    return lectureremail.includes("lecturer");
}
