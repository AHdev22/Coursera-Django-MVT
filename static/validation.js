const form = document.getElementById("form");
const firstname_input = document.getElementById("firstname-input");
const email_input = document.getElementById("email-input");
const password_input = document.getElementById("password-input");
const repeat_password_input = document.getElementById("repeat-password-input");
const phoneInput = document.getElementById("phone");
const error_message = document.getElementById("error-message");

// Disable copy/paste in password fields
[password_input, repeat_password_input].forEach((input) => {
    input.addEventListener("copy", (e) => e.preventDefault());
    input.addEventListener("paste", (e) => e.preventDefault());
    input.addEventListener("cut", (e) => e.preventDefault());
});

// Submit event
form.addEventListener("submit", (e) => {
    let errors = [];

    if (firstname_input) {
        // Signup form
        errors = getSignupFormErrors(
            firstname_input.value,
            email_input.value,
            phoneInput.value,
            password_input.value,
            repeat_password_input.value
        );
    } else {
        // Login form
        errors = getLoginFormErrors(email_input.value, password_input.value);
    }

    if (errors.length > 0) {
        e.preventDefault();
        error_message.innerHTML = errors.join("<br>");
    }
});

// Signup validation function
function getSignupFormErrors(
    firstname,
    email,
    phone,
    password,
    repeatPassword
) {
    let errors = [];

    // Firstname
    if (!firstname) {
        errors.push("Username is required");
        firstname_input.parentElement.classList.add("incorrect");
    }

    // Phone (Egyptian numbers only)
    if (!phone) {
        errors.push("Phone number is required");
        phoneInput.parentElement.classList.add("incorrect");
    } else if (!/^(01)[0-2,5]{1}[0-9]{8}$/.test(phone)) {
        errors.push(
            "Phone number must be a valid Egyptian number (11 digits, starts with 010, 011, 012, or 015)"
        );
        phoneInput.parentElement.classList.add("incorrect");
    }

    // Email
    if (!email) {
        errors.push("Email is required");
        email_input.parentElement.classList.add("incorrect");
    }

    // Password
    if (!password) {
        errors.push("Password is required");
        password_input.parentElement.classList.add("incorrect");
    } else if (password.length < 8 || password.length > 16) {
        errors.push("Password must be between 8 to 16 characters.");
        password_input.parentElement.classList.add("incorrect");
    }

    // Repeat password
    if (password !== repeatPassword) {
        errors.push("Password does not match repeated password");
        password_input.parentElement.classList.add("incorrect");
        repeat_password_input.parentElement.classList.add("incorrect");
    }

    return errors;
}

// Login validation function
function getLoginFormErrors(email, password) {
    let errors = [];

    if (!email) {
        errors.push("Email is required");
        email_input.parentElement.classList.add("incorrect");
    }

    if (!password) {
        errors.push("Password is required");
        password_input.parentElement.classList.add("incorrect");
    } else if (password.length < 8 || password.length > 16) {
        errors.push("Password must be between 8 to 16 characters.");
        password_input.parentElement.classList.add("incorrect");
    }

    return errors;
}

// Clear error highlighting dynamically
const allInputs = [
    firstname_input,
    email_input,
    phoneInput,
    password_input,
    repeat_password_input,
].filter((input) => input != null);

allInputs.forEach((input) => {
    input.addEventListener("input", () => {
        if (input.parentElement.classList.contains("incorrect")) {
            input.parentElement.classList.remove("incorrect");
            error_message.innerHTML = "";
        }
    });
});
