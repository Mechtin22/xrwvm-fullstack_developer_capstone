import json
import logging

from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


# LOGIN VIEW
@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )

    try:
        data = json.loads(request.body)

        username = data.get("userName")
        password = data.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required."},
                status=400
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })

        return JsonResponse({
            "userName": username,
            "status": "Invalid credentials"
        }, status=401)

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON request body."},
            status=400
        )


# LOGOUT VIEW
def logout_request(request):
    logout(request)

    data = {"userName": ""}

    return JsonResponse(data)


# REGISTRATION VIEW
@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )

    try:
        # Load JSON data from the request body
        data = json.loads(request.body)

        username = data.get("userName", "").strip()
        password = data.get("password", "")
        first_name = data.get("firstName", "").strip()
        last_name = data.get("lastName", "").strip()
        email = data.get("email", "").strip()

        # Validate required fields
        if not all([username, password, first_name, last_name, email]):
            return JsonResponse(
                {"error": "All fields are required."},
                status=400
            )

        # Check whether the username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "userName": username,
                "error": "Already Registered"
            }, status=409)

        # Check whether the email is already registered
        if User.objects.filter(email__iexact=email).exists():
            return JsonResponse({
                "userName": username,
                "error": "Email already registered"
            }, status=409)

        # Create a new Django user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )

        # Log in the newly registered user
        login(request, user)

        # Return the username and authentication status
        return JsonResponse({
            "userName": username,
            "status": "Authenticated"
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON request body."},
            status=400
        )

    except Exception:
        logger.exception("Registration failed.")

        return JsonResponse(
            {"error": "Registration failed. Please try again."},
            status=500
        )


# IMPORTANT:
# Keep your existing dealership, review, and other views below.
# Do not delete functions such as:
# get_dealerships()
# get_dealer_details()
# get_dealer_reviews()
# add_review()
