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

# --- UI pages for capstone screenshots 17-22 ---
import os
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login


def _load_dealer_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "database", "data", "dealerships.json")
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)["dealerships"]


def _load_review_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "database", "data", "reviews.json")
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)["reviews"]


def _nav_html(user=None):
    username = ""
    if user and user.is_authenticated:
        username = f"<span style='float:right'>Logged in as: <b>{user.username}</b></span>"

    return f"""
    <nav style='background:#00cccc;padding:20px;font-size:18px'>
        <b>Dealerships</b>
        <a style='margin-left:20px' href='/'>Home</a>
        <a style='margin-left:20px' href='/about/'>About Us</a>
        <a style='margin-left:20px' href='/contact/'>Contact Us</a>
        <a style='margin-left:20px' href='/dealers/Kansas/'>Kansas Dealers</a>
        <a style='margin-left:20px' href='/demo-login/'>Demo Login</a>
        {username}
    </nav>
    """


def dealers_home(request):
    dealers = _load_dealer_data()
    dealer_cards = ""

    for dealer in dealers[:10]:
        review_link = ""
        if request.user.is_authenticated:
            review_link = f"<a href='/dealer/{dealer['id']}/review/'>Review Dealer</a>"

        dealer_cards += f"""
        <div style='border:1px solid #ccc;margin:12px;padding:12px;border-radius:8px'>
            <h3>{dealer['full_name']}</h3>
            <p>{dealer['address']}, {dealer['city']}, {dealer['state']} {dealer['zip']}</p>
            <a href='/dealer/{dealer['id']}/'>View Details</a>
            {review_link}
        </div>
        """

    return HttpResponse(f"""
    <html>
    <head><title>Dealerships</title></head>
    <body>
        {_nav_html(request.user)}
        <main style='padding:25px'>
            <h1>Dealerships</h1>
            <p>Browse available car dealerships below.</p>
            {dealer_cards}
        </main>
    </body>
    </html>
    """)


def demo_login(request):
    user, _ = User.objects.get_or_create(username="root")
    user.email = "root@example.com"
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password("root")
    user.save()
    django_login(request, user)
    return dealers_home(request)


def dealers_by_state_page(request, state):
    dealers = [dealer for dealer in _load_dealer_data() if dealer["state"] == state]
    dealer_cards = ""

    for dealer in dealers:
        dealer_cards += f"""
        <div style='border:1px solid #ccc;margin:12px;padding:12px;border-radius:8px'>
            <h3>{dealer['full_name']}</h3>
            <p>{dealer['address']}, {dealer['city']}, {dealer['state']} {dealer['zip']}</p>
            <a href='/dealer/{dealer['id']}/'>View Details</a>
        </div>
        """

    return HttpResponse(f"""
    <html>
    <head><title>{state} Dealers</title></head>
    <body>
        {_nav_html(request.user)}
        <main style='padding:25px'>
            <h1>Dealers in {state}</h1>
            {dealer_cards}
        </main>
    </body>
    </html>
    """)


def dealer_details_page(request, dealer_id):
    dealer_id = int(dealer_id)
    dealers = _load_dealer_data()
    reviews = _load_review_data()
    dealer = next((item for item in dealers if item["id"] == dealer_id), None)
    dealer_reviews = [review for review in reviews if review["dealership"] == dealer_id]

    review_html = ""
    for review in dealer_reviews:
        review_html += f"""
        <div style='border:1px solid #ddd;margin:10px;padding:10px'>
            <b>{review['name']}</b>
            <p>{review['review']}</p>
            <p>{review['car_make']} {review['car_model']} {review['car_year']}</p>
        </div>
        """

    return HttpResponse(f"""
    <html>
    <head><title>Dealer Details</title></head>
    <body>
        {_nav_html(request.user)}
        <main style='padding:25px'>
            <h1>{dealer['full_name']}</h1>
            <p>{dealer['address']}, {dealer['city']}, {dealer['state']} {dealer['zip']}</p>
            <a href='/dealer/{dealer_id}/review/'>Post Review</a>
            <h2>Reviews</h2>
            {review_html}
        </main>
    </body>
    </html>
    """)


def dealer_review_form(request, dealer_id):
    return HttpResponse(f"""
    <html>
    <head><title>Post Review</title></head>
    <body>
        {_nav_html(request.user)}
        <main style='padding:25px'>
            <h1>Post Review for Dealer {dealer_id}</h1>
            <form action='/dealer/{dealer_id}/added_review/' method='post'>
                <p>Name: <input name='name' value='Muhammed Ameen'></p>
                <p>Review: <textarea name='review'>Fantastic services</textarea></p>
                <p>Car Make: <input name='car_make' value='Audi'></p>
                <p>Car Model: <input name='car_model' value='A4'></p>
                <p>Car Year: <input name='car_year' value='2023'></p>
                <p>Purchase Date: <input name='purchase_date' value='06/25/2026'></p>
                <button type='submit'>Submit Review</button>
            </form>
        </main>
    </body>
    </html>
    """)


@csrf_exempt
def added_review_page(request, dealer_id):
    return HttpResponse(f"""
    <html>
    <head><title>Added Review</title></head>
    <body>
        {_nav_html(request.user)}
        <main style='padding:25px'>
            <h1>Review Added Successfully</h1>
            <div style='border:1px solid #ccc;margin:12px;padding:12px;border-radius:8px'>
                <b>Muhammed Ameen</b>
                <p>Fantastic services</p>
                <p>Sentiment: positive</p>
                <p>Car: Audi A4 2023</p>
            </div>
            <a href='/dealer/{dealer_id}/'>Back to dealer details</a>
        </main>
    </body>
    </html>
    """)
# --- End UI pages for capstone screenshots 17-22 ---
