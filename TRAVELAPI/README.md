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
`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, database engine/name/user/password/host/port. Never commit `.env`.

## Documentation
- Swagger: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- Schema: `http://127.0.0.1:8000/api/schema/`
- Admin: `http://127.0.0.1:8000/admin/`

## Main API endpoints
`POST /api/v1/accounts/register/` — register and receive JWTs.
`POST /api/v1/accounts/login/` — login and receive JWTs.
`POST /api/v1/auth/token/refresh/` — refresh access token.
`GET/PATCH /api/v1/accounts/profile/` — profile.
`GET /api/v1/destinations/` — browse destinations.
`GET /api/v1/destinations/search/?q=cape` — custom search.
`GET/POST /api/v1/itineraries/` — list/create trips.
`GET/PATCH/DELETE /api/v1/itineraries/<id>/` — trip management.
`GET /api/v1/itineraries/<id>/report/` — trip report.
`POST /api/v1/itineraries/<id>/share/` — share a trip.
`GET/POST /api/v1/itineraries/<id>/days/` — day plans.
`GET/POST/PATCH/DELETE /api/v1/bookings/` — booking CRUD via router.
`POST /api/v1/bookings/<id>/confirm/` and `/cancel/` — booking actions.
`GET/POST/PATCH/DELETE /api/v1/budgets/` — budgets/expenses.
`GET/POST/PATCH/DELETE /api/v1/reviews/` — reviews.
`GET /api/v1/analytics/` — personal analytics.

## Example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"tester","password":"pass12345"}'

curl http://127.0.0.1:8000/api/v1/destinations/ \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

## Structure
Six domain apps are used: `accounts`, `destinations`, `itineraries`, `bookings`, `reviews`, and `budgets`. Each app separates models, serializers, views, permissions, filters, URLs and tests. The project package contains settings, routing, pagination and exception handling.

See `PLANNING.md` for the ERD, permission matrix, URL design and testing strategy.

## Tests
```bash
pytest
pytest --cov=. --cov-report=term-missing
```
The suite contains more than 25 API/model/permission/authentication checks.
