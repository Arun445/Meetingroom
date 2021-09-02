from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import (EmployeeReservationsSerializer, MeetingRoomSerializer, ReservationSerializer,
                          EmployeeReservations, UserSerializer, MeetingRoomSerializerWithReservations)
from .models import (MeetingRoom, Reservation,
                     EmployeeReservations)
from rest_framework import serializers, status
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .invalid_reservation import delete_invalid_reservations


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_meeting_rooms(request):
    rooms = MeetingRoom.objects.all()
    serializer = MeetingRoomSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_meeting_room_with_reservations(request, pk):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    room = MeetingRoom.objects.get(pk=pk)
    reservations = room.reservation_set.filter(
        employee__first_name__icontains=query)

    delete_invalid_reservations(reservations)

    serializer = MeetingRoomSerializerWithReservations(room, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_meeting_room(request):

    serializer = MeetingRoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    message = {'detail': 'There was a problem creating this meeting room'}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    data = request.data
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
@permission_classes([IsAuthenticated])
def cancel_reservation(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    reservation.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_employees(request):

    employees = User.objects.all()
    serializer = UserSerializer(employees, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_employee_reservations(request, pk):
    employee = User.objects.get(pk=pk)
    employee_reservations = employee.employeereservations_set.all()
    delete_invalid_reservations(employee_reservations)
    serializer = EmployeeReservationsSerializer(
        employee_reservations, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def createEmployee(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializer(user, many=False)
        print(dir(serializer))
        return Response(serializer.data)
    except:
        message = {'detail': 'Employee with this email already exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
