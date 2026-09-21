from django.contrib.auth.models import AbstractUser
from django.db import models
from TRAVELAPI.file_validators import validate_upload

class User(AbstractUser):
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=20,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    bio=models.TextField(max_length=500,blank=True)
    profile_picture=models.ImageField(upload_to='profiles/',null=True,blank=True,validators=[validate_upload])
    travel_preferences=models.JSONField(default=dict,blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-created_at']; indexes=[models.Index(fields=['email'])]
    def __str__(self): return self.username
    @property
    def full_name(self): return f'{self.first_name} {self.last_name}'.strip() or self.username
    def recommendation_profile(self): return self.travel_preferences or {}
