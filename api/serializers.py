from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (MeetingRoom, Reservation,
                     EmployeeReservations)


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = User
        fields = ['id', 'username', 'email', 'full_name']

    def get_full_name(self, obj):
        full_name = obj.first_name + ' ' + obj.last_name

        return full_name


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Reservation
        fields = '__all__'


class EmployeeReservationsSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeReservations
        fields = '__all__'


class MeetingRoomSerializer(serializers.ModelSerializer):

    class Meta:

        model = MeetingRoom
        fields = '__all__'


class MeetingRoomSerializerWithReservations(serializers.ModelSerializer):
    reservations = serializers.SerializerMethodField()

    class Meta:

        model = MeetingRoom
        fields = '__all__'

    def get_reservations(self, obj):
        reservations = obj.reservation_set.all()
        serializer = ReservationSerializer(reservations, many=True)
        return serializer.data
