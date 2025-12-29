from django.db import models
from django.utils import timezone

class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('industrial-wiring', 'Industrial & Domestic Wiring'),
        ('solar', 'Solar Installation & Maintenance'),
        ('cctv', 'CCTV Systems'),
        ('smart-home', 'Smart Home & Automation'),
        ('satellite', 'Satellite Installation'),
        ('maintenance', 'Electrical Maintenance & Repairs'),
        ('consultation', 'General Consultation'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    details = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.service_type} on {self.appointment_date}"

class Membership(models.Model):
    MEMBERSHIP_TYPES = [
        ('partner', 'Partner'),
        ('apprentice', 'Apprentice'),
        ('intern', 'Intern'),
    ]
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES)
    organization = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ])
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.membership_type}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"