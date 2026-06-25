from django.urls import path
from . import views

app_name = "djangoapp"

urlpatterns = [
    path("get_cars", views.get_cars, name="get_cars"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("register", views.registration_request, name="register"),
]
