from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from .serializers import RegistrationSerializer,UserSerializer,LoginSerializer,PasswordChangeSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a user and return access/refresh JWT tokens."""
    s=RegistrationSerializer(data=request.data)
    if not s.is_valid(): return Response(s.errors,status=400)
    user=s.save(); refresh=RefreshToken.for_user(user)
    return Response({'user':UserSerializer(user).data,'tokens':{'refresh':str(refresh),'access':str(refresh.access_token)}},status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Authenticate a user and issue JWT tokens."""
    s=LoginSerializer(data=request.data)
    if not s.is_valid(): return Response(s.errors,status=401)
    user=s.validated_data['user']; refresh=RefreshToken.for_user(user)
    return Response({'user':UserSerializer(user).data,'tokens':{'refresh':str(refresh),'access':str(refresh.access_token)}})
class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's profile."""
    serializer_class=UserSerializer; permission_classes=[IsAuthenticated]
    def get_object(self): return self.request.user
class PasswordChangeView(generics.UpdateAPIView):
    """Change the authenticated user's password."""
    serializer_class=PasswordChangeSerializer; permission_classes=[IsAuthenticated]
    def get_object(self): return self.request.user
    def update(self,request,*args,**kwargs):
        s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); request.user.set_password(s.validated_data['new_password']); request.user.save(); update_session_auth_hash(request,request.user); return Response({'detail':'Password changed successfully.'})

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """Generate a password-reset token for an account email."""
    from django.contrib.auth import get_user_model
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode
    User = get_user_model()
    try:
        user = User.objects.get(email=request.data.get('email', ''))
    except User.DoesNotExist:
        return Response({'detail': 'If the email exists, reset instructions are available.'})
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return Response({'uid': uid, 'token': default_token_generator.make_token(user)})

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """Validate a reset token and set a new password."""
    from django.contrib.auth import get_user_model
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_str
    from django.utils.http import urlsafe_base64_decode
    User = get_user_model()
    try:
        user = User.objects.get(pk=force_str(urlsafe_base64_decode(request.data['uid'])))
    except (KeyError, ValueError, TypeError, User.DoesNotExist):
        return Response({'detail': 'Invalid reset request.'}, status=400)
    if not default_token_generator.check_token(user, request.data.get('token', '')):
        return Response({'detail': 'Invalid or expired token.'}, status=400)
    password = request.data.get('new_password', '')
    if len(password) < 8:
        return Response({'detail': 'Password must be at least 8 characters.'}, status=400)
    user.set_password(password)
    user.save(update_fields=['password'])
    return Response({'detail': 'Password reset successfully.'})
