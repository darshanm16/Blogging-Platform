function changebyoldpass() {
  var oldpass = document.getElementById("oldpass").value;
  var newpass = document.getElementById("newpass").value;
  var confirmpass = document.getElementById("confirmpass").value;

  if (!oldpass || !newpass || !confirmpass) {
    alert("All fields are required.");
    return;
  }

  if (newpass !== confirmpass) {
    alert("Passwords do not match.");
    return;
  }
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

let byotp = `        <div class="form-group" id="byotp">
          <label for="passotp">OTP Verification</label>
          <div style="display: flex ;gap: 12px;">
            <input type="passotp" id="passotp" name="passotp" maxlength="6" style="flex: 3;">
            <button id="button" type="button" style="flex: 1;">Send otp</button>
            <button id="button" type="button" style="flex: 1;background-color:#04aa6d">Verify</button>
          </div>
          <p id="otpmsg"></p>
        </div>`;
let byoldpass = `        <div class="form-group" id="byoldpass">
          <label for="oldpass">Old Password</label>
          <input type="password" id="oldpass" name="oldpass">
        </div>`;

function changemethod() {
  if (document.getElementById("byotp")) {
    document.getElementById("byotp").remove();
    document.getElementById("method").insertAdjacentHTML("afterend", byoldpass);
    document
      .getElementsByClassName("passchangebtn")[0]
      .setAttribute("onclick", "changebyoldpass()");
    return;
  }
  if (document.getElementById("byoldpass")) {
    document.getElementById("byoldpass").remove();
    document.getElementById("method").insertAdjacentHTML("afterend", byotp);
    document
      .getElementsByClassName("passchangebtn")[0]
      .setAttribute("onclick", "changebyotp()");
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
