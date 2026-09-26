from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Destination,DestinationPhoto
User=get_user_model()

class DestinationTests(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='u',password='pass12345'); self.client.force_authenticate(self.user); self.d=Destination.objects.create(name='Cape Town',country='South Africa',description='City',category='city',climate='temperate',best_time_to_visit='Summer',avg_daily_cost=500)
    
    def test_list(self): 
        self.assertEqual(self.client.get(
            '/api/v1/destinations/'
        ).status_code,200)
    
    def test_search(self): 
        self.assertEqual(self.client.get(
            '/api/v1/destinations/search/?q=Cape'
        ).status_code,200)
    
    def test_detail(self): 
        self.assertEqual(self.client.get(
            f'/api/v1/destinations/{self.d.id}/'
        ).status_code,200)
    
    def test_average_rating_without_reviews(self): 
        self.assertEqual(self.d.average_rating,0)
    
    def test_photo_model(self):
        self.assertEqual(
            str(DestinationPhoto(destination=self.d,image='x.jpg')),
            'Photo for Cape Town')
