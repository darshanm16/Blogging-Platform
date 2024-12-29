document.addEventListener("DOMContentLoaded", () => {
  const showCommentButtons = document.querySelectorAll(".show-comments-btn");

  showCommentButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const commentSectionId = button.getAttribute("data-comment-id");
      const commentSection = document.getElementById(
        `comments-${commentSectionId}`
      );

      if (
        commentSection.style.display === "none" ||
        commentSection.style.display === ""
      ) {
        commentSection.style.display = "block";
        button.textContent = "Hide Comments";
      } else {
        commentSection.style.display = "none";
        button.textContent = "Show Comments";
      }
    });
  });
});
function toggleComments(button) {
  const commentSection = button
    .closest(".card")
    .querySelector(".comment-section");
  commentSection.style.display =
    commentSection.style.display === "block" ? "none" : "block";
  button.textContent =
    commentSection.style.display === "block"
      ? "Hide Comments"
      : "Show Comments";
}
