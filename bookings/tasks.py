from django.core.mail import send_mail

from lensmaster_pro.settings import DEFAULT_FROM_EMAIL


def send_booking_confirmed_email(booking_id,email, full_name):
    subject = 'Booking Confirmed! - LensMaster Pro'
    message = (
        f'Dear {full_name},\n\n'
        f'Great news! Your booking request (ID: #{booking_id}) has been CONFIRMED.\n'
        f'We are looking forward to seeing you soon!\n\n'
        f'Thank you for choosing LensMaster Pro for your photography needs!\n'
        f'Best regards,\n'
        f'The LensMaster Pro Team'
    )
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)