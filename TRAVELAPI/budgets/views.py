from django.db.models import Sum,Count,F,Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Budget,Expense
from .serializers import BudgetSerializer,ExpenseSerializer
from .filters import ExpenseFilter
from .permissions import IsBudgetOwner

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class=BudgetSerializer; permission_classes=[IsAuthenticated,IsBudgetOwner]
    
    def get_queryset(self): 
        return Budget.objects.filter(itinerary__owner=self.request.user).select_related('itinerary')
    
    @action(detail=True,methods=['get'])
    def summary(self,request,pk=None):
        budget=self.get_object(); spent=budget.itinerary.expenses.aggregate(total=Sum('amount'))['total'] or 0
        return Response({'budget':budget.total_budget,'spent':spent,'remaining':budget.remaining(spent)})

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class=ExpenseSerializer; permission_classes=[IsAuthenticated]; filterset_class=ExpenseFilter; search_fields=['description','notes']; ordering_fields=['amount','date','created_at']
    
    def get_queryset(self): 
        return Expense.objects.filter(itinerary__owner=self.request.user).select_related('itinerary')
    
    def perform_create(self,serializer): 
        serializer.save()
    
    @action(detail=False,methods=['get'])
    def by_category(self,request):
        return Response(list(self.get_queryset().values('category').annotate(total=Sum('amount'),count=Count('id')).order_by('-total')))
