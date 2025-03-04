function changeStatus() {
  fetch("/profile/change-status/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status) {
        alert("Profile status changed to public.");
        document.getElementById("profile-status").textContent = "Profile Status : Public";
      } else {
        alert("Profile status changed to private.");
        document.getElementById("profile-status").textContent = "Profile Status : Private";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while changing the status.");
    });
}

function shareProfile(user_name) {
  var url = window.location.origin + "/";
  var blog_url = url + user_name + "/";
  if (navigator.share) {
    navigator
      .share({
        title: user_name,
        text: "Check out this profile!",
        url: blog_url,
      })
      .catch((error) => console.log("Error sharing:", error));
  } else {
    navigator.clipboard.writeText(blog_url);
    alert("Link copied to clipboard!");
  }
}

function blockComments(id) {
  fetch("/profile/block-comments/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: id }),
  })
    .then((response) => {
      if (response.ok) {
        location.reload();
      } else {
        return response.json().then((data) => {
          alert(data.message || "Failed to block comments.");
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while blocking comments.");
    });
}

function changebyotp() {
  var newpass = document.getElementById("newpass").value;
  var confirmpass = document.getElementById("confirmpass").value;
  if (!newpass || !confirmpass) {
    alert("All fields are required.");
    return;
  }
  if (newpass !== confirmpass) {
    alert("Passwords do not match.");
    return;
  }
  fetch("/profile/change-by-otp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ newpass: newpass }),
  })
    .then((response) => {
      if (response.ok) {
        location.reload();
        alert("Password changed successfully.");
      } else {
        return response.json().then((data) => {
          location.reload();
          alert("Failed to change the password.");
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while changing the password.");
    });
}

function verifyresetotp() {
  var otp = document.getElementById("passotp").value;
  if (!otp) {
    alert("OTP is required.");
    return;
  }
  fetch("/profile/verify-reset-otp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ otp: otp }),
  })
    .then((response) => {
      if (response.ok) {
        document.getElementById("byotp").remove();
        document.getElementById("newpassinp").style.display = "block";
        document
          .getElementById("passchangebtn")
          .setAttribute("onclick", "changebyotp()");
      } else {
        return response.json().then((data) => {
          document.getElementById("otpmsg").textContent = "Invalid OTP.";
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while verifying OTP.");
    });
}

function sendresetotp() {
  document.getElementById("passotp").value = "";
  document.getElementById("sendbtn").innerText = "Sending...";
  fetch("/profile/send-reset-otp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (response.ok) {
        document.getElementById("otpmsg").textContent =
          "OTP sent please check your email.";
        document.getElementById("passotp").focus();
        document.getElementById("sendbtn").innerText = "Resend";
        document
          .getElementById("verifybtn")
          .setAttribute("onclick", "verifyresetotp()");
      } else {
        return response.json().then((data) => {
          document.getElementById("otpmsg").textContent = "Failed to send OTP.";
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("otpmsg").textContent =
        "An error occurred while sending OTP.";
    });
}

function changebyoldpass() {
  var oldpass = document.getElementById("oldpass").value;
  var newpass = document.getElementById("newpass").value;
  var confirmpass = document.getElementById("confirmpass").value;

  if (!oldpass || !newpass || !confirmpass) {
    alert("All fields are required.");
    return;
  }

  if (oldpass == newpass) {
    alert("New password cannot be same as old password.");
    document.getElementById("newpass").value = "";
    document.getElementById("confirmpass").value = "";
    document.getElementById("newpass").focus();
    return;
  }

  if (newpass !== confirmpass) {
    alert("Passwords do not match.");
    document.getElementById("confirmpass").value = "";
    document.getElementById("confirmpass").focus();
    return;
  }
  document.getElementById("passchangebtn").innerText = "Submitting...";
  fetch("/profile/change-old-password/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ oldpass: oldpass, newpass: newpass }),
  })
    .then((response) => {
      if (response.ok) {
        location.reload();
        alert("Password changed successfully.");
        closechangepass();
      } else {
        return response.json().then((data) => {
          alert(data.message || "Failed to change the password.");
          document.getElementById("oldpass").value = "";
          document.getElementById("oldpass").focus();
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while changing the password.");
    });
}

function showchangepass() {
  document.getElementById("changepass").style.display = "flex";
}

function closechangepass() {
  document.getElementById("changepass").style.display = "none";
}

let byotp = `<div class="form-group" id="byotp">
          <label for="passotp">OTP Verification</label>
          <div style="display: flex ;gap: 12px;">
            <input type="passotp" id="passotp" name="passotp" maxlength="6" style="flex: 3;" required>
            <button class="button" id="sendbtn" type="button" style="flex: 1;" onclick="sendresetotp()">Send</button>
            <button class="button" id="verifybtn" type="button" style="flex: 1;background-color:#04aa6d">Verify</button>
          </div>
          <p id="otpmsg"></p>
        </div>`;
let byoldpass = `<div class="form-group" id="byoldpass">
          <label for="oldpass">Old Password</label>
          <input type="password" id="oldpass" name="oldpass">
        </div>`;

function changemethod() {
  if (document.getElementById("byotp")) {
    document.getElementById("byotp").remove();
    document.getElementById("method").insertAdjacentHTML("afterend", byoldpass);
    document
      .getElementById("passchangebtn")
      .setAttribute("onclick", "changebyoldpass()");
    document.getElementById("newpassinp").style.display = "block";
    return;
  }
  if (document.getElementById("byoldpass")) {
    document.getElementById("byoldpass").remove();
    document.getElementById("method").insertAdjacentHTML("afterend", byotp);
    document.getElementById("passchangebtn").removeAttribute("onclick");
    document.getElementById("newpassinp").style.display = "None";
    return;
  }
}

function removeSavedblog(id) {
  fetch("/profile/remove-saved-blog/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: id }),
  })
    .then((response) => {
      if (response.ok) {
        document.getElementById("saved-blog" + id).remove();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while removing the blog.");
    });
}

function showSavedBlogs() {
  document.getElementById("savedblogshead").style.border = "1px solid black";
  document.getElementById("myblogshead").style.border = "1px solid white";
  document.getElementById("myblogs").style.display = "none";
  document.getElementById("savedblogs").style.display = "block";
}
function showMyBlogs() {
  document.getElementById("myblogshead").style.border = "1px solid black";
  document.getElementById("savedblogshead").style.border = "1px solid white";
  document.getElementById("savedblogs").style.display = "none";
  document.getElementById("myblogs").style.display = "block";
}

function cancelEditprofile() {
  document.getElementById("edit-profile").style.display = "none";
}

function editProfile() {
  document.getElementById("edit-profile").style.display = "flex";
}

// New comment functionality
function setupPostInteractions(post) {
  // Comment toggle
  const commentToggle = post.querySelector(".comment-toggle");
  const commentsSection = post.querySelector(".comments-section");
  if (commentToggle && commentsSection) {
    commentToggle.addEventListener("click", () => {
      commentsSection.classList.toggle("show");
    });
  }
}

// Set up interactions for existing posts
document.querySelectorAll(".post-card").forEach(setupPostInteractions);

function readmore(id) {
  var blog = document.getElementsByClassName("post-content" + id)[0];
  var readMoreButton = document.getElementsByClassName("readmore" + id)[0];

  if (blog.style.height === "63px" || blog.style.height === "") {
    blog.style.height = "auto";
    readMoreButton.innerHTML = "Read less";
  } else {
    blog.style.height = "63px";
    readMoreButton.innerHTML = "Read more...";
  }
}

// Post menu functionality
document.querySelectorAll(".post-menu-btn").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    const menu = button.nextElementSibling;
    document.querySelectorAll(".post-menu-content.show").forEach((m) => {
      if (m !== menu) m.classList.remove("show");
    });
    menu.classList.toggle("show");
  });
});

// Close menus when clicking outside
document.addEventListener("click", () => {
  document.querySelectorAll(".post-menu-content.show").forEach((menu) => {
    menu.classList.remove("show");
  });
});

// Edit functionality
let currentEditPost = 0;
const editOverlay = document.querySelector(".edit-overlay");
const editContent = document.querySelector(".edit-content");

function editPost(id) {
  currentEditPost = id;
  editOverlay.style.display = "flex";
  document.getElementById("edited-title").value = document.getElementById(
    "blog-title" + id
  ).textContent;
  let content = document.getElementById("blog-content" + id).innerHTML;
  content = content.replace(/<br>/g, "\n");
  document.getElementById("edited-content").value = content.trim();
}

function closeEditModal() {
  editOverlay.style.display = "none";
  currentEditPost = 0;
}

function saveEdit() {
  var title = document.getElementById("edited-title").value.trim();
  var content = document.getElementById("edited-content").value.trim();

  if (!title || !content) {
    alert("Title or content element not found.");
    return;
  }

  fetch("/profile/modify-blog/", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: currentEditPost,
      title: title,
      content: content,
    }),
  })
    .then((response) => {
      if (response.ok) {
        location.reload();
      } else {
        return response.json().then((data) => {
          alert(data.message || "Failed to edit the blog.");
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while editing the blog.");
    });
}

// Delete functionality
function deletePost(id) {
  if (
    confirm(
      "Are you sure you want to delete this post? This action cannot be undone."
    )
  ) {
    fetch("/profile/modify-blog/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: id }),
    })
      .then((response) => {
        if (response.ok) {
          location.reload();
        } else {
          alert("Failed to delete the blog.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while deleting the blog.");
      });
  }
}

// Close modal when clicking outside
editOverlay.addEventListener("click", (e) => {
  if (e.target === editOverlay) {
    closeEditModal();
  }
});

// Close modal with escape key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeEditModal();
  }
});

function updateAnanymous(id) {
  fetch("/profile/modify-anonymous/", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: id }),
  })
    .then((response) => {
      if (response.ok) {
        location.reload();
      } else {
        return response.json().then((data) => {
          alert(data.message || "Failed to update the anonymous setting.");
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while updating the anonymous setting.");
    });
}
