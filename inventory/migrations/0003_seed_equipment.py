from django.db import migrations
from datetime import date

EQUIPMENT_SEED = [
    {
        "internal_id": "INV-D3410E41",
        "brand": "Sony",
        "model": "A7 IV",
        "equipment_type": "camera",
        "specifications": "Full-frame mirrorless camera — primary workhorse for weddings and portraits.",
        "purchase_date": date(2022, 3, 15),
        "notes": "",
    },
    {
        "internal_id": "INV-BDAB7871",
        "brand": "Sony",
        "model": "35mm f1.4GM",
        "equipment_type": "lens",
        "specifications": "Fast wide prime for environmental portraits and low-light.",
        "purchase_date": date(2021, 9, 2),
        "notes": "",
    },
    {
        "internal_id": "INV-FD2362EF",
        "brand": "Sony",
        "model": "85mm f1.4GM",
        "equipment_type": "lens",
        "specifications": "Short tele prime for portraits with creamy bokeh.",
        "purchase_date": date(2020, 5, 12),
        "notes": "",
    },
    {
        "internal_id": "INV-25951949",
        "brand": "Godox",
        "model": "V1S",
        "equipment_type": "lighting",
        "specifications": "Round-head on-camera flash for flattering light; TTL-capable.",
        "purchase_date": date(2019, 11, 20),
        "notes": "",
    },
    {
        "internal_id": "INV-487A7435",
        "brand": "DJI",
        "model": "mini 2",
        "equipment_type": "drone",
        "specifications": "Compact drone used for quick aerial establishing shots.",
        "purchase_date": date(2019, 2, 7),
        "notes": "",
    },
    {
        "internal_id": "INV-B029B494",
        "brand": "Sony",
        "model": "A7 IV",
        "equipment_type": "camera",
        "specifications": "Secondary full-frame mirrorless body for multi-camera coverage.",
        "purchase_date": date(2022, 4, 10),
        "notes": "",
    },
    {
        "internal_id": "INV-1C77B0AA",
        "brand": "DJI",
        "model": "Mavic 3",
        "equipment_type": "drone",
        "specifications": "Professional drone for aerial photography and smooth cinematic shots.",
        "purchase_date": date(2022, 6, 1),
        "notes": "",
    },
    {
        "internal_id": "INV-9A12C0F1",
        "brand": "Zhiyun",
        "model": "Crane 3",
        "equipment_type": "other",
        "specifications": "3-axis gimbal for smooth video movement and highlight films.",
        "purchase_date": date(2020, 8, 9),
        "notes": "",
    },
    {
        "internal_id": "INV-73F1B9D2",
        "brand": "Godox",
        "model": "AD200",
        "equipment_type": "lighting",
        "specifications": "Compact strobe for fast-paced events and off-camera flash setups.",
        "purchase_date": date(2018, 12, 5),
        "notes": "",
    },
    {
        "internal_id": "INV-PLACEHOLDER-010",
        "brand": "Generic",
        "model": "Accessory Placeholder",
        "equipment_type": "other",
        "specifications": "Placeholder accessory entry for future equipment.",
        "purchase_date": date(2023, 1, 1),
        "notes": "Placeholder",
    },
]


def forwards(apps, schema_editor):
    equipment = apps.get_model("inventory", "Equipment")

    field_names = {f.name for f in equipment._meta.get_fields() if hasattr(f, "name")}

    for row in EQUIPMENT_SEED:
        if "internal_id" in field_names and row.get("internal_id"):
            lookup = {"internal_id": row["internal_id"]}
        elif "brand" in field_names and "model" in field_names:
            lookup = {"brand": row["brand"], "model": row["model"]}
        else:
            lookup = {"specifications": row.get("specifications", "")}

        defaults = {}
        for key in ["brand", "model", "equipment_type", "specifications", "purchase_date", "notes", "internal_id"]:
            if key in field_names and key in row:
                defaults[key] = row[key]

        equipment.objects.update_or_create(defaults=defaults, **lookup)


def backwards(apps, schema_editor):
    equipment = apps.get_model("inventory", "Equipment")

    field_names = {f.name for f in equipment._meta.get_fields() if hasattr(f, "name")}

    internal_ids = [r["internal_id"] for r in EQUIPMENT_SEED if r.get("internal_id")]
    if "internal_id" in field_names and internal_ids:
        equipment.objects.filter(internal_id__in=internal_ids).delete()
    else:
        from django.db import models
        pairs = [(r["brand"], r["model"]) for r in EQUIPMENT_SEED if r.get("brand") and r.get("model")]
        if pairs:
            q = models.Q()
            for b, m in pairs:
                q |= models.Q(brand=b, model=m)
            equipment.objects.filter(q).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0002_remove_equipment_productions"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]