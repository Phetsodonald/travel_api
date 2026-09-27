from django.db.models import Avg,Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Review,RatingSummary
from .serializers import ReviewSerializer,RatingSummarySerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class=ReviewSerializer; 
    permission_classes=[IsAuthenticated]; 
    search_fields=['title','content']; 
    ordering_fields=['rating','created_at']

    def get_queryset(self): 
        return Review.objects.select_related('user','destination','activity','accommodation').filter(user=self.request.user)
    
    @action(detail=True,methods=['post'])
    def helpful(self,request,pk=None):
        review=self.get_object(); review.helpful_count+=1; review.save(update_fields=['helpful_count']); return Response({'helpful_count':review.helpful_count})

class RatingSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=RatingSummary.objects.select_related('destination'); 
    serializer_class=RatingSummarySerializer; 
    permission_classes=[IsAuthenticated]
