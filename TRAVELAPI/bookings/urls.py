from django.urls import path
from .views import BookingViewSet
from itineraries.views import bulk_update_bookings
from rest_framework.routers import DefaultRouter

router=DefaultRouter(); 
router.register('bookings',BookingViewSet,basename='booking-local')
app_name='bookings'

urlpatterns=router.urls+[path('bulk-update/',bulk_update_bookings,name='bulk-update')]
