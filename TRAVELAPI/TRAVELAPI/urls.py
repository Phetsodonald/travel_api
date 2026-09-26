
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/destinations/', include('destinations.urls')),
    path('api/itineraries/', include('itineraries.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/budgets/', include('budgets.urls'))
]
