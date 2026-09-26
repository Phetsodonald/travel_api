from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from destinations.models import Destination
from itineraries.models import Itinerary
from .models import Activity,Booking,Accommodation

User=get_user_model()

class BookingTests(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='u',password='pass12345'); self.client.force_authenticate(self.user); d=Destination.objects.create(name='Cape',country='ZA',description='City',category='city',climate='temperate',best_time_to_visit='Summer',avg_daily_cost=500); self.trip=Itinerary.objects.create(title='Trip',destination=d,owner=self.user,start_date=date.today(),end_date=date.today(),budget=1000); self.activity=Activity.objects.create(name='Hike',destination=d,category='outdoor',description='Hike',duration_hours=2,price=50)
    
    def test_activity_create(self): 
        self.assertEqual(self.client.post(
            '/api/v1/activities/',
            {
                'name':'Museum',
                'destination':self.trip.destination.id,
                'category':'attraction',
                'description':'Visit',
                'duration_hours':'2',
                'price':'50'
            }).status_code,201)
    
    def test_accommodation_create(self): 
        self.assertEqual(self.client.post(
            '/api/v1/accommodations/',
            {
                'name':'Hotel',
                'destination':self.trip.destination.id,
                'accommodation_type':'hotel',
                'description':'Stay',
                'price_per_night':'800',
                'max_guests':2,
                'amenities':[],
                'address':'Cape',
                'contact_email':'hotel@example.com',
                'contact_phone':'123'
            }).status_code,201)
        
    def test_booking_create(self): 
        self.assertEqual(self.client.post(
            '/api/v1/bookings/',
            {
                'itinerary':self.trip.id,
                'activity':self.activity.id,
                'booking_date':str(date.today()),
                'price':'50'
            }).status_code,201)
        
    def test_confirm_and_cancel(self):
        b=Booking.objects.create(
            user=self.user,
            itinerary=self.trip,
            activity=self.activity,
            booking_date=date.today(),
            price=50);
         
        self.assertEqual(self.client.post(
            f'/api/v1/bookings/{b.id}/confirm/'
            ).status_code,200); 
        
        self.assertEqual(self.client.post(
            f'/api/v1/bookings/{b.id}/cancel/'
            ).status_code,200)
    
    def test_booking_owner_isolated(self):
        b=Booking.objects.create(
            user=self.user,
            itinerary=self.trip,
            activity=self.activity,
            booking_date=date.today(),
            price=50); 
        
        other=User.objects.create_user(
            username='other',
            password='pass12345');
         
        self.client.force_authenticate(other); 
        self.assertEqual(self.client.get(
            f'/api/v1/bookings/{b.id}/'
            ).status_code,404)
