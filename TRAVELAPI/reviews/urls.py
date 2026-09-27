from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet,RatingSummaryViewSet

router=DefaultRouter(); 
router.register('reviews',ReviewViewSet,basename='review'); 
router.register('ratings',RatingSummaryViewSet,basename='rating')
app_name='reviews'; 
urlpatterns=[path('',include(router.urls))]
