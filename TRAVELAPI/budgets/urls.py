from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet,ExpenseViewSet

router=DefaultRouter(); 
router.register('budgets',BudgetViewSet,basename='budget'); router.register('expenses',ExpenseViewSet,basename='expense')
app_name='budgets'; 
urlpatterns=[path('',include(router.urls))]
