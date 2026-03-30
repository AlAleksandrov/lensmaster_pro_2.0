from django.db import migrations
from datetime import date

BOOKING_SEED = [
    {
        "first_name": "Alina",
        "last_name": "Georgieva",
        "email": "alina.georgieva@example.com",
        "phone": "08787908324",
        "city": "Plovdiv",
        "event_date": date(2026, 2, 28),
        "package_name": "Wedding photography",
        "message": "Hi! We’re looking for full-day wedding coverage. Can we schedule a call this week?",
        "heard_from": "instagram",
        "status": "pending",
        "internal_notes": "Requested a meeting; propose 2 time slots and send pricing PDF.",
    },
    {
        "first_name": "Dimitar",
        "last_name": "Nikolov",
        "email": "d.nikolov@example.com",
        "phone": "08787908329",
        "city": "Varna",
        "event_date": date(2026, 3, 21),
        "package_name": "Corporate events",
        "message": "We need photo coverage for a small conference + speaker portraits.",
        "heard_from": "google",
        "status": "pending",
        "internal_notes": "Ask for agenda and brand guidelines.",
    },
    {
        "first_name": "Ivan",
        "last_name": "Petrov",
        "email": "ivan.petrov@example.com",
        "phone": "08787654321",
        "city": "Lovech",
        "event_date": date(2026, 5, 30),
        "package_name": "Real estate Interior",
        "message": "Interior architectural photography with wide-angle compositions.",
        "heard_from": "friend",
        "status": "pending",
        "internal_notes": "Architectural and interior photography for real estate listings.",
    },
    {
        "first_name": "Ivana",
        "last_name": "Petrova",
        "email": "ivana.petrova@example.com",
        "phone": "08787908327",
        "city": "Lom",
        "event_date": date(2026, 5, 24),
        "package_name": "Birthday",
        "message": "Small indoor birthday party, about 20 guests.",
        "heard_from": "other",
        "status": "confirmed",
        "internal_notes": "Confirmed. Ask for address, parking and timeline.",
    },
    {
        "first_name": "Stavri",
        "last_name": "Karapetrov",
        "email": "stavri.karapetrov@example.com",
        "phone": "08787908524",
        "city": "Elin Pelin",
        "event_date": date(2026, 3, 28),
        "package_name": "Drone photography & videography",
        "message": "We want drone flyover shots of a countryside venue for a short promo reel.",
        "heard_from": "google",
        "status": "pending",
        "internal_notes": "Confirm permissions/weather window; suggest 2-hour slot.",
    },
]

def forwards(apps, schema_editor):
    booking_request = apps.get_model("bookings", "BookingRequest")
    service_package = apps.get_model("bookings", "ServicePackage")

    packages = {p.name: p for p in service_package.objects.all()}

    for row in BOOKING_SEED:
        package = packages.get(row["package_name"])
        if package is None:
            raise ValueError(f"Missing ServicePackage with name={row['package_name']}")

        booking_request.objects.update_or_create(
            email=row["email"],
            event_date=row["event_date"],
            defaults={
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "phone": row["phone"],
                "city": row["city"],
                "package_id": package.id,
                "message": row["message"],
                "heard_from": row["heard_from"],
                "status": row["status"],
                "internal_notes": row["internal_notes"],
            },
        )

def backwards(apps, schema_editor):
    booking_request = apps.get_model("bookings", "BookingRequest")
    emails = [b["email"] for b in BOOKING_SEED]
    booking_request.objects.filter(email__in=emails).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0004_seed_service_packages"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]