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
  var blog_para = document.getElementsByClassName("blog-para"+id)[0];
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
