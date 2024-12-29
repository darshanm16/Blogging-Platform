document.getElementById("toggle-form").addEventListener("click", function () {
  const signupForm = document.querySelector(".form--signup");
  const loginForm = document.querySelector(".form--login");
  const toggleButton = document.getElementById("toggle-form");

  if (signupForm.classList.contains("active")) {
    // Show login form
    signupForm.classList.remove("active");
    loginForm.classList.add("active");
    toggleButton.textContent = "Create new account";
  } else {
    // Show signup form
    loginForm.classList.remove("active");
    signupForm.classList.add("active");
    toggleButton.textContent = "Already have an account?";
  }
});
