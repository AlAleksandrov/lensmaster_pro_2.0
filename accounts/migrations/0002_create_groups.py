from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # --- Photographers group ---
    photographers, _ = Group.objects.get_or_create(name='Photographers')
    photographer_codenames = [
        # productions
        'add_production', 'change_production', 'delete_production', 'view_production',
        'add_category', 'change_category', 'delete_category', 'view_category',
        # inventory
        'add_equipment', 'change_equipment', 'delete_equipment', 'view_equipment',
        # bookings
        'add_service_package', 'change_service_package', 'delete_service_package', 'view_service_package',
        'add_booking_request', 'change_booking_request', 'delete_booking_request', 'view_booking_request',
    ]
    photographer_perms = Permission.objects.filter(codename__in=photographer_codenames)
    photographers.permissions.set(photographer_perms)

    # --- Clients group ---
    clients, _ = Group.objects.get_or_create(name='Clients')
    client_codenames = [
        'add_booking_request', 'view_booking_request',
        'view_production',
        'view_category',
        'view_service_package',
        'view_equipment',
    ]
    client_perms = Permission.objects.filter(codename__in=client_codenames)
    clients.permissions.set(client_perms)


def delete_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Photographers', 'Clients']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('productions', '0006_alter_category_cover_image_and_more'),
        ('bookings', '0006_bookingrequest_user_alter_bookingrequest_city_and_more'),
        ('inventory', '0004_equipment_cover_image'),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]