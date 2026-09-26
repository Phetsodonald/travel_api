from rest_framework.permissions import BasePermission

class IsTripOwner(BasePermission):
    def has_object_permission(self,request,view,obj): 
        return obj.owner==request.user

class IsTripOwnerOrCollaborator(BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.owner==request.user or obj.collaborations.filter(user=request.user).exists()

class CanEditItinerary(BasePermission):
    def has_object_permission(self,request,view,obj):
        if obj.owner==request.user: return True
        c=obj.collaborations.filter(user=request.user).first(); 
        return bool(c and c.role in ('editor','admin'))
