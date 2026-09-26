from datetime import date
from django.db import transaction
from django.db.models import Q,F,Count,Sum,Prefetch,Avg
from rest_framework import generics,status,viewsets
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Itinerary,DailyPlan,Collaboration
from .serializers import ItineraryListSerializer,ItineraryDetailSerializer,ItineraryCreateUpdateSerializer,DailyPlanSerializer,CollaborationSerializer
from .filters import ItineraryFilter
from .permissions import IsTripOwner,IsTripOwnerOrCollaborator,CanEditItinerary

class ItineraryListCreateView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    def get_queryset(self): 
        return Itinerary.objects.filter(Q(owner=self.request.user)|Q(collaborators=self.request.user)).select_related('destination','owner').prefetch_related('daily_plans','bookings').only('id','title','destination','owner','start_date','end_date','budget','actual_spent','status').distinct()
    
    def get_serializer_class(self): 
        return ItineraryCreateUpdateSerializer if self.request.method=='POST' else ItineraryListSerializer
    
    def perform_create(self,serializer): 
        serializer.save(owner=self.request.user)

class ItineraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated,CanEditItinerary]
    def get_queryset(self): 
        return Itinerary.objects.filter(Q(owner=self.request.user)|Q(collaborators=self.request.user)).select_related('destination','owner').prefetch_related('daily_plans','collaborations').distinct()
    
    def get_serializer_class(self): 
        return ItineraryCreateUpdateSerializer if self.request.method in ('PUT','PATCH') else ItineraryDetailSerializer

class TripCollaborationView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated,IsTripOwner]
    def get_object(self): 
        return Itinerary.objects.prefetch_related('collaborations__user').get(pk=self.kwargs['trip_id'])
    
    def get(self,request,trip_id): 
        return Response(CollaborationSerializer(self.get_object().collaborations.all(),many=True).data)
    
    def post(self,request,trip_id):
        trip=self.get_object(); from accounts.models import User
        user=User.objects.get(pk=request.data.get('user_id')); role=request.data.get('role','viewer'); c,created=Collaboration.objects.get_or_create(itinerary=trip,user=user,defaults={'role':role})
        if not created: c.role=role; c.save(update_fields=['role'])
        return Response(CollaborationSerializer(c).data,status=201 if created else 200)
    
    def patch(self,request,trip_id,user_id):
        c=Collaboration.objects.get(itinerary=self.get_object(),user_id=user_id); c.role=request.data.get('role',c.role); c.save(update_fields=['role']); return Response(CollaborationSerializer(c).data)
    
    def delete(self,request,trip_id,user_id): Collaboration.objects.filter(itinerary=self.get_object(),user_id=user_id).delete(); return Response(status=204)
class DailyPlanListCreateView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=DailyPlanSerializer
    
    def get_queryset(self): 
        return DailyPlan.objects.filter(itinerary_id=self.kwargs['trip_id']).select_related('itinerary').prefetch_related('activities')
    
    def perform_create(self,serializer): 
        serializer.save(itinerary=Itinerary.objects.get(pk=self.kwargs['trip_id']))

class ItineraryViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    filterset_class=ItineraryFilter; search_fields=['title','description','destination__name']; ordering_fields=['created_at','start_date','budget']
    
    def get_queryset(self): 
        return Itinerary.objects.filter(Q(owner=self.request.user)|Q(collaborators=self.request.user)|Q(is_public=True)).select_related('destination','owner').prefetch_related('daily_plans','bookings','collaborations__user').distinct()
    
    def get_serializer_class(self):
        if self.action=='list': return ItineraryListSerializer
        if self.action in ('create','update','partial_update'): return ItineraryCreateUpdateSerializer
        return ItineraryDetailSerializer
    
    def get_permissions(self):
        if self.action in ('update','partial_update','destroy'): return [IsAuthenticated(),CanEditItinerary()]
        return [IsAuthenticated()]
    
    def perform_create(self,serializer): serializer.save(owner=self.request.user)
    
    @action(detail=True,methods=['post'])
    def duplicate(self,request,pk=None):
        original=self.get_object(); clone=Itinerary.objects.create(title=f'{original.title} (Copy)',description=original.description,destination=original.destination,owner=request.user,start_date=original.start_date,end_date=original.end_date,budget=original.budget,is_public=False)
        for plan in original.daily_plans.prefetch_related('activities'):
            p=DailyPlan.objects.create(itinerary=clone,day_number=plan.day_number,date=plan.date,title=plan.title,notes=plan.notes); p.activities.set(plan.activities.all())
        return Response(ItineraryDetailSerializer(clone).data,status=201)
    
    @action(detail=True,methods=['get'])
    def export_pdf(self,request,pk=None): return Response({'detail':'PDF export endpoint ready. Upload/generated file can be attached to the itinerary.','itinerary_id':self.get_object().id})
    
    @action(detail=True,methods=['post'],url_path='share')
    def share_with_user(self,request,pk=None):
        trip=self.get_object(); from accounts.models import User
        user=User.objects.get(pk=request.data.get('user_id')); c=Collaboration.objects.create(itinerary=trip,user=user,role=request.data.get('role','viewer')); return Response(CollaborationSerializer(c).data,status=201)
    
    @action(detail=False,methods=['get'])
    def upcoming_trips(self,request): return Response(ItineraryListSerializer(self.get_queryset().filter(start_date__gte=date.today()).order_by('start_date'),many=True).data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def trip_search(request):
    if request.method=='POST':
        request.user.travel_preferences=request.data; request.user.save(update_fields=['travel_preferences']); return Response({'detail':'Search preferences saved.'},status=201)
    q=request.query_params.get('q',''); qs=Itinerary.objects.filter(Q(owner=request.user)|Q(collaborators=request.user)|Q(is_public=True)).filter(Q(title__icontains=q)|Q(description__icontains=q)).select_related('destination').prefetch_related('collaborations').distinct()
    return Response(ItineraryListSerializer(qs[:20],many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_trip_report(request,trip_id):
    try:
        trip=Itinerary.objects.select_related('destination','owner').prefetch_related('daily_plans','bookings').get(Q(owner=request.user)|Q(collaborators=request.user),id=trip_id)
        booking_total=trip.bookings.aggregate(total=Sum('price'))['total'] or 0
        expense_total=trip.expenses.aggregate(total=Sum('amount'))['total'] or 0
        return Response({'trip':trip.title,'destination':trip.destination.name,'duration_days':trip.duration_days,'budget':trip.budget,'booking_total':booking_total,'expense_total':expense_total,'budget_remaining':trip.budget-booking_total-expense_total,'daily_plans':trip.daily_plans.count()})
    except Itinerary.DoesNotExist: return Response({'detail':'Trip not found.'},status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_update_bookings(request):
    """Bulk update booking statuses atomically."""
    from bookings.models import Booking
    items=request.data.get('bookings',[])
    updated=0
    try:
        with transaction.atomic():
            for item in items:
                b=Booking.objects.get(pk=item['id'],user=request.user); b.status=item['status']; b.save(update_fields=['status','updated_at']); updated+=1
    except (Booking.DoesNotExist,KeyError) as exc: return Response({'detail':f'Invalid booking payload: {exc}'},status=400)
    return Response({'updated':updated})

class TripAnalyticsViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    def list(self,request):
        qs=Itinerary.objects.filter(owner=request.user).defer('description'); return Response({'trip_count':qs.count(),'average_budget':qs.aggregate(value=Avg('budget'))['value'] or 0,'total_spent':qs.aggregate(value=Sum('actual_spent'))['value'] or 0})
    
    @action(detail=False,methods=['get'])
    def budget_summary(self,request):
        return Response(Itinerary.objects.filter(owner=request.user).annotate(expense_total=Sum('expenses__amount')).values('id','title','budget','expense_total'))
    
    @action(detail=False,methods=['get'])
    def destination_preferences(self,request):
        return Response(list(Itinerary.objects.filter(owner=request.user).values('destination__country','destination__category').annotate(trips=Count('id')).order_by('-trips')))
