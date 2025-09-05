# 🍋 Little Lemon Restaurant – Django MVT Project

This project is a **restaurant website** for **Little Lemon**, built using **Django (MVT architecture)**.  
It provides a **user interface** where customers can:  
- Browse the restaurant menu  
- Register and log in securely  
- Make reservations online  

Passwords are encrypted using Django’s built-in hashing, and token-based authentication is applied to each logged-in user.  
This project focuses on the **UI side** (templates), not the Django admin panel.

---

## 🚀 Features
- **User Accounts**
  - Registration with encrypted password storage
  - Login & logout functionality
  - Token generated for each logged-in user

- **Restaurant Menu**
  - Display menu items (name, description, price)
  - Menu items stored in the database (via Django models)

- **Reservations**
  - Authenticated users can book a reservation
  - Reservation details saved in the database
  - Simple form-based UI for booking

- **Security**
  - Passwords stored using Django’s secure hashing system
  - Token authentication applied for logged-in sessions
  - CSRF protection enabled for forms

---

## 🛠️ Tech Stack
- **Backend Framework**: Django (MVT pattern)  
- **Database**: MySQL    
- **Authentication**: Custom token authentication + Django sessions  
- **Templates**: HTML, CSS (basic UI)  

---

## Project Structure
│── littlelemon/ # Django project settings
│── restaurant/ # Main app (menu + reservations)
│── users/ # User auth & tokens
│── templates/ # HTML templates (UI)
│── static/ # CSS, JS, images
│── manage.py # Django manager

## 📂 Project Structure
