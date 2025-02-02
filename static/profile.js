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

// Edit Profile Button
document
  .querySelector(".edit-profile-btn")
  .addEventListener("click", function () {
    alert("Edit profile functionality would go here!");
  });

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
  document.getElementById("edited-content").value = content;
}

function closeEditModal() {
  editOverlay.style.display = "none";
  currentEditPost = 0;
}

function saveEdit() {
  var title = document
    .getElementById("edited-title")
    .value.trim();
  var content = document
    .getElementById("edited-content")
    .value.trim();

  if (!title || !content) {
    alert("Title or content element not found.");
    return;
  }

  fetch("/profile/modify-blog/", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: currentEditPost, title: title, content: content }),
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