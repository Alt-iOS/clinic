import random, string, datetime
from django.db import models


# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField(blank=False, null=True)
    sex = models.CharField(max_length=1, null=False)
    height = models.FloatField(null=False, max_length=3)
    starting_weight = models.FloatField(max_length=6, null=False)
    aerobics = models.BooleanField(default=False)
    recent_weight = models.FloatField(max_length=6, null=False)
    public_id = models.CharField(max_length=10, null=False, unique=True)


    def save(self, *args, **kwargs):
        if self.recent_weight is None:
            self.recent_weight = self.starting_weight
        if self.public_id.__eq__(''):
            self.public_id = ''.join(random.choices(self.name + self.surname, k=10))
        super(Patient, self).save(*args, **kwargs)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) ##change to one to many
    date = models.DateField(blank=False, null=True, default=datetime.date.today)
    new_weight = models.FloatField(max_length=6, null=False)
    observations = models.CharField(max_length=200, null=False)

    def save(self, *args, **kwargs):
        most_recent_appt = Appointment.objects.filter(patient=self.patient).order_by('-date').first()
        self.patient.recent_weight = most_recent_appt.new_weight
        self.patient.save()
        super(Appointment, self).save(*args, **kwargs)
