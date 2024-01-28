// Logout dropdown
document.addEventListener("DOMContentLoaded", function () {
  const profileBtn = document.querySelector(".profile-btn");
  const dropdownContainer = document.querySelector(".dropdown-container");
  profileBtn.addEventListener("click", function (e) {
    e.preventDefault();
    dropdownContainer.classList.toggle("hide-logout");
  });
});

// body transparent when sign up form open
document.addEventListener("DOMContentLoaded", function () {
  const createAccountBtn = document.querySelector(".create-account-btn");
  const bodyWrapper = document.querySelector(".body-wrapper");

  const closeRegistrationBtn = document.querySelector(
    ".close-registration-form"
  );
  createAccountBtn.addEventListener("click", function (e) {
    // e.preventDefault();
    // alert("clicked");
    bodyWrapper.style.display = "block";
  });

  closeRegistrationBtn.addEventListener("click", function () {
    bodyWrapper.style.display = "none";
  });
});

// body transparent for post upload form
document.addEventListener("DOMContentLoaded", function () {
  const fileUploadBtn = document.querySelector("#whats-on-mind");
  const bodyWrapper = document.querySelector(".body-wrapper-two");

  const closeFileUploadBtn = document.querySelector(".close-post-upload");
  fileUploadBtn.addEventListener("click", function (e) {
    bodyWrapper.style.display = "block";
  });

  closeFileUploadBtn.addEventListener("click", function () {
    bodyWrapper.style.display = "none";
  });
});

// opening file upload input on clicking image or video in post upload pop up
document.addEventListener("DOMContentLoaded", function () {
  const imageBtn = document.querySelector(".upload-icon-image");
  const videoBtn = document.querySelector(".upload-icon-video");
  const fileInput = document.querySelector(".file-upload-inp");
  imageBtn.addEventListener("click", function () {
    fileInput.classList.toggle("file-upload-imp-show");
  });
  videoBtn.addEventListener("click", function () {
    fileInput.classList.toggle("file-upload-imp-show");
  });
});

// deleting post from UI

document.addEventListener("click", function (e) {
  console.log(e.target);
});
