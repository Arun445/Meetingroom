
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('room/<str:pk>', views.list_meeting_room),
    path('rooms/', views.list_meeting_rooms),
    path('rooms/create/', views.create_meeting_room),
    path('reservations/', views.list_reservations),
    path('reservations/create/', views.create_reservation),
    path('reservations/delete/<str:pk>', views.cancel_reservation),
    path('users/', views.list_employee_reservations),
]
