from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Appointment, Membership, ContactMessage

# Page views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def membership(request):
    return render(request, 'membership.html')

def appointments(request):
    return render(request, 'appointments.html')

def contact(request):
    return render(request, 'contact.html')

# Admin dashboard view
def admin_dashboard(request):
    # Only allow staff or superuser
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden('You do not have permission to view this page.')

    appointments = Appointment.objects.all().order_by('-id')
    memberships = Membership.objects.all().order_by('-id')
    contacts = ContactMessage.objects.all().order_by('-id')

    context = {
        'appointments': appointments,
        'memberships': memberships,
        'contacts': contacts,
    }
    return render(request, 'admin_dashboard.html', context)

# Form submission views
def book_appointment(request):
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                service_type=request.POST.get('service_type'),
                appointment_date=request.POST.get('appointment_date'),
                appointment_time=request.POST.get('appointment_time'),
                details=request.POST.get('details')
            )
            messages.success(request, 'Appointment booked successfully! We will contact you within 24 hours.')
            return redirect('appointments')
        except Exception as e:
            messages.error(request, 'There was an error booking your appointment. Please try again.')
            return redirect('appointments')
    return redirect('appointments')

def register_membership(request):
    if request.method == 'POST':
        try:
            membership = Membership.objects.create(
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                membership_type=request.POST.get('membership_type'),
                organization=request.POST.get('organization', ''),
                message=request.POST.get('message', '')
            )
            messages.success(request, 'Membership registration successful! We will contact you soon.')
            return redirect('membership')
        except Exception as e:
            messages.error(request, 'There was an error with your registration. Please try again.')
            return redirect('membership')
    return redirect('membership')

def contact_form(request):
    if request.method == 'POST':
        try:
            contact = ContactMessage.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                subject=request.POST.get('subject'),
                message=request.POST.get('message')
            )
            messages.success(request, 'Message sent successfully! We will get back to you soon.')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again.')
            return redirect('contact')
    return redirect('contact')