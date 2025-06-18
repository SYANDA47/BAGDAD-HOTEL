from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Room, RoomType, Booking
from .forms import BookingForm

def accommodation_list(request):
    room_types = RoomType.objects.all()
    available_rooms = Room.objects.filter(is_available=True)
    
    context = {
        'room_types': room_types,
        'available_rooms': available_rooms,
    }
    return render(request, 'accommodation/room_list.html', context)

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    context = {'room': room}
    return render(request, 'accommodation/room_detail.html', context)

def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.save()  # The save method will calculate total_price automatically
            
            # Mark room as unavailable
            room.is_available = False
            room.save()
            
            messages.success(request, 'Room booked successfully!')
            return redirect('accommodation:booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'accommodation/book_room.html', context)

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    context = {'booking': booking}
    return render(request, 'accommodation/booking_confirmation.html', context)
