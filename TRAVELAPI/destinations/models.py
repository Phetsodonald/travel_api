from django.core.validators import MinValueValidator
from django.db import models
from TRAVELAPI.file_validators import validate_upload

class Destination(models.Model):
    class ClimateChoices(models.TextChoices):
        TROPICAL='tropical','Tropical'; DRY='dry','Dry'; TEMPERATE='temperate','Temperate'; CONTINENTAL='continental','Continental'; POLAR='polar','Polar'
    
    class CategoryChoices(models.TextChoices):
        BEACH='beach','Beach'; MOUNTAIN='mountain','Mountain'; CITY='city','City'; CULTURAL='cultural','Cultural'; ADVENTURE='adventure','Adventure'; RELAXATION='relaxation','Relaxation'
    name=models.CharField(max_length=200,unique=True); country=models.CharField(max_length=100); description=models.TextField()
    category=models.CharField(max_length=20,choices=CategoryChoices.choices); climate=models.CharField(max_length=20,choices=ClimateChoices.choices)
    best_time_to_visit=models.CharField(max_length=200); avg_daily_cost=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
    image=models.ImageField(upload_to='destinations/',null=True,blank=True,validators=[validate_upload]); latitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True); longitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['name']; indexes=[models.Index(fields=['country','category']),models.Index(fields=['climate']),models.Index(fields=['is_active'])]
    def __str__(self): return f'{self.name}, {self.country}'
    
    @property
    def average_rating(self): return self.reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0
    def recommendation_score(self, preferences):
        score=0
        if preferences.get('country')==self.country: score+=3
        if preferences.get('category')==self.category: score+=2
        if preferences.get('climate')==self.climate: score+=1
        return score

class DestinationPhoto(models.Model):
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE,related_name='photos'); image=models.ImageField(upload_to='destination_photos/',validators=[validate_upload]); caption=models.CharField(max_length=200,blank=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'Photo for {self.destination.name}'
