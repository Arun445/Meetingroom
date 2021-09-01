from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (MeetingRoom, Reservation,
                     EmployeeReservations)


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['id']
        read_only_fields = ['username']


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Reservation
        fields = '__all__'


class EmployeeReservationsSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeReservations
        fields = '__all__'


class MeetingRoomSerializer(serializers.ModelSerializer):
    reservations = serializers.SerializerMethodField()

    class Meta:

        model = MeetingRoom
        fields = '__all__'

    def get_reservations(self, obj):
        reservations = obj.reservation_set.all()
        serializer = ReservationSerializer(reservations, many=True)
        return serializer.data
