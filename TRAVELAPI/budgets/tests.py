from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from destinations.models import Destination
from itineraries.models import Itinerary
from .models import Budget,Expense
User=get_user_model()

class BudgetTests(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='u',password='pass12345'); self.client.force_authenticate(self.user); d=Destination.objects.create(name='Cape',country='ZA',description='City',category='city',climate='temperate',best_time_to_visit='Summer',avg_daily_cost=500); self.trip=Itinerary.objects.create(title='Trip',destination=d,owner=self.user,start_date=date.today(),end_date=date.today(),budget=1000); self.budget=Budget.objects.create(itinerary=self.trip,food_budget=300,transport_budget=200)
    
    def test_total_budget(self):
        self.assertEqual(self.budget.total_budget,500)
    
    def test_expense_create(self):
        self.assertEqual(self.client.post('/api/budgets/expenses/',{'itinerary':self.trip.id,'category':'food','description':'Lunch','amount':'100','date':str(date.today())}).status_code,201)
    
    def test_summary(self): 
        self.assertEqual(self.client.get(f'/api/budgets/budgets/{self.budget.id}/summary/').status_code,200)
    
    def test_by_category(self): 
        self.assertEqual(self.client.get('/api/budgets/expenses/by_category/').status_code,200)
