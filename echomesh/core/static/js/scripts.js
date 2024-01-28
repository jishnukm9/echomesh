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
  const fileInputImage = document.querySelector(".file-upload-inp-image");
  const fileInputVideo = document.querySelector(".file-upload-inp-video");
  imageBtn.addEventListener("click", function () {
    if (fileInputVideo.classList.contains("file-upload-inp-show")) {
      fileInputVideo.classList.remove("file-upload-inp-show");
    }
    fileInputImage.classList.toggle("file-upload-inp-show");
    // if (fileInputVideo.contains(''))
    // fileInputVideo.style.display = "none";
  });
  videoBtn.addEventListener("click", function () {
    if (fileInputImage.classList.contains("file-upload-inp-show")) {
      fileInputImage.classList.remove("file-upload-inp-show");
    }
    fileInputVideo.classList.toggle("file-upload-inp-show");
    // fileInputImage.style.display = "none";
  });
});

// deleting post from UI
document.addEventListener("DOMContentLoaded", function () {
  const postContainer = document.querySelectorAll(".middle-content-two-child");

  postContainer.forEach((elem) => {
    elem.addEventListener("click", function (e) {
      if (e.target.classList.contains("post-close-btn")) {
        // Apply fade out transition
        e.currentTarget.style.transition = "display 2s";
        e.currentTarget.style.display = "none";
      }
    });
  });
});

// Liking and Disliking a post

document.addEventListener("DOMContentLoaded", function () {
  const likeBtn = document.querySelectorAll(".post-like-btn");

  likeBtn.forEach((element) => {
    element.addEventListener("click", function (e) {
      e.preventDefault();
      const elemTarget = e.target;
      const elem = e.currentTarget;
      if (elem.classList.contains("not-liked")) {
        const postId = elem.dataset.postId;
        const userId = elem.dataset.userId;
        console.log("post-id", postId, "userid", userId);

        const requestData = {
          post_id: postId,
          user_id: userId,
        };
        const csrftoken = csrf_token;

        fetch("/like-post/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify(requestData),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }

            return response.json();
          })
          .then((data) => {
            console.log("Success:", data);
            if (data.Response == "Success") {
              let likeIcon = elem.firstElementChild;
              let likeText = elem.lastElementChild;
              likeIcon.style.color = "blue";
              likeText.textContent = "Like";
              likeText.style.color = "blue";

              let likesCountElement = elem
                .closest(".middle-content-two-child")
                .querySelector(".likes-count").firstElementChild;
              console.log("likesCountElem-", likesCountElement);
              let likeCount = likesCountElement.textContent;
              elem
                .closest(".middle-content-two-child")
                .querySelector(".likes-count").firstElementChild.textContent =
                parseInt(likeCount) + 1;

              elem.classList.remove("not-liked");
              elem.classList.add("post-liked");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      } else if (elem.classList.contains("post-liked")) {
        const postId = elem.dataset.postId;
        const userId = elem.dataset.userId;
        console.log("post-id", postId, "userid", userId);

        const requestData = {
          post_id: postId,
          user_id: userId,
        };
        const csrftoken = csrf_token;

        fetch("/dislike-post/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify(requestData),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }

            return response.json();
          })
          .then((data) => {
            console.log("Success:", data);
            if (data.Response == "Success") {
              let likeIcon = elem.firstElementChild;
              let likeText = elem.lastElementChild;
              likeIcon.style.color = "inherit";
              likeText.style.color = "inherit";

              let likesCountElement = elem
                .closest(".middle-content-two-child")
                .querySelector(".likes-count").firstElementChild;
              console.log("likesCountElem-", likesCountElement);
              let likeCount = likesCountElement.textContent;
              elem
                .closest(".middle-content-two-child")
                .querySelector(".likes-count").firstElementChild.textContent =
                parseInt(likeCount) - 1;

              elem.classList.add("not-liked");
              elem.classList.remove("post-liked");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }
    });
  });
});
