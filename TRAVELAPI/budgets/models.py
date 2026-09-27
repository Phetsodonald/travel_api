from django.core.validators import MinValueValidator
from django.db import models
from TRAVELAPI.file_validators import validate_upload
from itineraries.models import Itinerary

class Budget(models.Model):
    itinerary=models.OneToOneField(Itinerary,on_delete=models.CASCADE,related_name='budget_detail'); 
    accommodation_budget=models.DecimalField(max_digits=10,decimal_places=2,default=0,validators=[MinValueValidator(0)]); 
    activities_budget=models.DecimalField(max_digits=10,decimal_places=2,default=0,validators=[MinValueValidator(0)]); 
    food_budget=models.DecimalField(max_digits=10,decimal_places=2,default=0,validators=[MinValueValidator(0)]); 
    transport_budget=models.DecimalField(max_digits=10,decimal_places=2,default=0,validators=[MinValueValidator(0)]); 
    shopping_budget=models.DecimalField(max_digits=10,decimal_places=2,default=0,validators=[MinValueValidator(0)]); 
    miscellaneous_budget=models.DecimalField(max_digits=10,decimal_places=2,default=0,validators=[MinValueValidator(0)]); 
    created_at=models.DateTimeField(auto_now_add=True); 
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta: 
        ordering=['-created_at']
    
    def __str__(self): 
        return f'Budget for {self.itinerary.title}'
    
    @property
    def total_budget(self): 
        return sum(getattr(self,f) for f in ('accommodation_budget','activities_budget','food_budget','transport_budget','shopping_budget','miscellaneous_budget'))
    
    def remaining(self,spent): 
        return self.total_budget-spent

class Expense(models.Model):
    class CategoryChoices(models.TextChoices):
        ACCOMMODATION='accommodation','Accommodation'
        ACTIVITIES='activities','Activities'
        FOOD='food','Food'
        TRANSPORT='transport','Transport'
        SHOPPING='shopping','Shopping'
        MISCELLANEOUS='miscellaneous','Miscellaneous'
    
    itinerary=models.ForeignKey(Itinerary,on_delete=models.CASCADE,related_name='expenses'); category=models.CharField(max_length=20,choices=CategoryChoices.choices); description=models.CharField(max_length=200); amount=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)]); date=models.DateField(); receipt=models.ImageField(upload_to='receipts/',null=True,blank=True,validators=[validate_upload]); notes=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    
    class Meta: 
        ordering=['-date']; 
        indexes=[models.Index(fields=['itinerary','category']),models.Index(fields=['date'])]
    
    def __str__(self): 
        return f'{self.description} - {self.amount}'
    
    def clean(self):
        if self.amount<0: raise ValueError('Expense cannot be negative.')
    
    def is_large(self,threshold=1000): 
        return self.amount>=threshold
