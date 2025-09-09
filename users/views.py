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




User = get_user_model()

def verify_otp(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login_view')

    user = User.objects.get(id=user_id)
    profile, created = Profile.objects.get_or_create(user=user)

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
            # SUCCESS: log in the user with backend specified
            backend = 'django.contrib.auth.backends.ModelBackend'  # default backend
            login(request, user, backend=backend)

            profile.verification_code = None
            profile.code_attempts = 0
            profile.save()
            messages.success(request, "Email verified successfully!")
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

        # ---- Profile update ----
        if "update_profile" in request.POST:
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            image = request.FILES.get("image")

            # Update email
            if email and email != user.email:
                
                user.email = email
                user.save()

            # Update phone
            if phone:
                # Optionally: send verification SMS here
                profile.phone = phone

            # Update image
            if image:
                if profile.profile_image:
                    profile.profile_image.delete(save=False)  # delete old file from disk
                profile.profile_image = image
                
            profile.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect('edit_profile')

        # ---- Password change ----
        elif "change_password" in request.POST:
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not user.check_password(current_password):
                messages.error(request, "❌ Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "❌ New passwords do not match.")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # keep logged in
                messages.success(request, "✅ Password changed successfully!")
                return redirect('edit_profile')

    return render(request, "profile.html", {
        "user": user,
        "profile": profile
    })
