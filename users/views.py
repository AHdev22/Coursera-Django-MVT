# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

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
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'home_show')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")




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
