from django.db import migrations
from datetime import date

PRODUCTION_SEED = [
    {
        "slug": "alina-petar",
        "title": "Alina & Petar",
        "category_slug": "wedding-photography",
        "date_created": date(2025, 6, 7),
        "location": "Sofia",
        "short_description": "A classic Sofia wedding with elegant portraits.",
        "description": "Full-day wedding coverage — preparations, ceremony, couple portraits, and reception highlights.",
        "cover_image": "production_covers/wedding_ceremony_1.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-D3410E41", "INV-B029B494", "INV-BDAB7871", "INV-FD2362EF", "INV-25951949"],
    },
    {
        "slug": "evelin-valentin",
        "title": "Evelin & Valentin",
        "category_slug": "wedding-photography",
        "date_created": date(2025, 6, 6),
        "location": "Paris",
        "short_description": "Paris city romance with editorial-style portraits.",
        "description": "A destination wedding story with soft tones and editorial approach.",
        "cover_image": "production_covers/wedding_ceremony_4.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-D3410E41", "INV-BDAB7871", "INV-FD2362EF", "INV-25951949"],
    },
    {
        "slug": "autumn-family-session",
        "title": "Autumn family session",
        "category_slug": "family-photography",
        "date_created": date(2025, 9, 19),
        "location": "Plovdiv",
        "short_description": "Golden hour family session with warm autumn colors.",
        "description": "Outdoor family session in autumn light focusing on real interactions and laughter.",
        "cover_image": "production_covers/autumn_family_session.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-B029B494", "INV-FD2362EF", "INV-BDAB7871"],
    },
    {
        "slug": "the-baptism-of-elina",
        "title": "The baptism of Elina",
        "category_slug": "personal-events",
        "date_created": date(2025, 7, 11),
        "location": "Sofia",
        "short_description": "A tender family celebration with ceremony details.",
        "description": "Baptism coverage with focus on family and tradition; gentle documentary coverage and portraits.",
        "cover_image": "production_covers/baptism.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-D3410E41", "INV-FD2362EF", "INV-25951949", "INV-1C77B0AA"],
    },
    {
        "slug": "annas-birthday",
        "title": "Anna's birthday",
        "category_slug": "personal-events",
        "date_created": date(2026, 2, 21),
        "location": "Sofia",
        "short_description": "A lively birthday party with flash bounce and dance-floor energy.",
        "description": "Birthday party coverage — guests, decorations, cake moment and dance highlights.",
        "cover_image": "production_covers/birthday.png",
        "video_url": "",
        "is_featured": False,
        "equipment_internal_ids": ["INV-B029B494", "INV-FD2362EF", "INV-25951949"],
    },
    {
        "slug": "ivailas-prom",
        "title": "Ivaila's prom",
        "category_slug": "personal-events",
        "date_created": date(2025, 5, 24),
        "location": "Varna",
        "short_description": "Prom portraits with a cinematic look and styling details.",
        "description": "Prom portrait session — editorial portraits and candid family moments.",
        "cover_image": "production_covers/prom.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-D3410E41", "INV-FD2362EF", "INV-25951949"],
    },
    {
        "slug": "patyka",
        "title": "Patyka — product launch",
        "category_slug": "corporate-events",
        "date_created": date(2025, 10, 17),
        "location": "Sofia",
        "short_description": "Corporate product launch coverage with brand visuals.",
        "description": "Event coverage for a product launch — venue details, speakers, and guest interactions.",
        "cover_image": "production_covers/corporate_event_2.png",
        "video_url": "",
        "is_featured": False,
        "equipment_internal_ids": ["INV-D3410E41", "INV-BDAB7871", "INV-73F1B9D2", "INV-1C77B0AA"],
    },
    {
        "slug": "drone-videography",
        "title": "Drone videography",
        "category_slug": "drone-photography-videography",
        "date_created": date(2026, 2, 21),
        "location": "Elin Pelin",
        "short_description": "Aerial establishing shots over countryside landscapes.",
        "description": "Drone session focused on landscape movement and smooth transitions for reels.",
        "cover_image": "production_covers/drone_photography.JPG",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-487A7435", "INV-1C77B0AA"],
    },
    {
        "slug": "city-lights-highlight-film",
        "title": "City lights — highlight film",
        "category_slug": "videography",
        "date_created": date(2025, 12, 15),
        "location": "Sofia",
        "short_description": "Short cinematic highlight film with clean audio.",
        "description": "Short highlight film project combining handheld, gimbal and drone shots.",
        "cover_image": "production_covers/videography.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-D3410E41", "INV-9A12C0F1", "INV-1C77B0AA"],
    },
    {
        "slug": "engagement-session-plovdiv",
        "title": "Engagement session — Plovdiv",
        "category_slug": "wedding-photography",
        "date_created": date(2025, 8, 14),
        "location": "Plovdiv",
        "short_description": "Relaxed pre-wedding session at a vineyard.",
        "description": "Engagement session in the Plovdiv wine region with golden light and relaxed poses.",
        "cover_image": "production_covers/engagement_session.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-D3410E41", "INV-FD2362EF", "INV-BDAB7871"],
    },
    {
        "slug": "newborn-session-sofia",
        "title": "Newborn session — Sofia",
        "category_slug": "personal-events",
        "date_created": date(2025, 11, 3),
        "location": "Sofia",
        "short_description": "Tender studio newborn session with soft light.",
        "description": "Newborn session with macro details, wrapped poses, and family portraits.",
        "cover_image": "production_covers/newborn_session.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-B029B494", "INV-FD2362EF", "INV-73F1B9D2"],
    },
{
        "slug": "golden-hour-maternity",
        "title": "Golden Hour Maternity",
        "category_slug": "maternity-photography",
        "date_created": date(2025, 9, 15),
        "location": "Plovdiv",
        "short_description": "Emotional maternity session in a sunlit meadow.",
        "description": "A sunset maternity session focusing on natural movement and the beauty of motherhood.",
        "cover_image": "production_covers/maternity_session.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-D3410E41", "INV-FD2362EF"],
    },
    {
        "slug": "modern-loft-interior",
        "title": "Modern Loft Interior",
        "category_slug": "real-estate-photography",
        "date_created": date(2025, 11, 10),
        "location": "Sofia",
        "short_description": "Architectural photography for a luxury city loft.",
        "description": "Clean lines and natural light photography for high-end real estate marketing.",
        "cover_image": "production_covers/real_estate.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-D3410E41", "INV-BDAB7871"],
    },
    {
        "slug": "skincare-brand-campaign",
        "title": "Skincare Brand Campaign",
        "category_slug": "commercial-product-photography",
        "date_created": date(2025, 12, 5),
        "location": "Studio",
        "short_description": "Minimalist product photography for a premium skincare line.",
        "description": "Studio lighting and creative styling for commercial advertising.",
        "cover_image": "production_covers/commercial.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-B029B494", "INV-73F1B9D2"],
    },
    {
        "slug": "urban-creative-portraits",
        "title": "Urban Creative Portraits",
        "category_slug": "creative-portraits",
        "date_created": date(2025, 8, 20),
        "location": "Sofia",
        "short_description": "Cinematic street portraits with a moody editorial feel.",
        "description": "A creative session exploring urban textures and dramatic lighting.",
        "cover_image": "production_covers/creative_portraits.png",
        "video_url": "",
        "is_featured": True,
        "equipment_internal_ids": ["INV-D3410E41", "INV-FD2362EF"],
    },
]

