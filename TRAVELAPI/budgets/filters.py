from django_filters import rest_framework as filters
from .models import Expense

class ExpenseFilter(filters.FilterSet):
    min_amount=filters.NumberFilter(field_name='amount',lookup_expr='gte'); 
    max_amount=filters.NumberFilter(field_name='amount',lookup_expr='lte')
    
    class Meta: 
        model=Expense; 
        fields=['itinerary','category','date']
