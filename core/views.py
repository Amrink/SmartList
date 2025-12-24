# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .forms import SignUpForm  # we’ll create this next

@login_required
def home(request):
    return render(request, "home.html")

class CustomLoginView(LoginView):
    template_name = "login.html"

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()       # creates user
            login(request, user)     # logs in immediately
            return redirect("home")  # redirect to dashboard
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})
