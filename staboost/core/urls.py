from django.urls import path
from .views import RegistrationView, UserDetailView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
]
