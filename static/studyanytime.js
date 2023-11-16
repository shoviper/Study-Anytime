// MODAL
// Function to display the modal
function displayModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "block";
}

// Check if the user is signed in
async function isUserSignedIn() {
    try {
        const response = await fetch("/verify_token", {
            method: "GET",
            credentials: "include", // Include cookies in the request
        });

        const isValid = await response.json();

        if (!isValid) {
            displayModal();
        }
    } catch (error) {
        console.error("Error checking access token validity:", error);
    }
}

// Function to check sign-in status and show modal if needed
async function checkSignInStatus() {
    await isUserSignedIn();
}

// Add click event listener to modal overlay (to prevent closing)
window.addEventListener("click", function (event) {
    var modal = document.getElementById("myModal");
    if (event.target === modal) {
        // Do nothing or show an error message since we don't want the modal to be closed
    }
});

// Check sign-in status on page load
window.onload = function () {
    checkSignInStatus();
};



//textarea
const textarea = document.querySelector("textarea");
textarea.addEventListener("keyup", e => {
    textarea.style.height = "59px";
    let scHeight= e.target.scrollHeight;
    textarea.style.height = `${scHeight}px`;
})