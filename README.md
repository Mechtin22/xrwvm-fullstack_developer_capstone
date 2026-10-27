# Car Dealership Review Platform

A full-stack dealership directory and review application for the IBM Full Stack Developer capstone.

## Features
- Browse dealerships and filter them by state.
- Register and log in with Django authentication.
- Open dealer detail pages, read reviews, and post a review with car details.
- Retrieve dealership, review, and car inventory data through an Express + MongoDB API.
- Analyze review sentiment through a Flask/NLTK VADER service, with a fallback if the service is offline.
- Manage car makes and models through Django Admin.
- Validate the backend and frontend with GitHub Actions.

## Technology
Frontend: React 18 and React Router. Application API and authentication: Django. Dealer/review API: Express, Mongoose, and MongoDB. Sentiment analysis: Flask and NLTK VADER. Django templates and static files are stored in server/frontend/static.

## Local setup

### 1. Start MongoDB and Express
Install Docker Desktop. Open a terminal in server/database and run:

    docker compose up --build

The Express API listens on http://127.0.0.1:3030. Docker Compose provides the MongoDB container URL. For a local MongoDB instance instead, set MONGO_URI=mongodb://127.0.0.1:27017/dealershipsDB and run npm install and npm start from server/database.

### 2. Start Django
Open a terminal in server, create and activate a Python virtual environment, and run:

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py shell -c "from djangoapp.populate import initiate; initiate()"
    python manage.py createsuperuser
    python manage.py runserver

Django runs at http://127.0.0.1:8000. The landing page and dealer directory are / and /dealers. The admin site is /admin/.

Set environment variables for non-local environments: DJANGO_SECRET_KEY (private), DJANGO_DEBUG=false, ALLOWED_HOSTS (comma-separated hostnames), BACKEND_URL (default http://127.0.0.1:3030), and SENTIMENT_ANALYZER_URL (default http://127.0.0.1:5050). See server/.env.example for safe example values. Never commit a real .env file or production secrets.

### 3. Optional sentiment service
From server/djangoapp/microservices, install its requirements and run python app.py. It listens on port 5050 by default. Reviews remain usable if the service is offline.

### 4. Start React
In another terminal, open server/frontend and run npm install followed by npm start. The React development server runs at http://localhost:3000 and proxies /djangoapp API requests to Django on port 8000.

## Useful endpoints

Django: POST /djangoapp/login; GET /djangoapp/logout; POST /djangoapp/registration; GET /djangoapp/get_dealers; GET /djangoapp/get_dealers/Kansas; GET /djangoapp/dealer/8; GET /djangoapp/reviews/dealer/8; GET /djangoapp/get_cars; POST /djangoapp/add_review; POST /djangoapp/analyze_review.

Express: GET /fetchDealers; GET /fetchDealers/Kansas; GET /fetchDealer/8; GET /fetchReviews/dealer/8; POST /insert_review; GET /fetchCars.

## CI and deployment
GitHub Actions checks Django, validates Express JavaScript, and builds React on pushes and pull requests. Deploy the components to hosting services and configure the environment variables above before recording a deployment URL. This repository does not yet contain a verified production deployment URL.
