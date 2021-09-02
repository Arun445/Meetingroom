
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register/', views.createEmployee),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('room/<str:pk>', views.list_meeting_room_reservations),
    path('rooms/', views.list_meeting_rooms),
    path('rooms/create/', views.create_meeting_room),
    path('reservations/', views.list_reservations),
    path('reservations/<str:pk>', views.list_reservation),
    path('reservations/create/', views.create_reservation),
    path('reservations/delete/<str:pk>', views.cancel_reservation),
    path('users/', views.list_employee_reservations),
    path('users/get/', views.getUser),
]
