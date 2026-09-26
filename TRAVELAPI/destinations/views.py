from django.db.models import Q,Count
from rest_framework import status,viewsets
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Destination,DestinationPhoto
from .serializers import DestinationListSerializer,DestinationDetailSerializer,DestinationPhotoSerializer
from .filters import DestinationFilter
from .permissions import IsDestinationAdminOrReadOnly
from TRAVELAPI.pagination import SmallResultsPagination

class DestinationSearchView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get(self,request):
        q=request.query_params.get('q','').strip(); qs=Destination.objects.filter(is_active=True)
        if q: qs=qs.filter(Q(name__icontains=q)|Q(country__icontains=q)|Q(description__icontains=q))
        qs=qs.annotate(review_count=Count('reviews')).order_by('-review_count','name')
        return Response(DestinationListSerializer(qs[:50],many=True,context={'request':request}).data)
    
    def post(self,request):
        if not request.user.is_authenticated: return Response({'detail':'Authentication required.'},status=401)
        request.user.travel_preferences=request.data; request.user.save(update_fields=['travel_preferences']); return Response({'saved':True})

class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Destination.objects.filter(is_active=True).prefetch_related('photos'); permission_classes=[IsDestinationAdminOrReadOnly]
    filterset_class=DestinationFilter; search_fields=['name','description','country']; ordering_fields=['name','avg_daily_cost','created_at']; pagination_class=SmallResultsPagination
    
    def get_serializer_class(self): return DestinationDetailSerializer if self.action=='retrieve' else DestinationListSerializer
    
    @action(detail=True,methods=['get'])
    def popular_activities(self,request,pk=None):
        d=self.get_object(); from bookings.serializers import ActivitySerializer
        activities=d.activities.annotate(booking_count=Count('bookings')).order_by('-booking_count','name')[:10]
        return Response(ActivitySerializer(activities,many=True).data)
    
    @action(detail=True,methods=['get'])
    def weather_info(self,request,pk=None):
        d=self.get_object(); return Response({'destination':d.name,'climate':d.climate,'best_time_to_visit':d.best_time_to_visit})

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def destination_search_preferences(request):
    """GET saved destination preferences; POST updates them."""
    if request.method=='GET': return Response(request.user.travel_preferences or {})
    request.user.travel_preferences=request.data; request.user.save(update_fields=['travel_preferences']); return Response({'detail':'Preferences saved.'},status=201)
