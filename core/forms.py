from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# ======================
# AUTH / SIGN UP FORM
# ======================

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# ======================
# RESTAURANT FILTER FORM
# ======================

CUISINE_CHOICES = [
    ("mexican", "Mexican"),
    ("italian", "Italian"),
    ("japanese", "Japanese"),
    ("indian", "Indian"),
    ("chinese", "Chinese"),
    ("thai", "Thai"),
    ("korean", "Korean"),
    ("american", "American"),
    ("mediterranean", "Mediterranean"),
    ("middle_eastern", "Middle Eastern"),
    ("vietnamese", "Vietnamese"),
    ("greek", "Greek"),
    ("french", "French"),
]

PRICE_CHOICES = [
    ("", "Any"),
    ("1", "$"),
    ("2", "$$"),
    ("3", "$$$"),
    ("4", "$$$$"),
]


class RestaurantFilterForm(forms.Form):
    price_range = forms.ChoiceField(
        choices=PRICE_CHOICES,
        required=False,
        label="Price Range"
    )

    radius = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=50,
        label="Search Radius (miles)",
        help_text="1–50 miles"
    )

    cuisine = forms.MultipleChoiceField(
        choices=CUISINE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Cuisine Type"
    )
