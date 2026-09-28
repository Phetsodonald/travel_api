from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from destinations.models import Destination
from .models import Review
User=get_user_model()

class ReviewTests(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='u',password='pass12345'); self.client.force_authenticate(self.user); self.d=Destination.objects.create(name='Cape',country='ZA',description='City',category='city',climate='temperate',best_time_to_visit='Summer',avg_daily_cost=500)
    
    def test_create_review(self): 
        self.assertEqual(self.client.post('/api/reviews/',{'destination':self.d.id,'rating':5,'title':'Great','content':'Excellent','visit_date':str(date.today())}).status_code,201)
    
    def test_invalid_rating(self): 
        self.assertEqual(self.client.post('/api/reviews/',{'destination':self.d.id,'rating':9,'title':'Bad','content':'x','visit_date':str(date.today())}).status_code,400)
    
    def test_review_target_validation(self):
        r=Review(user=self.user,rating=5,title='x',content='x',visit_date=date.today()); self.assertRaises(Exception,r.full_clean)
    
    def test_helpful_action(self):
        r=Review.objects.create(
            user=self.user,
            destination=self.d,
            rating=5,
            title='Great',
            content='x',
            visit_date=date.today()); 
        
        self.assertEqual(self.client.post(f'/api/reviews/{r.id}/helpful/').status_code,200)
