from django import forms
from django.contrib.auth.models import User
from .models import Patient, Appointment
from django.utils import timezone


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser')
        labels = {
            'is_superuser': 'Is the user an admin?',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            print(f'[*** INFO ***] the passwords do not match')
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name', 'surname', 'date_of_birth', 'sex', 'height', 'starting_weight', 'aerobics')
        widgets = {'date_of_birth': forms.SelectDateWidget(years=range(1900, 2023)),
                   'starting_weight': forms.NumberInput(attrs={'steps': '0.1', 'min': '0.1', 'max': '300.0'}),
                   'height': forms.NumberInput(attrs={'steps': '0.01', 'min': '0.01', 'max': '2.5'}),
                   }
        labels = {
            'name': 'Name',
            'surname': 'Last name',
            'height': 'Height (m)',
            'starting_weight': 'Starting weight (kg)',
            'aerobics': 'Does the patient do aerobics?',
        }


class PatientRequestForm(forms.Form):
    public_id = forms.CharField(label='Public ID', max_length=10)


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('date', 'new_weight', 'observations')
        widgets = {'date': forms.SelectDateWidget(years=range(2020, timezone.now().year + 1)),
                   'new_weight': forms.NumberInput(attrs={'steps': '0.1', 'min': '0.1', 'max': '300.0'}),
                   'observations': forms.Textarea(attrs={'rows': 4, 'cols': 15})
                   }
        labels = {
            'date': 'Date of appointment',
            'new_weight': 'Recent weight (kg)',
            'observations': 'Observations',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now()


class EditPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name', 'surname', 'date_of_birth', 'sex', 'height', 'starting_weight', 'aerobics', 'active')
        widgets = {'date_of_birth': forms.SelectDateWidget(years=range(1900, 2023)),
                   'starting_weight': forms.NumberInput(attrs={'steps': '0.1', 'min': '0.1', 'max': '300.0'}),
                   'height': forms.NumberInput(attrs={'steps': '0.01', 'min': '0.01', 'max': '2.5'}),
                   'active': forms.CheckboxInput(),
                   }
        labels = {
            'name': 'Name',
            'surname': 'Last name',
            'height': 'Height (m)',
            'starting_weight': 'Starting weight (kg)',
            'aerobics': 'Does the patient do aerobics?',
            'active': 'Is the still patient active?',
        }

