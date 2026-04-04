from django.db.models.signals import pre_save
from django.dispatch import receiver
from bookings.models import BookingRequest
from django_q.tasks import async_task


@receiver(pre_save, sender=BookingRequest)
def handle_booking_request_save(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = BookingRequest.objects.get(pk=instance.pk)
    except BookingRequest.DoesNotExist:
        return

    status_changed_to_confirmed = (
        old_instance.status != BookingRequest.Status.CONFIRMED
        and instance.status == BookingRequest.Status.CONFIRMED
    )
    if status_changed_to_confirmed:
        async_task(
            'bookings.tasks.send_booking_confirmation',
            booking_id=instance.pk,
        )