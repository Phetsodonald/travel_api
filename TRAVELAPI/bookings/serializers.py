from rest_framework import serializers
from .models import Accommodation,Activity,Booking,Recommendation

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta: model=Accommodation; fields='__all__'; read_only_fields=['id','created_at','updated_at']
    def validate_max_guests(self,value):
        if value<1: raise serializers.ValidationError('At least one guest is required.')
        return value

class ActivitySerializer(serializers.ModelSerializer):
    booking_count=serializers.SerializerMethodField()
    class Meta: model=Activity; fields='__all__'; read_only_fields=['id','created_at','updated_at','booking_count']
    def get_booking_count(self,obj): return obj.bookings.count()

class BookingSerializer(serializers.ModelSerializer):
    resource_name=serializers.SerializerMethodField()
    class Meta: model=Booking; fields='__all__'; read_only_fields=['id','user','created_at','updated_at','confirmation_code','resource_name']
    def get_resource_name(self,obj): return obj.accommodation.name if obj.accommodation else (obj.activity.name if obj.activity else None)
    def validate(self,data):
        if bool(data.get('accommodation'))==bool(data.get('activity')): raise serializers.ValidationError('Select exactly one accommodation or activity.')
        if data.get('check_in') and data.get('check_out') and data['check_out']<=data['check_in']: raise serializers.ValidationError({'check_out':'Check-out must be after check-in.'})
        return data
    def create(self,validated_data):
        validated_data['user']=self.context['request'].user; return super().create(validated_data)

class BookingDetailSerializer(BookingSerializer):
    class Meta(BookingSerializer.Meta):
        fields=BookingSerializer.Meta.fields

class RecommendationSerializer(serializers.ModelSerializer):
    destination_name=serializers.CharField(source='destination.name',read_only=True)
    class Meta: model=Recommendation; fields='__all__'; read_only_fields=['id','created_at']