def forwards(apps, schema_editor):
    category = apps.get_model("productions", "Category")
    production = apps.get_model("productions", "Production")
    equipment = apps.get_model("inventory", "Equipment")

    categories = {c.slug: c for c in category.objects.all()}
    equipment_by_internal = {e.internal_id: e for e in equipment.objects.all()}

    for row in PRODUCTION_SEED:
        category = categories.get(row["category_slug"])
        if category is None:
            raise ValueError(f"Missing category with slug={row['category_slug']}")

        prod, _ = production.objects.update_or_create(
            slug=row["slug"],
            defaults={
                "title": row["title"],
                "category_id": category.id,
                "date_created": row["date_created"],
                "location": row["location"],
                "short_description": row["short_description"],
                "description": row["description"],
                "cover_image": row["cover_image"],
                "video_url": row["video_url"],
                "is_featured": row["is_featured"],
            },
        )

        equip_objs = []
        for internal_id in row.get("equipment_internal_ids", []):
            e = equipment_by_internal.get(internal_id)
            if e is None:
                raise ValueError(f"Missing equipment with internal_id={internal_id} (required by production {row['slug']})")
            equip_objs.append(e)
        prod.equipment.set(equip_objs)


def backwards(apps, schema_editor):
    production = apps.get_model("productions", "Production")
    slugs = [p["slug"] for p in PRODUCTION_SEED]
    production.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("productions", "0004_seed_categories"),
        ("inventory", "0003_seed_equipment"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]