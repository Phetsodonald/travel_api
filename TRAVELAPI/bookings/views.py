from django.db.models import Count,Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Accommodation,Activity,Booking,Recommendation
from .serializers import AccommodationSerializer,ActivitySerializer,BookingSerializer,BookingDetailSerializer,RecommendationSerializer
from .filters import AccommodationFilter,ActivityFilter,BookingFilter
from .permissions import IsBookingOwner

class AccommodationViewSet(viewsets.ModelViewSet):
    queryset=Accommodation.objects.select_related('destination').all(); serializer_class=AccommodationSerializer; permission_classes=[IsAuthenticatedOrReadOnly]; filterset_class=AccommodationFilter; search_fields=['name','description','address']; ordering_fields=['name','price_per_night']

class ActivityViewSet(viewsets.ModelViewSet):
    queryset=Activity.objects.select_related('destination').all(); serializer_class=ActivitySerializer; permission_classes=[IsAuthenticatedOrReadOnly]; filterset_class=ActivityFilter; search_fields=['name','description','requirements']; ordering_fields=['name','price','created_at']
    def get_queryset(self): return super().get_queryset().prefetch_related('daily_plans')

class BookingViewSet(viewsets.ModelViewSet):
    filterset_class=BookingFilter; 
    search_fields=['confirmation_code','notes']; 
    ordering_fields=['created_at','price','booking_date']

    def get_queryset(self): 
        return Booking.objects.filter(user=self.request.user).select_related('accommodation','activity','itinerary')
    
    def get_serializer_class(self): 
        return BookingDetailSerializer if self.action=='retrieve' else BookingSerializer
    
    def get_permissions(self):
        if self.action in ('update','partial_update','destroy'): return [IsAuthenticated(),IsBookingOwner()]
        return [IsAuthenticated()]
    
    @action(detail=True,methods=['post'])
    def confirm(self,request,pk=None): 
        booking=self.get_object(); booking.confirm(); 
        return Response(BookingDetailSerializer(booking).data)
    
    @action(detail=True,methods=['post'])
    def cancel(self,request,pk=None): 
        booking=self.get_object(); 
        booking.cancel(); 
        return Response({'status':booking.status,'refund':str(booking.price)})

class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Recommendation.objects.select_related('user','destination'); serializer_class=RecommendationSerializer; permission_classes=[IsAuthenticated]
    def get_queryset(self): 
        return super().get_queryset().filter(user=self.request.user)
