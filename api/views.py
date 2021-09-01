from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmployeeReservationsSerializer, MeetingRoomSerializer, ReservationSerializer, EmployeeReservations
from .models import (MeetingRoom, Reservation,
                     EmployeeReservations)
from rest_framework import serializers, status


@api_view(['POST'])
def create_meeting_room(request):

    serializer = MeetingRoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_meeting_rooms(request):
    rooms = MeetingRoom.objects.all()
    serializer = MeetingRoomSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_meeting_room(request, pk):
    room = MeetingRoom.objects.get(pk=pk)
    serializer = MeetingRoomSerializer(room, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_reservations(request):
    reservations = Reservation.objects.all()
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_reservation(request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        #reservation = Reservation.objects.get(id=serializer.data['id'])
        # for i in serializer.data['user']:
        # reservation.employeereservations_set.create(
        # user=i, reservation=serializer.data['id'])

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def cancel_reservation(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    reservation.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list_employee_reservations(request):
    reservations = EmployeeReservations.objects.all()
    serializer = EmployeeReservationsSerializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
