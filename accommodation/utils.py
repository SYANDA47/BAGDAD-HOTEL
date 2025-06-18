from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import requests
import json

def send_booking_confirmation_email(booking):
    """Send booking confirmation email"""
    subject = f'Booking Confirmation - {booking.room.room_type.name}'
    
    # Render HTML email template
    html_message = render_to_string('accommodation/emails/booking_confirmation.html', {
        'booking': booking,
    })
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.guest_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def send_booking_sms(booking):
    """Send booking confirmation SMS using Africa's Talking API"""
    if not booking.guest_phone:
        return False
    
    # Format phone number (ensure it starts with +254 for Kenya)
    phone = booking.guest_phone
    if phone.startswith('0'):
        phone = '+254' + phone[1:]
    elif not phone.startswith('+'):
        phone = '+254' + phone
    
    message = f"""
Booking Confirmed!
Room: {booking.room.room_number}
Check-in: {booking.check_in_date}
Check-out: {booking.check_out_date}
Total: KSh {booking.total_price}
Guest: {booking.guest_name}
Thank you for choosing us!
    """.strip()
    
    try:
        # Using Africa's Talking API (popular in Kenya)
        url = "https://api.africastalking.com/version1/messaging"
        headers = {
            'apiKey': settings.SMS_API_KEY,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        data = {
            'username': settings.SMS_USERNAME,
            'to': phone,
            'message': message,
            'from': 'HOTEL'  # Your sender ID
        }
        
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 201:
            return True
        else:
            print(f"SMS sending failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"SMS sending failed: {e}")
        return False

def send_booking_whatsapp(booking):
    """Send booking confirmation via WhatsApp using Twilio"""
    try:
        from twilio.rest import Client
        
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        
        # Format phone number
        phone = booking.guest_phone
        if phone.startswith('0'):
            phone = '+254' + phone[1:]
        elif not phone.startswith('+'):
            phone = '+254' + phone
        
        message = f"""
🏨 *Booking Confirmed!*

*Guest:* {booking.guest_name}
*Room:* {booking.room.room_number} - {booking.room.room_type.name}
*Check-in:* {booking.check_in_date}
*Check-out:* {booking.check_out_date}
*Total:* KSh {booking.total_price:,}

Thank you for choosing our hotel! 🙏
        """.strip()
        
        message = client.messages.create(
            body=message,
            from_='whatsapp:+14155238886',  # Twilio WhatsApp number
            to=f'whatsapp:{phone}'
        )
        
        return True
    except Exception as e:
        print(f"WhatsApp sending failed: {e}")
        return False