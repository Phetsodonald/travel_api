from django.db import transaction
from rest_framework import serializers
from .models import Itinerary,DailyPlan,Collaboration
from destinations.serializers import DestinationListSerializer
from destinations.models import Destination

class CollaborationSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username',read_only=True); 
    email=serializers.EmailField(source='user.email',read_only=True)

    class Meta: 
        model=Collaboration; 
        fields=['id','user','username','email','role','invited_at']; 
        read_only_fields=['id','invited_at']

class DailyPlanSerializer(serializers.ModelSerializer):
    activities_count=serializers.SerializerMethodField()

    class Meta: 
        model=DailyPlan; 
        fields=['id','day_number','date','title','notes','activities','activities_count'];
        read_only_fields=['id']

    def get_activities_count(self,obj): 
        return obj.activities.count()
    
    def validate_day_number(self,value):
        if value<1: raise serializers.ValidationError('Day number must be positive.')
        return value

class ItineraryListSerializer(serializers.ModelSerializer):
    destination_name=serializers.CharField(source='destination.name',read_only=True); 
    owner_username=serializers.CharField(source='owner.username',read_only=True); 
    duration_days=serializers.ReadOnlyField(); 
    budget_remaining=serializers.ReadOnlyField()
    
    class Meta: 
        model=Itinerary; 
        fields=['id','title','destination','destination_name','owner','owner_username','start_date','end_date','duration_days','budget','budget_remaining','status','is_public']; 
        read_only_fields=['id','owner']

class ItineraryDetailSerializer(serializers.ModelSerializer):
    destination=DestinationListSerializer(read_only=True); 
    destination_id=serializers.PrimaryKeyRelatedField(queryset=Destination.objects.all(),source='destination',write_only=True)
    daily_plans=DailyPlanSerializer(many=True,read_only=True); collaborations=CollaborationSerializer(many=True,read_only=True); bookings_count=serializers.SerializerMethodField(); duration_days=serializers.ReadOnlyField(); budget_remaining=serializers.ReadOnlyField()
    
    class Meta: 
        model=Itinerary; 
        fields=['id','title','description','destination','destination_id','owner','start_date','end_date','budget','actual_spent','status','is_public','pdf','created_at','updated_at','daily_plans','collaborations','bookings_count','duration_days','budget_remaining']; read_only_fields=['id','owner','actual_spent','created_at','updated_at','duration_days','budget_remaining','bookings_count']
    
    def get_bookings_count(self,obj): 
        return obj.bookings.count()
    
    def validate(self,data):
        if data.get('end_date') and data.get('start_date') and data['end_date']<data['start_date']: raise serializers.ValidationError({'end_date':'End date must be after start date.'})
        if data.get('budget') is not None and data['budget']<0: raise serializers.ValidationError({'budget':'Budget cannot be negative.'})
        return data
    
    @transaction.atomic
    def create(self,validated_data):
        from budgets.models import Budget
        trip=Itinerary.objects.create(**validated_data); 
        Budget.objects.create(itinerary=trip); return trip

class ItineraryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Itinerary; 
        fields=['title','description','destination','start_date','end_date','budget','is_public','status']
    
    def validate_budget(self,value):
        if value<=0: raise serializers.ValidationError('Budget must be greater than zero.')
        return value
    
    def validate(self,data):
        if data.get('start_date') and data.get('end_date') and data['end_date']<data['start_date']: raise serializers.ValidationError({'end_date':'Invalid date range.'})
        return data
    
    def create(self,validated_data):
        from budgets.models import Budget
        trip=Itinerary.objects.create(**validated_data)
        Budget.objects.get_or_create(itinerary=trip)
        return trip
    
    def update(self,instance,validated_data): return super().update(instance,validated_data)
