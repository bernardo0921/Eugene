from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('membership/', views.membership, name='membership'),
    path('appointments/', views.appointments, name='appointments'),
    path('contact/', views.contact, name='contact'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    # CRUD: Appointments
    path('admin/appointments/create/', views.appointment_create, name='appointment_create'),
    path('admin/appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('admin/appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),

    # CRUD: Memberships
    path('admin/memberships/create/', views.membership_create, name='membership_create'),
    path('admin/memberships/<int:pk>/edit/', views.membership_edit, name='membership_edit'),
    path('admin/memberships/<int:pk>/delete/', views.membership_delete, name='membership_delete'),

    # CRUD: Contacts
    path('admin/contacts/<int:pk>/edit/', views.contact_edit, name='contact_edit'),
    path('admin/contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),

    # Analytics
    path('admin/analytics/', views.analytics, name='admin_analytics'),

    # Form submission endpoints
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('register-membership/', views.register_membership, name='register_membership'),
    path('contact-form/', views.contact_form, name='contact_form'),
]