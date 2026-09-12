from rest_framework import viewsets, mixins, permissions, status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import User, LawyerProfile, ClientProfile, Case, Appointment, Message
from .serializers import (
    UserSerializer,
    LawyerProfileSerializer,
    ClientProfileSerializer,
    CaseSerializer,
    AppointmentSerializer,
    MessageSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response


class MessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows creating a new Message via POST.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for User instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LawyerProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for Lawyer profiles.
    """
    queryset = LawyerProfile.objects.select_related('user').all()
    serializer_class = LawyerProfileSerializer
    permission_classes = [AllowAny]
    
    
    @action(detail=False, methods=['get'], pagination_class=None)
    def all(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = [
            {key: value for key, value in lawyer.items() if key != 'description'}
            for lawyer in serializer.data
        ]
        return Response(data)

    @action(detail=False, methods=['get'], pagination_class=None)
    def get_lawyers(self, request):
        queryset = self.get_queryset()
        data = [
            {'id': lawyer.id, 'name': lawyer.full_name}
            for lawyer in queryset
        ]
        return Response(data)
    
    
    


class ClientProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for Client profiles.
    """
    queryset = ClientProfile.objects.select_related('user').all()
    serializer_class = ClientProfileSerializer
    permission_classes = [AllowAny]


class CaseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for Cases with pre-fetched relations for performance.
    """
    queryset = Case.objects.select_related('client', 'assigned_lawyer').all()
    serializer_class = CaseSerializer
    permission_classes = [AllowAny]


class AppointmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for Appointment slots.
    """
    queryset = Appointment.objects.select_related('lawyer', 'client').all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def book(self, request):
        """Creates an appointment for the requesting client with the given lawyer_id."""
        lawyer_id = request.data.get('lawyer_id')
       

        if not lawyer_id :
            return Response(
                {"error": "lawyer_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not hasattr(request.user, 'client_profile'):
            return Response(
                {"error": "This account does not have a client profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

        lawyer = get_object_or_404(LawyerProfile, pk=lawyer_id)
        appointment = Appointment.objects.create(
            lawyer=lawyer,
            client=request.user.client_profile,
        )

        return Response(
            AppointmentSerializer(appointment).data,
            status=status.HTTP_201_CREATED,
        )