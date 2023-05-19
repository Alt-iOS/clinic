from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic import ListView, FormView, CreateView
from .forms import LoginForm, UserRegistrationForm, PatientRegistrationForm, PatientRequestForm, AppointmentForm, \
    EditPatientForm
from django.contrib.auth.decorators import user_passes_test
from .models import Patient, Appointment
from django.utils.decorators import method_decorator


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser:
                        return HttpResponse('Authenticated successfully as admin')
                    elif user.is_staff:
                        return HttpResponse('Authenticated successfully as assistant')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            print(f'[*** INFO ***] the form is not invalid')
    else:
        print(f'[*** INFO ***] USING GET , the form has not been submitted')
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.is_superuser:
        patients_info = Patient.objects.filter(active=True).values()
    elif request.user.is_staff:
        patients_info = Patient.objects.filter(active=True).values('name', 'surname', 'sex', 'aerobics', 'public_id')
    else:
        return HttpResponse('You are not authorized to view this page')
    patients_info = sorted(patients_info, key=lambda x:  (x['surname'].lower(), x['surname']))
    return render(request, 'account/dashboard.html', {'patients_info': patients_info, 'section': 'dashboard'})


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class PatientListView(ListView):
    model = Patient
    context_object_name = 'patients_info'
    paginate_by = 5
    template_name = 'account/dashboard.html'

    def get_queryset(self):
        return Patient.objects.filter(active=True).values()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        context['patients_info'] = sorted(context['patients_info'], key=lambda x: (x['surname'].lower(), x['surname']))
        return context

@login_required
@user_passes_test(lambda u: u.is_superuser)
def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            if new_user.is_superuser:
                new_user.is_staff = False
            else:
                new_user.is_staff = True
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user, 'section': 'register staff'})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form, 'section': 'register staff'})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def register_patient(request):
    if request.method == 'POST':
        patient_form = PatientRegistrationForm(request.POST)
        if patient_form.is_valid():
            new_patient = patient_form.save(commit=False)
            new_patient.save()
            return dashboard(request)
    else:
        patient_form = PatientRegistrationForm()
        return render(request, 'account/register.html', {'user_form': patient_form, 'section': 'patient registration'})


def show_patient_info(request):
    form = PatientRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        public_id = form.cleaned_data['public_id']
        patient = Patient.objects.get(public_id=public_id)
        appointments = Appointment.objects.filter(patient=patient).values()
        appointments = sorted(appointments, key=lambda x: x['date'], reverse=True)
        return render(request, 'account/patient_info.html', {'patient': patient, 'form': form, 'appointments': appointments})
    return render(request, 'account/patient_info.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def appointment_view(request, public_id):
    patient = get_object_or_404(Patient, public_id=public_id)
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            new_appointment = appointment_form.save(commit=False)
            new_appointment.patient = patient
            new_appointment.save()
            appointments = Appointment.objects.filter(patient=patient).values()
            appointments = sorted(appointments, key=lambda x: x['date'], reverse=True)
    else:
        appointments = Appointment.objects.filter(patient=patient).values()
        appointments = sorted(appointments, key=lambda x: x['date'], reverse=True)
        appointment_form = AppointmentForm()
    if len(appointments) == 0:
        this_appointment = {'BMI': '0 appointments'}
        second_last_appointments = {'BMI': '0 appointments'}
    elif len(appointments) < 2:
        this_appointment = appointments[0]
        second_last_appointments = {'BMI': 'Only one appointment'}
    else:
        this_appointment = appointments[0]
        second_last_appointments = appointments[1]
    return render(request, 'account/appointment.html', {'form': appointment_form, 'appointments': appointments,
                                                        'patient': patient, 'this': this_appointment,
                                                        'second_last_appointments': second_last_appointments})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_patient(request, public_id):
    patient = get_object_or_404(Patient, public_id=public_id)
    edit_form = EditPatientForm(request.POST or None, instance=patient)
    if request.method == 'POST' and edit_form.is_valid():
        edit_form.save()
    return render(request, 'account/edit_patient.html', {'form': edit_form, 'patient': patient})
