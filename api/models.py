from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MeetingRoom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    title = models.CharField(max_length=100)
    reserved_from = models.DateTimeField()
    reserved_to = models.DateTimeField()
    user = models.ManyToManyField(User)
    room = models.ForeignKey(
        MeetingRoom, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title


class EmployeeReservations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.user)
