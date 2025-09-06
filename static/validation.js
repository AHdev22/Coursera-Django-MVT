document.addEventListener("DOMContentLoaded", () => {
    // Grab elements (some may be null depending on the page)
    const form = document.getElementById("form");
    const firstname_input = document.getElementById("firstname-input");
    const email_input = document.getElementById("email-input");
    const password_input = document.getElementById("password-input");
    const repeat_password_input = document.getElementById(
        "repeat-password-input"
    );
    const phoneInput = document.getElementById("phone");
    const error_message = document.getElementById("error-message");

    if (!form) return; // If no form exists, stop execution

    // Disable copy/paste/cut on password fields
    [password_input, repeat_password_input].filter(Boolean).forEach((input) => {
        input.addEventListener("copy", (e) => e.preventDefault());
        input.addEventListener("paste", (e) => e.preventDefault());
        input.addEventListener("cut", (e) => e.preventDefault());
    });

    // Submit event
    form.addEventListener("submit", (e) => {
        let errors = [];

        if (firstname_input) {
            // Signup form validation
            errors = getSignupFormErrors(
                firstname_input.value.trim(),
                email_input.value.trim(),
                phoneInput.value.trim(),
                password_input.value,
                repeat_password_input.value
            );
        } else {
            // Login form validation
            errors = getLoginFormErrors(
                email_input.value.trim(),
                password_input.value
            );
        }

        if (errors.length > 0) {
            e.preventDefault(); // Stop form submission
            error_message.innerHTML = errors.join("<br>");
        }
    });

    // Clear error highlighting dynamically
    [
        firstname_input,
        email_input,
        phoneInput,
        password_input,
        repeat_password_input,
    ]
        .filter(Boolean)
        .forEach((input) => {
            input.addEventListener("input", () => {
                input.parentElement.classList.remove("incorrect");
                if (error_message) error_message.innerHTML = "";
            });
        });
});

// Signup validation function
function getSignupFormErrors(username, email, phone, password, repeatPassword) {
    let errors = [];

    // Username
    if (!username) {
        errors.push("Username is required");
        if (document.getElementById("firstname-input"))
            document
                .getElementById("firstname-input")
                .parentElement.classList.add("incorrect");
    }

    // Phone (Egyptian numbers only)
    if (!phone) {
        errors.push("Phone number is required");
        if (document.getElementById("phone"))
            document
                .getElementById("phone")
                .parentElement.classList.add("incorrect");
    } else if (!/^(010|011|012|015)[0-9]{8}$/.test(phone)) {
        errors.push(
            "Phone number must be a valid Egyptian number (11 digits, starts with 010, 011, 012, or 015)"
        );
        if (document.getElementById("phone"))
            document
                .getElementById("phone")
                .parentElement.classList.add("incorrect");
    }

    // Email
    if (!email) {
        errors.push("Email is required");
        if (document.getElementById("email-input"))
            document
                .getElementById("email-input")
                .parentElement.classList.add("incorrect");
    }

    // Password
    if (!password) {
        errors.push("Password is required");
        if (document.getElementById("password-input"))
            document
                .getElementById("password-input")
                .parentElement.classList.add("incorrect");
    } else if (password.length < 8 || password.length > 16) {
        errors.push("Password must be between 8 to 16 characters.");
        if (document.getElementById("password-input"))
            document
                .getElementById("password-input")
                .parentElement.classList.add("incorrect");
    }

    // Repeat password
    if (password !== repeatPassword) {
        errors.push("Password does not match repeated password");
        if (document.getElementById("password-input"))
            document
                .getElementById("password-input")
                .parentElement.classList.add("incorrect");
        if (document.getElementById("repeat-password-input"))
            document
                .getElementById("repeat-password-input")
                .parentElement.classList.add("incorrect");
    }

    return errors;
}

// Login validation function
function getLoginFormErrors(email, password) {
    let errors = [];

    if (!email) {
        errors.push("Email is required");
        if (document.getElementById("email-input"))
            document
                .getElementById("email-input")
                .parentElement.classList.add("incorrect");
    }

    if (!password) {
        errors.push("Password is required");
        if (document.getElementById("password-input"))
            document
                .getElementById("password-input")
                .parentElement.classList.add("incorrect");
    } else if (password.length < 8 || password.length > 16) {
        errors.push("Password must be between 8 to 16 characters.");
        if (document.getElementById("password-input"))
            document
                .getElementById("password-input")
                .parentElement.classList.add("incorrect");
    }

    return errors;
}
