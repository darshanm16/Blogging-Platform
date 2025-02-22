function editComment(id) {
  var comment = document.getElementById("comment-para" + id);
  var editComment = `
                <div style="display: flex;margin-bottom: 0;" id="comment-edit${id}"
                class="comment-input-container comment-update">
                <input type="text" id="comment-input${id}" class="comment-input" value="${comment.innerText}">
                <div id="commentedit-btns${id}" class="comment-btns">
                  <button class="comment-btn" style="background-color: #ff7474;" onclick="cancelEdit(${id})">Cancel</button>
                  <button class="comment-btn" style="background-color: #1877f2;" onclick="updateComment(${id})">Update</button>
                </div>
              </div>`;
  comment.style.display = "none";
  comment.insertAdjacentHTML("afterend", editComment);
  var commentBtns = document.getElementById("comment-btns" + id);
  commentBtns.style.display = "none";
}

function cancelEdit(id) {
  var commentEdit = document.getElementById("comment-edit" + id);
  var comment = document.getElementById("comment-para" + id);
  var commentBtns = document.getElementById("comment-btns" + id);
  commentEdit.remove();
  comment.style.display = "contents";
  commentBtns.style.display = "block";
}

function updateComment(id) {
  var commentInput = document.getElementById("comment-input" + id).value.trim();
  if (!commentInput) {
    return;
  }
  fetch("/index/blog/updateComment/", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: id, comment: commentInput }),
  })
    .then((response) => response.json())
    .then((data) => {
      var comment = document.getElementById("comment-para" + id);
      comment.innerText = data.comment;
      cancelEdit(id);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function deleteComment(id) {
  var comment = document.getElementById("comment" + id);
  if (
    confirm(
      "Are you sure you want to delete this comment? This action cannot be undone."
    )
  ) {
    fetch("/index/blog/postComment/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: id }),
    })
      .then((response) => {
        if (response.ok) {
          comment.remove();
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

function postComment(id) {
  var comment = document.getElementById("comment-input" + id).value.trim();
  if (!comment) {
    return;
  }
  fetch("/index/blog/postComment/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: id, comment: comment }),
  })
    .then((response) => response.json())
    .then((data) => {
      var commentsSection = document.getElementById("comments-section" + id);

      var newComment = document.createElement("div");
      newComment.className = "comment";
      newComment.id = "comment" + data.comment_id;
      newComment.innerHTML = `
        <div class="comment-content">
          <strong>${data.user_name || "Anonymous"}</strong><br>
          <span  style="display:content" id="comment-para${data.comment_id}">${
        data.comment || "No content"
      }</span>
          <div style="display: block;" id="comment-btns${
            data.comment_id
          }" class="comment-btns">
            <button class="comment-btn" onclick="editComment('${
              data.comment_id
            }')">Edit</button>
            <button class="comment-btn" style="background-color: #ff7474;" onclick="deleteComment('${
              data.comment_id
            }')">Delete</button>
          </div>
        </div>
      `;
      commentsSection.insertBefore(newComment, commentsSection.children[1]);
      document.getElementById(
        "n-comments" + id
      ).innerText = `💬 Comment (${data.total_comments})`;

      // Clear input field after successful post
      document.getElementById("comment-input" + id).value = "";
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function blogLike(id) {
  fetch("/index/blog/like/", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: id }),
  })
    .then((response) => response.json())

    .then((data) => {
      const heartIcon = data.likes > 0 ? "❤️" : "🤍";
      document.getElementById(
        "likes" + id
      ).innerText = `${heartIcon} ${data.likes} likes`;
    });
}

function readmore(id) {
  var blog_para = document.getElementsByClassName("blog-para" + id)[0];
  if (blog_para.style.height === "" || blog_para.style.height === "90px") {
    blog_para.style.height = "auto";
    blog_para.style.overflow = "visible";
    document.getElementsByClassName("readmore")[0].innerText = "Read less";
  } else {
    blog_para.style.height = "90px";
    blog_para.style.overflow = "hidden";
    document.getElementsByClassName("readmore")[0].innerText = "Read more...";
  }
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
