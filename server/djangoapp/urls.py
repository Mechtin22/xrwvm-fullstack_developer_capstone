from django.urls import path
from djangoapp import views


urlpatterns = [
    # Login
    path(
        "login",
        views.login_user,
        name="login"
    ),

    # Logout
    path(
        "logout",
        views.logout_request,
        name="logout"
    ),

    # Registration
    path(
        "register",
        views.registration,
        name="register"
    ),

    # Get all car makes and models
    path(
        "get_cars",
        views.get_cars,
        name="getcars"
    ),
]