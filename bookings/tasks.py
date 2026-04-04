from django.core.mail import send_mail
from bookings.models import BookingRequest
from lensmaster_pro.settings import DEFAULT_FROM_EMAIL


def send_booking_confirmation(booking_id):
    try:
        booking = BookingRequest.objects.select_related('package').get(pk=booking_id)
    except BookingRequest.DoesNotExist:
        return

    subject = 'Booking Confirmed! - LensMaster Pro'
    message = (
        f'Dear {booking.full_name},\n\n'
        f'Great news! Your booking request (ID: #{booking_id}) has been CONFIRMED.\n'
        f'We are looking forward to seeing you soon!\n\n'
        f'Thank you for choosing LensMaster Pro for your photography needs!\n'
        f'Best regards,\n'
        f'The LensMaster Pro Team'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[booking.email],
        fail_silently=False,
    )