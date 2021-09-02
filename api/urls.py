
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/', views.list_employees),
    path('users/register/', views.createEmployee),
    path('users/<str:pk>/', views.list_employee_reservations),
    path('rooms/', views.list_meeting_rooms),
    path('rooms/create/', views.create_meeting_room),
    path('rooms/<str:pk>/', views.list_meeting_room_with_reservations),
    path('reservations/create/', views.create_reservation),
    path('reservations/delete/<str:pk>/', views.cancel_reservation),

]
