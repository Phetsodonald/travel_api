from django_filters import rest_framework as filters
from .models import Destination

class DestinationFilter(filters.FilterSet):
    min_cost=filters.NumberFilter(field_name='avg_daily_cost',lookup_expr='gte'); 
    max_cost=filters.NumberFilter(field_name='avg_daily_cost',lookup_expr='lte')
    
    class Meta: 
        model=Destination; 
        fields=['country','category','climate','is_active']
