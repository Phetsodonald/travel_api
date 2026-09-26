from rest_framework import serializers
from .models import Destination,DestinationPhoto

class DestinationListSerializer(serializers.ModelSerializer):
    average_rating=serializers.ReadOnlyField(); review_count=serializers.SerializerMethodField()
    class Meta: model=Destination; fields=['id','name','country','category','climate','avg_daily_cost','image','average_rating','review_count']; read_only_fields=['id']
    def get_review_count(self,obj): return obj.reviews.count()

class DestinationPhotoSerializer(serializers.ModelSerializer):
    class Meta: model=DestinationPhoto; fields='__all__'; read_only_fields=['id','created_at']

class DestinationDetailSerializer(serializers.ModelSerializer):
    average_rating=serializers.ReadOnlyField(); 
    total_itineraries=serializers.SerializerMethodField(); 
    photos=DestinationPhotoSerializer(many=True,read_only=True)
    
    class Meta: 
        model=Destination; 
        fields='__all__'; read_only_fields=['id','created_at','updated_at']
    
    def get_total_itineraries(self,obj): 
        return obj.itineraries.count()
    
    def to_representation(self,instance):
        data=super().to_representation(instance); 
        data['recommendation_tags']=[instance.category,instance.climate]; return data
