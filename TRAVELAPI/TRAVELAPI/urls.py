from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView,SpectacularRedocView
from rest_framework_simplejwt.views import TokenRefreshView
from itineraries.views import ItineraryViewSet
from destinations.views import DestinationViewSet
from bookings.views import AccommodationViewSet, ActivityViewSet, BookingViewSet
from itineraries.views import TripAnalyticsViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('itineraries',ItineraryViewSet,basename='itinerary')
router.register('destinations',DestinationViewSet,basename='destination')
router.register('accommodations',AccommodationViewSet,basename='accommodation')
router.register('activities',ActivityViewSet,basename='activity')
router.register('bookings',BookingViewSet,basename='booking')
router.register('analytics',TripAnalyticsViewSet,basename='analytics')

urlpatterns=[
 path('admin/',admin.site.urls),
path('api/destinations/',include('destinations.urls')),
 path('api/',include(router.urls)),
 path('api/accounts/',include('accounts.urls')),
 path('api/itineraries/',include('itineraries.urls')),
 path('api/bookings/',include('bookings.urls')),
 path('api/reviews/',include('reviews.urls')),
 path('api/budgets/',include('budgets.urls')),
 path('api/schema/',SpectacularAPIView.as_view(),name='schema'),
 path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
 path('api/redoc/',SpectacularRedocView.as_view(url_name='schema'),name='redoc'),
 path('api/auth/token/refresh/',TokenRefreshView.as_view(),name='token-refresh'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
