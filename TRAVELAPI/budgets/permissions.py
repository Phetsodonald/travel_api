from rest_framework.permissions import BasePermission

class IsBudgetOwner(BasePermission):
    def has_object_permission(self,request,view,obj):
         return obj.itinerary.owner==request.user
