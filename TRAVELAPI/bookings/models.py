from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from TRAVELAPI.file_validators import validate_upload
from destinations.models import Destination
from itineraries.models import Itinerary

class Accommodation(models.Model):
    class TypeChoices(models.TextChoices):
        HOTEL='hotel','Hotel'
        HOSTEL='hostel','Hostel'
        RENTAL='rental','Vacation Rental'
        RESORT='resort','Resort'
        BNB='bnb','B&B'
    
    name=models.CharField(max_length=200); 
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE,related_name='accommodations'); 
    accommodation_type=models.CharField(max_length=10,choices=TypeChoices.choices); 
    description=models.TextField(); 
    price_per_night=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)]); 
    max_guests=models.PositiveIntegerField(); 
    amenities=models.JSONField(default=list); 
    address=models.CharField(max_length=300); 
    contact_email=models.EmailField(); 
    contact_phone=models.CharField(max_length=20); 
    image=models.ImageField(upload_to='accommodations/',null=True,blank=True,validators=[validate_upload]); 
    is_available=models.BooleanField(default=True); 
    created_at=models.DateTimeField(auto_now_add=True); 
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta: 
        ordering=['name']; indexes=[models.Index(fields=['destination','accommodation_type']),models.Index(fields=['is_available'])]
    
    def __str__(self): 
        return f'{self.name} ({self.get_accommodation_type_display()})'
    
    def total_cost(self,nights): 
        return self.price_per_night*nights

class Activity(models.Model):
    class CategoryChoices(models.TextChoices):
        TOUR='tour','Tour'
        ATTRACTION='attraction','Attraction'
        DINING='dining','Dining'
        SHOPPING='shopping','Shopping'
        ENTERTAINMENT='entertainment','Entertainment'
        OUTDOOR='outdoor','Outdoor'
    
    name=models.CharField(max_length=200); 
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE,related_name='activities'); 
    category=models.CharField(max_length=20,choices=CategoryChoices.choices); 
    description=models.TextField(); 
    duration_hours=models.DecimalField(max_digits=4,decimal_places=1); 
    price=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)]); 
    max_participants=models.PositiveIntegerField(null=True,blank=True); 
    requirements=models.TextField(blank=True); 
    image=models.ImageField(upload_to='activities/',null=True,blank=True,validators=[validate_upload]); 
    is_available=models.BooleanField(default=True); 
    created_at=models.DateTimeField(auto_now_add=True); 
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta: 
        ordering=['name']; 
        indexes=[models.Index(fields=['destination','category']),
                 models.Index(fields=['is_available'])]
    
    def __str__(self): 
        return f'{self.name} - {self.destination.name}'
    
    def is_capacity_available(self,requested): 
        return self.max_participants is None or requested<=self.max_participants

class Booking(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING='pending','Pending'
        CONFIRMED='confirmed','Confirmed'
        CANCELLED='cancelled','Cancelled'
        COMPLETED='completed','Completed'
    
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='bookings'); itinerary=models.ForeignKey(Itinerary,on_delete=models.CASCADE,related_name='bookings'); accommodation=models.ForeignKey(Accommodation,on_delete=models.SET_NULL,null=True,blank=True,related_name='bookings'); activity=models.ForeignKey(Activity,on_delete=models.SET_NULL,null=True,blank=True,related_name='bookings'); booking_date=models.DateField(); check_in=models.DateField(null=True,blank=True); check_out=models.DateField(null=True,blank=True); guests_count=models.PositiveIntegerField(default=1); price=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)]); status=models.CharField(max_length=20,choices=StatusChoices.choices,default=StatusChoices.PENDING); confirmation_code=models.CharField(max_length=50,blank=True); notes=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    
    class Meta: ordering=['-created_at']; 
    indexes=[models.Index(fields=['user','status']), models.Index(fields=['itinerary','status'])]
    
    def __str__(self): 
        return f'Booking #{self.id}'
    
    def clean(self):
        if bool(self.accommodation)==bool(self.activity): raise ValidationError('Booking must have exactly one resource: accommodation or activity.')
        if self.check_in and self.check_out and self.check_out<=self.check_in: raise ValidationError('Check-out must be after check-in.')
    
    def confirm(self): 
        self.status=self.StatusChoices.CONFIRMED; 
        self.save(update_fields=['status','updated_at'])

    def cancel(self): 
        self.status=self.StatusChoices.CANCELLED; 
        self.save(update_fields=['status','updated_at'])


class Recommendation(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='recommendations'); destination=models.ForeignKey(Destination,on_delete=models.CASCADE,related_name='recommendations'); score=models.DecimalField(max_digits=5,decimal_places=2); reason=models.CharField(max_length=300); created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        ordering=['-score','-created_at']; 
        unique_together=['user','destination']
    
    def __str__(self): 
        return f'{self.user.username} -> {self.destination.name}'
