from django_filters import rest_framework as filters
from .models import Accommodation,Activity,Booking

class AccommodationFilter(filters.FilterSet):
    min_price=filters.NumberFilter(field_name='price_per_night',lookup_expr='gte'); max_price=filters.NumberFilter(field_name='price_per_night',lookup_expr='lte')
    class Meta: model=Accommodation; fields=['destination','accommodation_type','is_available']

class ActivityFilter(filters.FilterSet):
    min_price=filters.NumberFilter(field_name='price',lookup_expr='gte'); max_price=filters.NumberFilter(field_name='price',lookup_expr='lte')
    class Meta: model=Activity; fields=['destination','category','is_available']

class BookingFilter(filters.FilterSet):
    class Meta: model=Booking; fields=['status','itinerary','booking_date']
