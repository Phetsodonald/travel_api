from django.urls import path
from .views import (
    register, login, UserProfileView, PasswordChangeView,
    password_reset_request, password_reset_confirm,
)
app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', password_reset_request, name='password-reset'),
    path('password/reset/confirm/', password_reset_confirm, name='password-reset-confirm'),
]
