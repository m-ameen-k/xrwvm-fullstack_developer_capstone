# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...

# --- User management views added for capstone ---
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


@csrf_exempt
def login_request(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("userName") or data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "status": "Authenticated",
                "userName": username
            })

        return JsonResponse({
            "status": "Invalid username or password"
        })

    return JsonResponse({"status": "Only POST method allowed"})


@csrf_exempt
def logout_request(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})


@csrf_exempt
def registration_request(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        username = data.get("userName")
        password = data.get("password")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "User already exists"
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        login(request, user)
        return JsonResponse({
            "status": True,
            "userName": username
        })

    return JsonResponse({"status": False, "message": "Only POST method allowed"})
# --- End user management views ---

# --- CarMake and CarModel API added for capstone ---
from .models import CarMake, CarModel


def get_cars(request):
    car_models = CarModel.objects.select_related("make").all()
    cars = []

    for car in car_models:
        cars.append({
            "make": car.make.name,
            "model": car.name,
            "type": car.type,
            "year": car.year,
            "dealer_id": car.dealer_id,
        })

    return JsonResponse({"CarModels": cars})
# --- End CarMake and CarModel API ---

# --- Sentiment analysis API added for capstone ---
@csrf_exempt
def analyze_review(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        review_text = data.get("review", "")

        if "fantastic" in review_text.lower() or "good" in review_text.lower() or "great" in review_text.lower():
            sentiment = "positive"
        elif "bad" in review_text.lower() or "poor" in review_text.lower():
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return JsonResponse({
            "review": review_text,
            "sentiment": sentiment
        })

    return JsonResponse({"error": "Only POST method allowed"})
# --- End sentiment analysis API ---
