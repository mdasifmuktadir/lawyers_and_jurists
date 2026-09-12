from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    LawyerProfileViewSet,
    ClientProfileViewSet,
    CaseViewSet,
    AppointmentViewSet,
    MessageViewSet, 
    
    )

# Initialize the DRF DefaultRouter
router = DefaultRouter()

# Register each ViewSet with a URL prefix
router.register(r'users', UserViewSet, basename='user')
router.register(r'lawyers', LawyerProfileViewSet, basename='lawyerprofile')
router.register(r'clients', ClientProfileViewSet, basename='clientprofile')
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'message', MessageViewSet, basename='message')

urlpatterns = [
    # Include all auto-generated router URLs
    path('', include(router.urls)),
]