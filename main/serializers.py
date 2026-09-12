from rest_framework import serializers
from .models import User, LawyerProfile, ClientProfile, Case, Appointment, Message


# -------------------------------------------------------------------
# 1. User Serializer
# -------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'role', 
            'phone_number', 
            'profile_picture',
            'password'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


# -------------------------------------------------------------------
# 2. Lawyer Profile Serializer

# -------------------------------------------------------------------



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'message_date', 'full_name', 'email', 'phone', 'subject', 'message']
        read_only_fields = ['id', 'message_date']


class LawyerProfileSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = LawyerProfile
        fields = [
            'id',
            'full_name', 
            'designation',
            'bio', 
            'description',
            'lawyer_photo'
        ]
        read_only_fields = ['id']


# -------------------------------------------------------------------
# 3. Client Profile Serializer
# -------------------------------------------------------------------
class ClientProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = ClientProfile
        fields = [
            'id', 
            'user', 
            'user_details', 
            'full_name', 
            'address'
        ]
        read_only_fields = ['id', 'user_details']


# -------------------------------------------------------------------
# 4. Case Serializer
# -------------------------------------------------------------------
class CaseSerializer(serializers.ModelSerializer):
   
    assigned_lawyer_details = LawyerProfileSerializer(source='assigned_lawyer', read_only=True)

    class Meta:
        model = Case
        fields = [
            'id', 
            'title', 
            'case_number', 
            'description', 
            'status', 
            
            'assigned_lawyer', 
            'assigned_lawyer_details', 
            'last_updated', 
            'created_at'
        ]
        read_only_fields = ['id', 'last_updated', 'created_at', 'assigned_lawyer_details']


# -------------------------------------------------------------------
# 5. Appointment Serializer
# -------------------------------------------------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    lawyer_details = LawyerProfileSerializer(source='lawyer', read_only=True)
    client_details = ClientProfileSerializer(source='client', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 
            'lawyer', 
            'lawyer_details', 
           
            'client', 
            'client_details', 
          
            'booking_date', 
          
        ]
        read_only_fields = [
            'id', 
            'booking_date', 
         
            'lawyer_details', 
            'client_details'
        ]

    def validate(self, attrs):
        # Mirror the model clean() validation logic
       
        client = attrs.get('client', getattr(self.instance, 'client', None))

       

        return attrs


# -------------------------------------------------------------------
# 6. Dedicated Booking Action Serializer (Optional Helper)
# -------------------------------------------------------------------
class AppointmentBookingSerializer(serializers.Serializer):
    """
    Helper serializer specifically for handling client booking requests
    to trigger the model's custom book() method cleanly.
    """
    client_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True, default="")

    def update(self, instance, validated_data):
        try:
            client_profile = ClientProfile.objects.get(pk=validated_data['client_id'])
        except ClientProfile.DoesNotExist:
            raise serializers.ValidationError({"client_id": "Client profile does not exist."})

        instance.book(client_profile=client_profile, notes=validated_data.get('notes', ''))
        return instance