const wrapper = document.querySelector(".wrapper"),
  carousel = document.querySelector(".carousel"),
  images = document.querySelectorAll("img"),
  buttons = document.querySelectorAll(".button");
let imageIndex = 1,
  intervalId;
const autoSlide = () => {
  intervalId = setInterval(() => slideImage(++imageIndex), 2000);
};
autoSlide();
const slideImage = () => {
  imageIndex = imageIndex === images.length ? 0 : imageIndex < 0 ? images.length - 1 : imageIndex;
  carousel.style.transform = `translate(-${imageIndex * 100}%)`;
};

const updateClick = (e) => {
  clearInterval(intervalId);
  imageIndex += e.target.id === "next" ? 1 : -1;
  slideImage(imageIndex);
  autoSlide();
};

buttons.forEach((button) => button.addEventListener("click", updateClick));
wrapper.addEventListener("mouseover", () => clearInterval(intervalId));
wrapper.addEventListener("mouseleave", autoSlide);

// MODAL
// Function to display the modal
function displayModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "block";
}

// Function to close the modal
function closeModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
}

// Function to check access token validity
async function checkAccessTokenValidity() {
  try {
    const response = await fetch("/verify_token", {
      method: "GET",
      credentials: "include", // Include cookies in the request
    });

    const isValid = await response.json();

    if (!isValid) {
      displayModal();
    } else {
      // If token is valid, redirect to the next page
      window.location.href = "/studyanytime";
    }
  } catch (error) {
    console.error("Error checking access token validity:", error);
  }
}

// Add click event listener to Study Anytime link
const studyAnytimeLink = document.getElementById("studyAnytimeLink");
studyAnytimeLink.addEventListener("click", function (event) {
  // Prevent default link behavior
  event.preventDefault();
  // Check access token validity before navigating to the next page
  checkAccessTokenValidity();
});

// Add click event listener to close button
const closeButton = document.querySelector(".modal-header .close");
closeButton.addEventListener("click", closeModal);

// Add click event listener to modal overlay
window.addEventListener("click", function (event) {
  var modal = document.getElementById("myModal");
  if (event.target === modal) {
    closeModal();
  }
});