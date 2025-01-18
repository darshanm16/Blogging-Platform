function toggleComments() {
  const commentsList = document.getElementById("comments-list");
  if (
    commentsList.style.display === "none" ||
    commentsList.style.display === ""
  ) {
    commentsList.style.display = "block";
  } else {
    commentsList.style.display = "none";
  }
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
      document.getElementById("like-count" + id).innerText = data.likes;
    });
}
