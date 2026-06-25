from django.urls import path
from . import views

app_name = "djangoapp"

urlpatterns = [
    path("dealer/<int:dealer_id>/added_review/", views.added_review_page, name="added_review_page"),
    path("dealer/<int:dealer_id>/review/", views.dealer_review_form, name="dealer_review_form"),
    path("dealer/<int:dealer_id>/", views.dealer_details_page, name="dealer_details_page"),
    path("dealers/<str:state>/", views.dealers_by_state_page, name="dealers_by_state_page"),
    path("analyze_review", views.analyze_review, name="analyze_review"),
    path("get_cars", views.get_cars, name="get_cars"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("register", views.registration_request, name="register"),
]
