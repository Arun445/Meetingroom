from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (EmployeeReservationsSerializer, MeetingRoomSerializer, ReservationSerializer,
                          EmployeeReservations, UserSerializer, MeetingRoomSerializerWithReservations)
from .models import (MeetingRoom, Reservation,
                     EmployeeReservations)
from rest_framework import status
from django.contrib.auth.hashers import make_password

from .invalid_reservation import delete_invalid_reservations
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_meeting_rooms(request):
    rooms = MeetingRoom.objects.all()
    serializer = MeetingRoomSerializer(rooms, many=True)
    logger.info(f"{request.user.get_full_name()} checks all rooms")
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_meeting_room_with_reservations(request, pk):
    room = MeetingRoom.objects.get(pk=pk)
    reservations = room.reservation_set.all()
    delete_invalid_reservations(reservations)
    serializer = MeetingRoomSerializerWithReservations(
        room, context={'request': request}, many=False)
    logger.info(
        f"{request.user.get_full_name()} checks room {room.name} reservations")
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_meeting_room(request):

    serializer = MeetingRoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(f"{request.user.get_full_name()} created a new room")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.warning(
        f"{request.user.get_full_name()} was not successfull creating a room")
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
            employee = User.objects.get(id=employee)
            EmployeeReservations.objects.create(
                employee=employee, reservation=reservation)

        serializer = ReservationSerializer(reservation, many=False)
        logger.info(
            f"{request.user.get_full_name()} created a new reservation")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        logger.warning(
            f"{request.user.get_full_name()} was not successfull creating a reservation")
        message = {'detail': 'Reservation creation failed'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_reservation(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    if request.user == reservation.employee:
        reservation.delete()
        logger.info(f"{request.user.get_full_name()} canceled a reservation")
        return Response({'detail': 'reservation was succesfully canceled'}, status=status.HTTP_200_OK)
    logger.warning(
        f"{request.user.get_full_name()} was not authorized to cancel ")
    return Response({'detail': 'You are not authorized to cancel this reservation'}, status=status.HTTP_400_BAD_REQUEST)


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
    employee_reservations = employee.employeereservations_set.filter(
        reservation__reserved_to__gte=timezone.now())
    all_employee_reservations = employee.employeereservations_set.all()
    delete_invalid_reservations(all_employee_reservations)
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
        logger.info(
            f'new employee {user.first_name} {user.last_name} was created')
        return Response(serializer.data)
    except:
        message = {'detail': 'Employee with this email already exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
