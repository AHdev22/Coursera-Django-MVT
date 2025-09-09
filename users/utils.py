import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    """Generate a 6-digit numeric OTP."""
    return str(random.randint(100000, 999999))

def send_verification_email(email, otp):
    """Send the OTP to user's email."""
    subject = "Your Verification Code"
    message = f"Your verification code is: {otp}\nThis code is valid for 5 minutes."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
