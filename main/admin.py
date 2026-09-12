from django.contrib.admin import forms
from django import forms
from unfold.admin import ModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LawyerProfile, ClientProfile, Case, Appointment, Message
from django.utils.html import format_html, format_html_join
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE



# -------------------------------------------------------------------
# INLINE CONFIGURATIONS
# -------------------------------------------------------------------

class AppointmentInline(admin.TabularInline):
    """
    Allows Lawyers and Admins to manage weekly recurring slots
    directly inside the LawyerProfile admin view.
    """
    model = Appointment
    extra = 1
    fields = ( 'client', 'booking_date')
    readonly_fields = ('booking_date',)
    raw_id_fields = ('client',)


class LawyerProfileInline(admin.StackedInline):
    model = LawyerProfile
    can_delete = False


class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    can_delete = False


class LawyerCaseInline(admin.TabularInline):
    """Shows cases assigned to this lawyer directly on the LawyerProfile admin view."""
    model = Case
    fk_name = 'assigned_lawyer'
    extra = 0
    fields = ('case_number', 'title', 'client', 'status', 'last_updated')
    readonly_fields = ('last_updated',)


class ClientCaseInline(admin.TabularInline):
    """Shows cases filed by this client directly on the ClientProfile admin view."""
    model = Case
    fk_name = 'client'
    extra = 0
    fields = ('case_number', 'title', 'assigned_lawyer', 'status', 'last_updated')
    readonly_fields = ('last_updated',)


# -------------------------------------------------------------------
# MODEL ADMIN REGISTRATIONS
# -------------------------------------------------------------------
@admin.register(Message)
class MessageAdmin(ModelAdmin):
  
    # Columns displayed in the main admin list view
    list_display = (
        'id', 
        'full_name', 
        'email', 
        'phone', 
        'subject', 
        'message_date'
    )
    
    # Clickable fields to open the detail view
    list_display_links = ('id', 'full_name', 'subject')
    
    # Filters in the right sidebar
    list_filter = ('message_date',)
    
    # Search box functionality across contact fields
    search_fields = (
        'full_name', 
        'email', 
        'phone', 
        'subject', 
        'message'
    )
    
    # Default ordering (newest messages first)
    ordering = ('-message_date',)
    
    # Number of records per page
    list_per_page = 25
    
    # Mark auto-populated timestamp as read-only in the detail form
    readonly_fields = ('message_date',)
    
    # Organize detail view into clean fieldsets
    fieldsets = (
        ('Sender Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'message_date')
        }),
    )

    # Optional: Prevent editing of messages in admin (read-only inbox style)
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
  
    """
    Custom User Admin displaying user role choices (Lawyer vs Client).
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Role Info', {'fields': ('role', 'phone_number')}),
        ('Related Cases', {'fields': ('related_cases',)}),
    )
    readonly_fields = ('related_cases',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')

    @admin.display(description="Cases")
    def related_cases(self, obj):
        # Cases reach the User through whichever profile (lawyer or client) it owns.
        profile = getattr(obj, 'lawyer_profile', None) or getattr(obj, 'client_profile', None)
        if not profile:
            return "No associated profile"
        cases = profile.cases.all()
        if not cases:
            return "No cases"
        return format_html_join(
            "",
            '<div>{} - {} ({})</div>',
            ((case.case_number, case.title, case.get_status_display()) for case in cases)
        )






@admin.register(LawyerProfile)
class LawyerProfileAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    """
    Lawyer Admin featuring the AppointmentInline to create and manage time slots.
    """
    list_display = ('full_name', 'designation')
    search_fields = ('full_name', 'designation')
    inlines = [AppointmentInline, LawyerCaseInline]
 
    



@admin.register(ClientProfile)
class ClientProfileAdmin(ModelAdmin):
   
    list_display = ('full_name', 'user')
    search_fields = ('full_name', 'user__email')
    inlines = [ClientCaseInline]


@admin.register(Case)
class CaseAdmin(ModelAdmin):
    
    list_display = ('case_number', 'title', 'client', 'assigned_lawyer', 'status', 'last_updated')
    list_filter = ('status', 'assigned_lawyer')
    search_fields = ('case_number', 'title', 'client__full_name')


@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    """
    Standalone Appointment Admin for global oversight of all slots,
    with an action to manually reset slots for the new week.
    """
    list_display = ('lawyer', 'client', 'booking_date')
    list_filter = ('lawyer',)
    search_fields = ('lawyer__full_name', 'client__full_name')
  
    

   