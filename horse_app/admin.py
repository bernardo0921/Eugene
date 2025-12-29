from django.contrib import admin
from .models import Appointment, Membership, ContactMessage

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service_type', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'service_type', 'appointment_date', 'created_at']
    search_fields = ['name', 'email', 'phone', 'details']
    list_editable = ['status']
    date_hierarchy = 'appointment_date'
    ordering = ['-created_at']

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'membership_type', 'organization', 'status', 'created_at']
    list_filter = ['membership_type', 'status', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'organization']
    list_editable = ['status']
    ordering = ['-created_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    ordering = ['-created_at']
    readonly_fields = ['created_at']