#🍋 Little Lemon Restaurant — Django MVT Project

A simple, educational restaurant website built with Django (MVT) that demonstrates user authentication, menu display, and reservation booking. Designed as a learning project — clean, minimal UI built with plain HTML/CSS/JS, and backend features implemented from scratch.

##🚀 Quick overview

Little Lemon lets customers:
Browse the restaurant menu.
Register, log in, and log out securely.
Book reservations online and view reservations by time slot.
Authenticate using an email OTP (one-time password) in addition to session-based login.
This project is intentionally simple so you can learn the full stack flow: templates → forms → views → models → database.

##✅ Features

###Authentication & Security

User registration with Django’s secure password hashing.
Session-based login/log out (Django auth).
Email OTP flow: user receives a one-time code to their email for verification / login. OTP implementation uses backend Django logic and frontend HTML/CSS/JavaScript — written from scratch (no third-party OTP UI).
Token-based authentication available for API endpoints (if used).
CSRF protection enabled for all forms.

###Menu

Menu items stored in MySQL via Django models.
Template-driven menu pages display item name, description, price, and image.

###Reservations

Authenticated users can make reservations via a simple form.
Reservations saved in the database and displayed grouped by time slot.
Admin / staff view (optional) to see all reservations by date/time slot.

###UI

Frontend built with plain HTML, CSS and vanilla JavaScript for behavior (form validation, OTP input flow, UI interactions).
Lightweight, responsive layout focused on learning rather than heavy styling frameworks.

##🛠 Tech Stack

Backend: Django (MVT)
Database: MySQL
Frontend: HTML / CSS / JavaScript (no heavy frameworks)
Email: SMTP (Django EmailMessage) for OTP delivery
Authentication: Django sessions + email OTP + optional token auth

##🔐 Email OTP (One-Time Password) — how it works (high level)

User requests login/verification with email (or during registration).
Backend generates a short, time-limited OTP (stored hashed or with expiry in DB).
Django sends OTP to the user’s email via configured SMTP settings.
Frontend shows an OTP input form (HTML + JS) for the user to paste/type the code.
Backend verifies OTP, logs the user in / completes verification, and invalidates the OTP.

##Notes:
OTPs expire after a short time window (1 minute).
OTPs are single-use; upon successful verification they are invalidated.
Implement rate-limiting to prevent abuse (throttle OTP requests per email).

##📂 Project structure (summary)

littlelemon/ — Django project settings
restaurant/ — main app (models, views, templates for menu + reservations)
users/ — auth, OTP models & views, token endpoints
templates/ — HTML templates (menu, auth, OTP form, reservations)

static/ — CSS, JS, images

manage.py
