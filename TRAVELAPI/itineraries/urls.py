from django.urls import path
from .views import ItineraryListCreateView,ItineraryDetailView,TripCollaborationView,DailyPlanListCreateView,trip_search,generate_trip_report,bulk_update_bookings
app_name='itineraries'
urlpatterns=[path('',ItineraryListCreateView.as_view(),name='list-create'),path('search/',trip_search,name='trip-search'),path('bulk-update-bookings/',bulk_update_bookings,name='bulk-update-bookings'),path('<int:trip_id>/',ItineraryDetailView.as_view(),name='detail'),path('<int:trip_id>/report/',generate_trip_report,name='trip-report'),path('<int:trip_id>/collaborators/',TripCollaborationView.as_view(),name='collaborators'),path('<int:trip_id>/days/',DailyPlanListCreateView.as_view(),name='daily-plans')]
