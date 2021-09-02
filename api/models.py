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
        return self.title

    def is_reservation_ended_(self):
        time = self.reserved_to < timezone.now()
        return time


class EmployeeReservations(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.employee)
