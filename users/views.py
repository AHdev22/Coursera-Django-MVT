# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

        if user is not None:
            login(request, user)
            return redirect("home_show")  # change to your home page url name
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "login.html", {"email": email})
    else:
        return render(request, "login.html")




@require_POST
def logout_view(request):
    logout(request)
    return redirect('home_show')   # change to your landing page



@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        if "image" in request.FILES:
            profile.image = request.FILES["image"]
            profile.save()
            return redirect("profile")  # redirect to profile page

    return render(request, "users/edit_profile.html", {"profile": profile})