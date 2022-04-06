const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const regButton = document.getElementById("reg-form-go");
const regForm = document.getElementById("reg-form");


regButton.addEventListener("click", (e) => {
    e.preventDefault();
    loginForm.style.display = 'none';
    regForm.style.display = 'grid';
    
})