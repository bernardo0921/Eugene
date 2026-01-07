from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Appointment, Membership, ContactMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm, MembershipForm, ContactMessageForm
from django.db.models import Count

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

# Admin login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active and user.is_staff:
                login(request, user)
                messages.success(request, 'Successfully signed in.')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You do not have admin access.')
                return redirect('admin_login')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('admin_login')
    return render(request, 'admin_login.html')

# Admin logout view
def admin_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# Helper: staff-only check
def _require_staff(user):
    return user.is_authenticated and user.is_staff

# Admin dashboard view
@login_required
def admin_dashboard(request):
    # Only allow staff or superuser
    if not request.user.is_staff:
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

# CRUD: Appointments
@login_required
def appointment_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment created.')
            return redirect('admin_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'admin/crud/appointment_form.html', {'form': form})

@login_required
def appointment_edit(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated.')
            return redirect('admin_dashboard')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'admin/crud/appointment_form.html', {'form': form, 'object': appointment})

@login_required
def appointment_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted.')
        return redirect('admin_dashboard')
    return render(request, 'admin/crud/confirm_delete.html', {'object': appointment, 'type': 'Appointment'})

# CRUD: Memberships
@login_required
def membership_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membership created.')
            return redirect('admin_dashboard')
    else:
        form = MembershipForm()
    return render(request, 'admin/crud/membership_form.html', {'form': form})

@login_required
def membership_edit(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    membership = get_object_or_404(Membership, pk=pk)
    if request.method == 'POST':
        form = MembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membership updated.')
            return redirect('admin_dashboard')
    else:
        form = MembershipForm(instance=membership)
    return render(request, 'admin/crud/membership_form.html', {'form': form, 'object': membership})

@login_required
def membership_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    membership = get_object_or_404(Membership, pk=pk)
    if request.method == 'POST':
        membership.delete()
        messages.success(request, 'Membership deleted.')
        return redirect('admin_dashboard')
    return render(request, 'admin/crud/confirm_delete.html', {'object': membership, 'type': 'Membership'})

# CRUD: Contacts
@login_required
def contact_edit(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    contact = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        form = ContactMessageForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated.')
            return redirect('admin_dashboard')
    else:
        form = ContactMessageForm(instance=contact)
    return render(request, 'admin/crud/contact_form.html', {'form': form, 'object': contact})

@login_required
def contact_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    contact = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted.')
        return redirect('admin_dashboard')
    return render(request, 'admin/crud/confirm_delete.html', {'object': contact, 'type': 'Contact'})

# Analytics view
@login_required
def analytics(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    # Example analytics: counts per status and per service type
    appointments_by_status = Appointment.objects.values('status').annotate(count=Count('id')).order_by('-count')
    appointments_by_service = Appointment.objects.values('service_type').annotate(count=Count('id')).order_by('-count')
    memberships_by_type = Membership.objects.values('membership_type').annotate(count=Count('id')).order_by('-count')

    # Totals and simple stats
    total_appointments = Appointment.objects.count()
    total_members = Membership.objects.count()
    pending_count = Appointment.objects.filter(status='pending').count()
    completed_count = Appointment.objects.filter(status='completed').count()

    # Most popular service and most common membership (strings or None)
    most_popular_service = None
    most_common_membership = None
    if appointments_by_service:
        svc_key = appointments_by_service[0]['service_type']
        # Map the internal choice key to the human-friendly label
        most_popular_service = dict(Appointment.SERVICE_CHOICES).get(svc_key, svc_key)
    if memberships_by_type:
        mem_key = memberships_by_type[0]['membership_type']
        most_common_membership = dict(Membership.MEMBERSHIP_TYPES).get(mem_key, mem_key)

    context = {
        'appointments_by_status': list(appointments_by_status),
        'appointments_by_service': list(appointments_by_service),
        'memberships_by_type': list(memberships_by_type),
        'total_appointments': total_appointments,
        'total_members': total_members,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'most_popular_service': most_popular_service,
        'most_common_membership': most_common_membership,
    }
    return render(request, 'admin/analytics.html', context)

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

def handler404(request, exception=None):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
