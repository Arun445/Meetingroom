from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class MeetingRoom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    title = models.CharField(max_length=100)
    reserved_from = models.DateTimeField()
    reserved_to = models.DateTimeField()
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    room = models.ForeignKey(
        MeetingRoom, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.title)

    def time_has_ended(self):
        time_ended = self.reserved_to < timezone.now()
        return time_ended


class EmployeeReservations(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.employee)

    def time_has_ended(self):
        time = self.reservation.reserved_to < timezone.now()
        return time
