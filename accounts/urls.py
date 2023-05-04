from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('register/',views.register_user, name='register'),
    path('register-patient/',views.register_patient, name='register_patient'),
    path('patient-info/',views.show_patient_info, name='patient_info'),
]