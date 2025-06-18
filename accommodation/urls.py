from django.urls import path
from . import views

app_name = 'accommodation'

urlpatterns = [
    path('', views.accommodation_list, name='room_list'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
]
