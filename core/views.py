# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import SignUpForm, RestaurantFilterForm

# Mock restaurant data
RESTAURANTS = [
    {"name": "Pasta Palace", "cuisine": "italian", "price": "$$", "rating": 4.7, "distance": 1.2},
    {"name": "Sushi World", "cuisine": "japanese", "price": "$$$", "rating": 4.8, "distance": 2.0},
    {"name": "Curry House", "cuisine": "indian", "price": "$", "rating": 4.5, "distance": 3.5},
    {"name": "Taco Town", "cuisine": "mexican", "price": "$", "rating": 4.3, "distance": 1.5},
    {"name": "Dragon Express", "cuisine": "chinese", "price": "$$", "rating": 4.6, "distance": 4.0},
]

@login_required
def home(request):
    results = None
    top_restaurants = None

    if request.method == "POST":
        form = RestaurantFilterForm(request.POST)
        if form.is_valid():
            results = form.cleaned_data

            # Filter restaurants based on selected filters
            filtered = RESTAURANTS

            # Cuisine filter (multiple)
            cuisines = results.get("cuisine")
            if cuisines:
                filtered = [r for r in filtered if r["cuisine"] in cuisines]

            # Price range filter
            price = results.get("price_range")
            if price:
                filtered = [r for r in filtered if r["price"] == price]

            # Radius filter
            radius = results.get("radius")
            if radius:
                filtered = [r for r in filtered if r["distance"] <= float(radius)]

            # Sort by rating descending and take top 3
            top_restaurants = sorted(filtered, key=lambda x: x["rating"], reverse=True)[:3]

    else:
        form = RestaurantFilterForm()

    return render(request, "home.html", {"form": form, "results": results, "restaurants": top_restaurants})



class CustomLoginView(LoginView):
    template_name = "login.html"

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})
