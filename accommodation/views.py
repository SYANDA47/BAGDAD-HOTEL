from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Room, RoomType, Booking
from .forms import BookingForm

def send_booking_email(booking):
    """Send booking confirmation email"""
    subject = f'Booking Confirmation - Room {booking.room.room_number}'
    
    message = f"""
Dear {booking.guest_name},

Your booking has been confirmed!

Booking Details:
- Room: {booking.room.room_number} - {booking.room.room_type.name}
- Check-in: {booking.check_in_date}
- Check-out: {booking.check_out_date}
- Guests: {booking.guests_count}
- Total Price: KSh {booking.total_price}

Special Requests: {booking.special_requests or 'None'}

Please arrive at the hotel by 2:00 PM on your check-in date.
Check-out time is 11:00 AM.
Don't forget to bring a valid ID for verification.

Thank you for choosing our hotel!

Best regards,
Hotel Management Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.guest_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False

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
    
    # Send confirmation email
    email_sent = send_booking_email(booking)
    
    if email_sent:
        messages.success(request, f'Confirmation email sent to {booking.guest_email}')
    else:
        messages.error(request, 'Booking confirmed but email could not be sent')
    
    context = {
        'booking': booking,
        'email_sent': email_sent
    }
    return render(request, 'accommodation/booking_confirmation.html', context)