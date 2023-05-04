from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, PatientRegistrationForm, ShowPatientInfoForm
from django.contrib.auth.decorators import user_passes_test
from .models import Patient


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
        patients_info = Patient.objects.all().values()
    elif request.user.is_staff:
        patients_info = Patient.objects.values('name', 'surname', 'sex', 'aerobics')
    else:
        return HttpResponse('You are not authorized to view this page')
    patients_info = sorted(patients_info, key=lambda x: x['surname'])
    return render(request, 'account/dashboard.html', {'patients_info': patients_info, 'section': 'dashboard'})


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
            return render(request, 'account/register_done.html', {'new_patient': new_patient, 'section': 'patient registration'})
    else:
        patient_form = PatientRegistrationForm()
        return render(request, 'account/register.html', {'user_form': patient_form, 'section': 'patient registration'})


def show_patient_info(request):
    form = ShowPatientInfoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        public_id = form.cleaned_data['public_id']
        patient = Patient.objects.get(public_id=public_id)
        return render(request, 'account/patient_info.html', {'patient': patient, 'form': form})
    return render(request, 'account/patient_info.html', {'form': form})
