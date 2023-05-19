from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_user, name='register'),
    path('register-patient/', views.register_patient, name='register_patient'),
    path('patient-info/', views.show_patient_info, name='patient_info'),
    path('dashboard_paginated/', views.PatientListView.as_view(), name='dashboard_paginated'),
    path('appointment/<str:public_id>/', views.appointment_view, name='appointment'),
    path('edit/<str:public_id>/', views.edit_patient, name='edit_patient'),

]