from django.contrib import admin
from .models import Reservation, MeetingRoom, EmployeeReservations
# Register your models here.
admin.site.register(Reservation)
admin.site.register(MeetingRoom)
admin.site.register(EmployeeReservations)
