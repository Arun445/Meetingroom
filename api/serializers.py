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
    reservation_from_date = serializers.SerializerMethodField()
    reservation_to_date = serializers.SerializerMethodField()

    class Meta:

        model = EmployeeReservations
        fields = ['employee', 'reservation',
                  'reservation_from_date', 'reservation_to_date']

    def get_reservation_from_date(self, obj):
        return obj.reservation.reserved_from

    def get_reservation_to_date(self, obj):
        return obj.reservation.reserved_to


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
        query = self.context['request'].query_params.get('keyword')
        if query == None:
            query = ''

        reservations = obj.reservation_set.filter(
            employee__first_name__icontains=query)
        serializer = ReservationSerializer(reservations, many=True)
        return serializer.data
