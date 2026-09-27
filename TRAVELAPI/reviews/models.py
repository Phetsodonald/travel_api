from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models
from TRAVELAPI .file_validators import validate_upload
from destinations.models import Destination
from bookings.models import Accommodation,Activity

class Review(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reviews'); 
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE,related_name='reviews',null=True,blank=True);
    accommodation=models.ForeignKey(Accommodation,on_delete=models.CASCADE,related_name='reviews',null=True,blank=True); 
    activity=models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='reviews',null=True,blank=True); 
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)]); 
    title=models.CharField(max_length=200); 
    content=models.TextField(); 
    visit_date=models.DateField(); 
    image=models.ImageField(upload_to='review_photos/',null=True,blank=True,validators=[validate_upload]); 
    helpful_count=models.PositiveIntegerField(default=0); 
    created_at=models.DateTimeField(auto_now_add=True); 
    updated_at=models.DateTimeField(auto_now=True)

    class Meta: 
        ordering=['-created_at']; 
        indexes=[models.Index(fields=['destination','rating']),models.Index(fields=['user'])]
    
    def __str__(self): 
        return f'{self.title} by {self.user.username}'
    
    def clean(self):
        if sum(bool(x) for x in (self.destination,self.accommodation,self.activity))!=1: raise ValidationError('Review must target exactly one resource.')

class RatingSummary(models.Model):
    destination=models.OneToOneField(Destination,on_delete=models.CASCADE,related_name='rating_summary'); 
    average=models.DecimalField(max_digits=3,decimal_places=2,default=0); 
    review_count=models.PositiveIntegerField(default=0); 
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self): 
        return f'Ratings for {self.destination.name}'
