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

    # Form submission endpoints
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('register-membership/', views.register_membership, name='register_membership'),
    path('contact-form/', views.contact_form, name='contact_form'),
]