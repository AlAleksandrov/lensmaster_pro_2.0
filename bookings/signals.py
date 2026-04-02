import threading
from django.db.models.signals import pre_save
from django.dispatch import receiver
from bookings.models import BookingRequest
from bookings.tasks import send_booking_confirmed_email


@receiver(pre_save, sender=BookingRequest)
def handle_booking_request_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = BookingRequest.objects.get(pk=instance.pk)
            if old_instance.status != BookingRequest.Status.CONFIRMED and instance.status == BookingRequest.Status.CONFIRMED:
                thread = threading.Thread(
                    target=send_booking_confirmed_email,
                    args=(
                        instance.id,
                        instance.email,
                        instance.full_name
                    )
                )
                thread.daemon = True
                thread.start()

        except BookingRequest.DoesNotExist:
            pass