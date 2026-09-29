# Travel Itinerary Planning & Booking API

A Django REST Framework backend for destinations, collaborative trip planning, bookings, budgets, reviews, recommendations, uploads and analytics. The API uses JWT authentication, PostgreSQL-compatible settings, filtering, search, pagination and OpenAPI documentation.

## Stack
Django, Django REST Framework, Simple JWT, django-filter, drf-spectacular, python-decouple, Pillow, SQLite, pytest, pytest-django and coverage.

## Setup
```bash
python -m venv venv
# Windows
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
SQLite is the default development fallback.

## Environment
`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`,

## Documentation
- Swagger: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- Schema: `http://127.0.0.1:8000/api/schema/`
- Admin: `http://127.0.0.1:8000/admin/`

## Main API endpoints
`POST /api/accounts/register/` — register and receive JWTs.
`POST /api/accounts/login/` — login and receive JWTs.
`POST /api/auth/token/refresh/` — refresh access token.
`GET/PATCH /api/accounts/profile/` — profile.
`GET /api/destinations/` — browse destinations.
`GET /api/destinations/search/?q=cape` — custom search.
`GET/POST /api/itineraries/` — list/create trips.
`GET/PATCH/DELETE /api/itineraries/<id>/` — trip management.
`GET /api/itineraries/<id>/report/` — trip report.
`POST /api/itineraries/<id>/share/` — share a trip.
`GET/POST /api/itineraries/<id>/days/` — day plans.
`GET/POST/PATCH/DELETE /api/bookings/` — booking CRUD via router.
`POST /api/bookings/<id>/confirm/` and `/cancel/` — booking actions.
`GET/POST/PATCH/DELETE /api/budgets/` — budgets/expenses.
`GET/POST/PATCH/DELETE /api/reviews/` — reviews.
`GET /api/analytics/` — personal analytics.

## Example
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"tester","password":"pass12345"}'

curl http://127.0.0.1:8000/api/destinations/ \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

## Structure
Six domain apps are used: `accounts`, `destinations`, `itineraries`, `bookings`, `reviews`, and `budgets`. Each app separates models, serializers, views, permissions, filters, URLs and tests. The project package contains settings, routing, pagination and exception handling.

See `PLANNING.md` for the ERD, permission matrix, URL design and testing strategy.

## Tests
```bash
coverage run manage.py test
coverage report --omit="*/tests.py" -m
```
The suite contains more than 25 API/model/permission/authentication checks.
