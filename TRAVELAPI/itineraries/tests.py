from datetime import date,timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from .models import Itinerary,Collaboration,DailyPlan
from destinations.models import Destination

User=get_user_model()

class ItineraryTests(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='owner',password='pass12345'); self.client.force_authenticate(self.user); self.d=Destination.objects.create(name='Cape Town',country='South Africa',description='City',category='city',climate='temperate',best_time_to_visit='Summer',avg_daily_cost=500); self.trip=Itinerary.objects.create(title='Cape',destination=self.d,owner=self.user,start_date=date.today(),end_date=date.today()+timedelta(days=2),budget=5000)
    
    def test_list(self): 
        self.assertEqual(self.client.get('/api/v1/itineraries/').status_code,200)
    
    def test_create(self):
        self.assertEqual(self.client.post('/api/v1/itineraries/',{'title':'New','destination':self.d.id,'start_date':str(date.today()),'end_date':str(date.today()),'budget':1000}).status_code,201)
    
    def test_detail(self): 
        self.assertEqual(self.client.get(f'/api/v1/itineraries/{self.trip.id}/').status_code,200)
    
    def test_patch(self): 
        self.assertEqual(self.client.patch(f'/api/v1/itineraries/{self.trip.id}/',{'budget':6000}).status_code,200)
    
    def test_report(self): 
        self.assertEqual(self.client.get(f'/api/v1/itineraries/{self.trip.id}/report/').status_code,200)
    
    def test_duration(self): 
        self.assertEqual(self.trip.duration_days,3)
    
    def test_collaborator_can_view(self):
        other=User.objects.create_user(username='viewer',password='pass12345'); Collaboration.objects.create(itinerary=self.trip,user=other,role='viewer'); self.client.force_authenticate(other); self.assertEqual(self.client.get(f'/api/v1/itineraries/{self.trip.id}/').status_code,200)
    
    def test_daily_plan(self):
        p=DailyPlan.objects.create(itinerary=self.trip,day_number=1,date=self.trip.start_date,title='Arrival'); self.assertTrue(p.is_within_trip())
