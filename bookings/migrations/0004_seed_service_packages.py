from django.db import migrations
from decimal import Decimal

PACKAGE_SEED = [
    {
        "name": "Birthday",
        "category_slug": "personal-events",
        "description": "Some pictures in good vibes",
        "price": Decimal("200.00"),
        "duration_hours": 2,
        "max_photos_included": 70,
        "is_active": True,
    },
    {
        "name": "Drone photography & videography",
        "category_slug": "drone-photography-videography",
        "description": "Drone photography & videography",
        "price": Decimal("350.00"),
        "duration_hours": 1,
        "max_photos_included": 40,
        "is_active": True,
    },
    {
        "name": "Wedding photography",
        "category_slug": "wedding-photography",
        "description": "Your happy day",
        "price": Decimal("750.00"),
        "duration_hours": 8,
        "max_photos_included": 400,
        "is_active": True,
    },
    {
        "name": "Wedding Premium",
        "category_slug": "wedding-photography",
        "description": "Extended coverage for bigger weddings.",
        "price": Decimal("950.00"),
        "duration_hours": 10,
        "max_photos_included": 550,
        "is_active": True,
    },
    {
        "name": "Family session",
        "category_slug": "family-photography",
        "description": "Relaxed family session ideal for golden hour.",
        "price": Decimal("220.00"),
        "duration_hours": 2,
        "max_photos_included": 80,
        "is_active": True,
    },
    {
        "name": "Corporate events",
        "category_slug": "corporate-events",
        "description": "Conference and corporate coverage.",
        "price": Decimal("550.00"),
        "duration_hours": 6,
        "max_photos_included": 220,
        "is_active": True,
    },
    {
        "name": "Highlight film (3–5 min)",
        "category_slug": "videography",
        "description": "Cinematic highlight film with clean audio.",
        "price": Decimal("700.00"),
        "duration_hours": 2,
        "max_photos_included": 30,
        "is_active": True,
    },
    {
        "name": "Real estate Interior",
        "category_slug": "real-estate-photography",
        "description": "Interior architectural photography with wide-angle compositions.",
        "price": Decimal("260.00"),
        "duration_hours": 2,
        "max_photos_included": 35,
        "is_active": True,
    },
]

def forwards(apps, schema_editor):
    category = apps.get_model("productions", "Category")
    service_package = apps.get_model("bookings", "ServicePackage")

    categories = {c.slug: c for c in category.objects.all()}

    for row in PACKAGE_SEED:
        category = categories.get(row["category_slug"])
        if category is None:
            raise ValueError(f"Missing category with slug={row['category_slug']}")

        service_package.objects.update_or_create(
            name=row["name"],
            category_id=category.id,
            defaults={
                "description": row["description"],
                "price": row["price"],
                "duration_hours": row["duration_hours"],
                "max_photos_included": row["max_photos_included"],
                "is_active": row["is_active"],
            },
        )

def backwards(apps, schema_editor):
    service_package = apps.get_model("bookings", "ServicePackage")
    names = [p["name"] for p in PACKAGE_SEED]
    service_package.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0003_servicepackage_category"),
        ("productions", "0004_seed_categories"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]