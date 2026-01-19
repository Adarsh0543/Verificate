const loginForm = document.querySelector("#login_form");
const emailInput = document.querySelector("#user_email");
const passwordInput = document.querySelector("#user_password");
const eye = document.getElementById("eye");

let eyeView = false;
if (eye) {
  eye.addEventListener("click", () => {
    eyeView = !eyeView;
    if (eyeView) {
      eye.classList.remove("fa-eye-slash");
      eye.classList.add("fa-eye");
      passwordInput.setAttribute("type", "text");
    } else {
      eye.classList.remove("fa-eye");
      eye.classList.add("fa-eye-slash");
      passwordInput.setAttribute("type", "password");
    }
  });
}

// Remove the form submission interception so that the form submits naturally
// and is handled by your Flask backend.
