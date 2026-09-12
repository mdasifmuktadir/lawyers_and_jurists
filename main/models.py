from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from pytz import timezone
from tinymce.models import HTMLField

# 1. Custom User Model with Role Types
class User(AbstractUser):
    class Role(models.TextChoices):
        LAWYER = "LAWYER", "Lawyer"
        CLIENT = "CLIENT", "Client"
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='user_pictures/', blank=True, null=True)
    

    def is_lawyer(self):
        return self.role == self.Role.LAWYER

    def is_client(self):
        return self.role == self.Role.CLIENT


# 2. Lawyer Profile Model
class LawyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lawyer_profile', limit_choices_to={'role': User.Role.LAWYER}, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    bio = HTMLField(blank=True)
    description = models.TextField(blank=True)
    lawyer_photo = models.ImageField(upload_to='lawyer_photos/', blank=True, null=True, help_text="Upload official lawyer photo")
    designation = models.CharField(max_length=1000, default="associate")

    def __str__(self):
        return f"Adv. {self.full_name} ({self.designation})"


# 3. Client Profile Model
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile', limit_choices_to={'role': User.Role.CLIENT})
    full_name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    

    def __str__(self):
        return f"Client: {self.full_name}"


# 4. Case Model (Track case status for clients)
class Case(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending Review"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        ON_HOLD = "ON_HOLD", "On Hold"
        CLOSED = "CLOSED", "Closed"

    title = models.CharField(max_length=255)
    case_number = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='cases')
    assigned_lawyer = models.ForeignKey(LawyerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='cases')
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case #{self.case_number} - {self.title} ({self.get_status_display()})"


# 5. Appointment Slot & Booking Model

class Appointment(models.Model):
    # class DaysOfWeek(models.TextChoices):
    #     MONDAY = "MONDAY", "Monday"
    #     TUESDAY = "TUESDAY", "Tuesday"
    #     WEDNESDAY = "WEDNESDAY", "Wednesday"
    #     THURSDAY = "THURSDAY", "Thursday"
    #     FRIDAY = "FRIDAY", "Friday"
    #     SATURDAY = "SATURDAY", "Saturday"
    #     SUNDAY = "SUNDAY", "Sunday"

    # DAY_MAP = {
    #     "MONDAY": 0, "TUESDAY": 1, "WEDNESDAY": 2, 
    #     "THURSDAY": 3, "FRIDAY": 4, "SATURDAY": 5, "SUNDAY": 6
    # }

    lawyer = models.ForeignKey('LawyerProfile', on_delete=models.CASCADE, related_name='appointments')
    # day_of_week = models.CharField(
    #     max_length=10, 
    #     choices=DaysOfWeek.choices,
    #     default=DaysOfWeek.MONDAY
    # )
    # start_time = models.TimeField()
    # end_time = models.TimeField()
    
    # Booking tracking
    # is_booked = models.BooleanField(default=False)
    client = models.ForeignKey('ClientProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    # notes_from_client = models.TextField(blank=True)
    
    # Dates
    booking_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="Timestamp when the booking was made")
    # appointment_date = models.DateField(null=True, blank=True, help_text="Calculated date of the upcoming meeting")


     

    # def book(self, client_profile, notes=""):
    #     """Call this method to book a slot. Calculates the exact upcoming appointment date."""
    #     now = timezone.now()
    #     today = now.date()
    #     target_weekday = self.DAY_MAP[self.day_of_week]
        
    #     # Calculate days until the next occurrence of this weekday
    #     days_ahead = target_weekday - today.weekday()
    #     if days_ahead < 0:  # Target day already passed this week
    #         days_ahead += 7
    #     elif days_ahead == 0 and self.start_time <= now.time():  # Today, but time passed
    #         days_ahead += 7

    #     self.is_booked = True
    #     self.client = client_profile
    #     self.notes_from_client = notes
    #     self.booking_date = now
    #     self.appointment_date = today + datetime.timedelta(days=days_ahead)
    #     self.save()

    # def reset_slot(self):
    #     """Clears booking info to make slot available for the new week."""
    #     self.is_booked = False
    #     self.client = None
    #     self.notes_from_client = ""
    #     self.booking_date = None
    #     self.appointment_date = None
    #     self.save()

    # def clean(self):
    #     if self.start_time and self.end_time and self.start_time >= self.end_time:
    #         raise ValidationError("End time must be after start time.")
    #     if self.is_booked and not self.client:
    #         raise ValidationError("A booked appointment must have an assigned client.")

    # def __str__(self):
    #     status = f"Booked by {self.client.full_name}" if self.is_booked else "Available"
    #     return f"{self.lawyer.full_name} | {self.get_day_of_week_display()} @ {self.start_time.strftime('%H:%M')} - [{status}]"
    
    
    
    
class Message(models.Model):
        id = models.AutoField(primary_key=True)
        message_date = models.DateTimeField(auto_now_add=True)
        full_name = models.CharField(max_length=1000)
        email= models.EmailField()
        phone = models.CharField(max_length=200)
        subject = models.CharField(max_length=1000)
        message = models.TextField()
    
    

