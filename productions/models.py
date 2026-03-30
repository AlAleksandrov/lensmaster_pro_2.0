from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from common.models import SlugMixin, DescriptionMixin, TimestampedMixin


# Create your models here.
class Category(SlugMixin, DescriptionMixin, models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    cover_image = models.ImageField(
        upload_to='category_covers/',
        blank=True,
        null=True,
        verbose_name='Category image',
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Production(SlugMixin, DescriptionMixin, TimestampedMixin, models.Model):
    title = models.CharField(
        max_length=150,
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='productions',
    )

    date_created = models.DateField(
        default=timezone.now
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    short_description = models.CharField(
        max_length=255,
        blank=True,
        help_text='Short teaser used in listings and cards.',
    )

    cover_image = models.ImageField(
        upload_to='production_covers/',
        blank=True,
        null=True,
        verbose_name='Production image',
    )

    video_url = models.URLField(
        blank=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    equipment = models.ManyToManyField(
        'inventory.Equipment',
        related_name='productions',
        blank=True,
    )

    class Meta:
        ordering = ['-date_created', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
