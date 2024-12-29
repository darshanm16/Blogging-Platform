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
