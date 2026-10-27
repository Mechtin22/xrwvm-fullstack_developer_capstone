import json
import logging

from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate

logger = logging.getLogger(__name__)


# ============================================================
# LOGIN VIEW
# ============================================================

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
                "userName": user.username,
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

    except Exception:
        logger.exception("Login failed.")

        return JsonResponse(
            {"error": "Login failed. Please try again."},
            status=500
        )


# ============================================================
# LOGOUT VIEW
# ============================================================

def logout_request(request):
    if request.method not in ["GET", "POST"]:
        return JsonResponse(
            {"error": "Only GET and POST requests are allowed."},
            status=405
        )

    logout(request)

    return JsonResponse({
        "userName": "",
        "status": "Logged out successfully"
    })


# ============================================================
# REGISTRATION VIEW
# ============================================================

@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )

    try:
        data = json.loads(request.body)

        username = data.get("userName", "").strip()
        password = data.get("password", "")
        first_name = data.get("firstName", "").strip()
        last_name = data.get("lastName", "").strip()
        email = data.get("email", "").strip()

        if not all([
            username,
            password,
            first_name,
            last_name,
            email
        ]):
            return JsonResponse(
                {"error": "All fields are required."},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "userName": username,
                "error": "Already Registered"
            }, status=409)

        if User.objects.filter(email__iexact=email).exists():
            return JsonResponse({
                "userName": username,
                "error": "Email already registered"
            }, status=409)

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )

        login(request, user)

        return JsonResponse({
            "userName": user.username,
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


# ============================================================
# GET CARS VIEW
# ============================================================

def get_cars(request):
    try:
        # Populate the database if no car makes exist.
        count = CarMake.objects.count()
        print(count)

        if count == 0:
            initiate()

        # Retrieve car models and their related car makes.
        car_models = CarModel.objects.select_related("car_make")

        cars = []

        for car_model in car_models:
            cars.append({
                "CarModel": car_model.name,
                "CarMake": car_model.car_make.name
            })

        return JsonResponse({
            "CarModels": cars
        })

    except Exception:
        logger.exception("Error retrieving cars.")

        return JsonResponse(
            {"error": "Unable to retrieve cars."},
            status=500
        )