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
      newComment.innerHTML = `
        <div class="comment-content">
          <strong>${data.user_name || "Anonymous"}</strong><br>
          <span>${data.comment || "No content"}</span>
        </div>
      `;
      commentsSection.insertBefore(newComment, commentsSection.children[1]);
      document.getElementById("n-comments" + id).innerText = `💬 Comment (${data.total_comments})`;

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

// Previous JavaScript functionality remains
document.querySelectorAll(".action-btn").forEach((button) => {
  button.addEventListener("click", function () {
    if (this.textContent.includes("Like")) {
      this.style.color =
        this.style.color === "rgb(24, 119, 242)" ? "#65676b" : "#1877f2";
    }
  });
});

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
