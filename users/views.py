# Create your views here.
from cProfile import Profile
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login,get_user_model,logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Profile
from .utils import send_verification_email
from django.contrib.auth.models import User
from django.conf import settings
import re
from django.core.files.base import ContentFile
import base64




def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST['password1'])  # manually set password
            user.save()
            return redirect('home_show')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        next_url = request.GET.get('next', 'home_show')  # default redirect

        user = authenticate(request, username=email, password=password)
        
        if user:
            profile, created = Profile.objects.get_or_create(user=user)
            code = profile.generate_verification_code()
            send_verification_email(user.email, code)

            request.session['otp_user_id'] = user.id
            request.session['next_url'] = next_url

            messages.info(request, "A verification code has been sent to your email.")
            return redirect('verify_otp')  # direct URL
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")



def resend_code(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login_view')

    user = User.objects.get(id=user_id)
    profile, created = Profile.objects.get_or_create(user=user)

    # Generate new OTP and reset attempts
    code = profile.generate_verification_code()
    send_verification_email(user.email, code)
    messages.success(request, "Verification code has been resent to your email.")
    
    return redirect('verify_otp')



def request_otp(request, user):
    profile, _ = Profile.objects.get_or_create(user=user)
    code = profile.generate_verification_code()
    send_verification_email(user.email, code)

    request.session['otp_user_id'] = user.id
    messages.info(request, "A verification code has been sent to your email.")
    return redirect("verify_otp")



from django.contrib.auth import login, get_user_model
User = get_user_model()

def verify_otp(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login_view')

    user = User.objects.get(id=user_id)
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        code = request.POST.get("code")

        if not profile.code_is_valid():
            messages.error(request, "Code expired. Please request a new one.")
        elif not profile.can_attempt():
            messages.error(request, "You have exceeded the maximum attempts. Request a new code.")
        elif code != profile.verification_code:
            profile.code_attempts += 1
            profile.save()
            messages.error(request, f"Incorrect code. Remaining attempts: {3 - profile.code_attempts}")
        else:
            # ✅ Success
            backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=backend)

            # Clear OTP after success
            profile.verification_code = None
            profile.code_attempts = 0
            profile.save()
            return redirect(request.session.get('next_url', 'home_show'))

    expiry_time = int(profile.code_created_at.timestamp() + settings.OTP_VALIDITY_MINUTES*60) if profile.code_created_at else 0
    attempts_left = 3 - profile.code_attempts

    return render(request, "verify.html", {
        "email": user.email,
        "expiry_time": expiry_time,
        "attempts_left": attempts_left
    })



@require_POST
def logout_view(request):
    logout(request)
    return redirect('home_show')   # change to your landing page



@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":

        if "update_profile" in request.POST:
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()
            cropped_image = request.POST.get("cropped_image")
            raw_image = request.FILES.get("image")

            # ---- Email validation ----
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messages.error(request, "❌ Invalid email format.")
                return redirect("edit_profile")

            # ---- Phone validation (Egypt format only, but no verification SMS) ----
            if phone and not re.match(r"^01[0-2,5][0-9]{8}$", phone):
                messages.error(request, "❌ Invalid Egyptian phone number (010/011/012/015).")
                return redirect("edit_profile")

            # ---- Email update with verification ----
            if email != user.email:
                user.email = email
                user.save()
                profile.email_verified = False   # custom field in Profile model
                profile.save()
                code = profile.generate_verification_code()
                send_verification_email(user.email, code) 
                messages.info(request, "📧 Verification email sent. Please check your inbox.")
                return redirect("verify_otp")     

            # ---- Phone update (save only, no SMS) ----
            if phone != profile.phone:
                profile.phone = phone

            # ---- Handle profile image ----
            if cropped_image:
                format, imgstr = cropped_image.split(';base64,')
                ext = format.split('/')[-1]
                file = ContentFile(base64.b64decode(imgstr), name=f"profile.{ext}")
                if profile.profile_image:
                    profile.profile_image.delete(save=False)
                profile.profile_image = file
            elif raw_image:
                if profile.profile_image:
                    profile.profile_image.delete(save=False)
                profile.profile_image = raw_image

            profile.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect("edit_profile")

        elif "change_password" in request.POST:
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not user.check_password(current_password):
                messages.error(request, "❌ Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "❌ Passwords do not match.")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "✅ Password changed successfully!")
                return redirect("edit_profile")

    return render(request, "profile.html", {"user": user, "profile": profile})
