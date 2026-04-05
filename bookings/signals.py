from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from bookings.models import BookingRequest
from django_q.tasks import async_task
from django.conf import settings
from bookings.tasks import send_booking_confirmation_celery


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

    if not status_changed_to_confirmed:
        return

    def enqueue_task():
        if getattr(settings, "ASYNC_TASK_BACKEND", "celery") == "celery":
            send_booking_confirmation_celery.delay(instance.pk)
        else:
            async_task(
                "bookings.tasks.send_booking_confirmation",
                booking_id=instance.pk,
            )

    transaction.on_commit(enqueue_task)