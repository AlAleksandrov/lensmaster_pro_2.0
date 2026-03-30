from django.db import migrations

CATEGORY_SEED = [
    {
        "slug": "wedding-photography",
        "name": "Wedding photography",
        "description": "Elegant wedding storytelling — preparations, ceremony, portraits, and reception.",
        "cover_image": "category_covers/wedding_ceremony_2.png",
    },
    {
        "slug": "family-photography",
        "name": "Family photography",
        "description": "Warm, candid family sessions — outdoors or at home.",
        "cover_image": "category_covers/family_photography.png",
    },
    {
        "slug": "personal-events",
        "name": "Personal events",
        "description": "Birthdays, baptisms, proms, and private celebrations.",
        "cover_image": "category_covers/personal_events.png",
    },
    {
        "slug": "corporate-events",
        "name": "Corporate events",
        "description": "Conference coverage, brand activations, product launches, and team events.",
        "cover_image": "category_covers/corporate_event_1.png",
    },
    {
        "slug": "drone-photography-videography",
        "name": "Drone photography & videography",
        "description": "Aerial perspectives for venues, resorts, landscapes and events.",
        "cover_image": "category_covers/drone_photography.JPG",
    },
    {
        "slug": "videography",
        "name": "Videography",
        "description": "Short films, highlight reels and event videos with clean audio and cinematic motion.",
        "cover_image": "category_covers/videography.png",
    },
    {
        "slug": "maternity-photography",
        "name": "Maternity photography",
        "description": "Emotional maternity sessions capturing the beauty of pregnancy.",
        "cover_image": "category_covers/maternity.png",
    },
    {
        "slug": "real-estate-photography",
        "name": "Real estate photography",
        "description": "Professional architectural and interior photography for real estate listings.",
        "cover_image": "category_covers/real_estate.png",
    },
    {
        "slug": "commercial-product-photography",
        "name": "Commercial product photography",
        "description": "Clean, high-end product photography for brands and e-commerce.",
        "cover_image": "category_covers/commercial.png",
    },
    {
        "slug": "creative-portraits",
        "name": "Creative portraits",
        "description": "Editorial and personal branding portrait sessions.",
        "cover_image": "category_covers/creative_portraits.png",
    },
]


def forwards(apps, schema_editor):
    category = apps.get_model("productions", "Category")
    for row in CATEGORY_SEED:
        category.objects.update_or_create(
            slug=row["slug"],
            defaults={
                "name": row["name"],
                "description": row["description"],
                "cover_image": row["cover_image"],
            },
        )


def backwards(apps, schema_editor):
    category = apps.get_model("productions", "Category")
    slugs = [c["slug"] for c in CATEGORY_SEED]
    category.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("productions", "0003_production_equipment"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]