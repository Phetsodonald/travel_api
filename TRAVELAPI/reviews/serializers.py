from rest_framework import serializers
from .models import Review,RatingSummary

class ReviewSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source='user.username',read_only=True)
    
    class Meta: 
        model=Review; 
        fields='__all__'; 
        read_only_fields=['id','user','helpful_count','created_at','updated_at','user_name']
    
    def validate_rating(self,value):
        if not 1<=value<=5: raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
    
    def validate(self,data):
        if sum(bool(data.get(x)) for x in ('destination','accommodation','activity'))!=1: raise serializers.ValidationError('Review must target exactly one resource.')
        return data
    
    def create(self,validated_data): 
        validated_data['user']=self.context['request'].user; 
        return super().create(validated_data)

class RatingSummarySerializer(serializers.ModelSerializer):
    class Meta: 
        model=RatingSummary; 
        fields='__all__'; 
        read_only_fields=['id','updated_at']
