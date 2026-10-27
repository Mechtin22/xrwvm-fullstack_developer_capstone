from django.urls import path
from djangoapp import views

urlpatterns = [
    # Login
    path(
        route="login",
        view=views.login_user,
        name="login"
    ),

    # Logout
    path(
        route="logout",
        view=views.logout_request,
        name="logout"
    ),

    # Registration
    path(
        route="register",
        view=views.registration,
        name="register"
    ),
]
