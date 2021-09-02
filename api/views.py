from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import EmployeeReservationsSerializer, MeetingRoomSerializer, ReservationSerializer, EmployeeReservations, UserSerializer
from .models import (MeetingRoom, Reservation,
                     EmployeeReservations)
from rest_framework import serializers, status
from django.contrib.auth.hashers import make_password
from datetime import datetime


@api_view(['GET'])
def list_meeting_rooms(request):
    rooms = MeetingRoom.objects.all()
    serializer = MeetingRoomSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_meeting_room_reservations(request, pk):
    room = MeetingRoom.objects.get(pk=pk)
    reservations = room.reservation_set.all()
    for i in reservations:
        if i.ended_reservation():
            i.delete()
    serializer = MeetingRoomSerializer(room, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_meeting_room_reservations_by_employee(request, pk):
    room = MeetingRoom.objects.get(pk=pk)
    reservations = room.reservation_set.all()

    serializer = MeetingRoomSerializer(room, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_meeting_room(request):

    serializer = MeetingRoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    message = {'detail': 'Employee with this email already exist'}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_reservations(request):
    reservations = Reservation.objects.all()
    for reservation in reservations:
        if reservation.is_reservation_ended_():
            reservation.delete()
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_reservation(request, pk):
    reservations = Reservation.objects.get()
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    data = request.data
    print(request)

    try:
        room = MeetingRoom.objects.get(id=data['room'])
        reservation = Reservation.objects.create(title=data['title'], reserved_from=data['reserved_from'],
                                                 reserved_to=data['reserved_to'], employee=request.user,
                                                 room=room)

        for employee in data['employees']:
            employeer = User.objects.get(id=employee)
            EmployeeReservations.objects.create(
                employee=employeer, reservation=reservation)

        serializer = ReservationSerializer(reservation, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        message = {'detail': 'Reservation creation failed'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def createEmployee(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['first_name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Employee with this email already exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
