from django.urls import path
from .views import DestinationSearchView,destination_search_preferences

app_name='destinations'
urlpatterns=[
    path('search/',DestinationSearchView.as_view(),name='search'),
    path('preferences/',destination_search_preferences,name='preferences')
]
