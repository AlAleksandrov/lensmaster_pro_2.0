from django.db import models
from common.models import DescriptionMixin, ActiveStatusMixin, TimestampedMixin


# Create your models here.
class ServicePackage(DescriptionMixin, ActiveStatusMixin, models.Model):
    name = models.CharField(
        max_length=120,
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    duration_hours = models.PositiveIntegerField(
        default=8,
        help_text='Typical coverage duration in hours.',
    )

    max_photos_included = models.PositiveIntegerField(
        default=200,
        help_text='Approximate number of edited photos included.',
    )

    category = models.ForeignKey(
        'productions.Category',
        on_delete=models.CASCADE,
        related_name='packages',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f'{self.name} - €{self.price} per {self.duration_hours} hours'


class BookingRequest(TimestampedMixin, models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    class Source(models.TextChoices):
        FACEBOOK = 'facebook', 'Facebook'
        INSTAGRAM = 'instagram', 'Instagram'
        GOOGLE = 'google', 'Google search'
        FRIEND = 'friend', 'Friend referral'
        OTHER = 'other', 'Other'

    first_name = models.CharField(
        max_length=50,
    )

    last_name = models.CharField(
        max_length=50,
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    event_date = models.DateField()

    package = models.ForeignKey(
        'ServicePackage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
    )

    message = models.TextField(
        blank=True,
    )

    heard_from = models.CharField(
        max_length=20,
        choices=Source,
        default=Source.OTHER,
        help_text='Where did you hear about us?',
    )

    status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.PENDING,
    )

    internal_notes = models.TextField(
        blank=True,
        help_text='Internal notes visible only in the admin area.',
    )

    class Meta:
        ordering = ['-created_at']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} - {self.event_date} ({self.get_status_display()})'
