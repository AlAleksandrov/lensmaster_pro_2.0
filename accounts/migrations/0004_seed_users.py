from django.db import migrations
from django.contrib.auth.hashers import make_password


USERS = [
    # (username, first_name, last_name, email, group_name, phone, city, bio)
    # ── Photographers ────────────────────────────────────────────────────────
    ('alex_lens',    'Alex',    'Petrov',    'alex@lensmaster.pro',   'Photographers', '+359882000001', 'Sofia',
     'Senior photographer with 12 years of experience in weddings and corporate events.'),
    ('maria_photo',  'Maria',   'Ivanova',   'maria@lensmaster.pro',  'Photographers', '+359882000002', 'Plovdiv',
     'Specialising in portrait and fashion photography. Natural light enthusiast.'),
    ('ivan_shoot',   'Ivan',    'Georgiev',  'ivan@lensmaster.pro',   'Photographers', '+359882000003', 'Varna',
     'Drone and aerial photographer. Licensed UAV pilot. Available for commercial shoots.'),

    # ── Clients ──────────────────────────────────────────────────────────────
    ('sofia_bride',   'Sofia',   'Nikolova',  'sofia@mail.com',        'Clients', '+359881000001', 'Sofia',
     'Planning my dream wedding — looking for the perfect photographer.'),
    ('peter_corp',    'Peter',   'Stoyanov',  'peter@corp.com',        'Clients', '+359881000002', 'Plovdiv',
     'Corporate client. Need regular product and event photography.'),
    ('elena_events',  'Elena',   'Dimitrova', 'elena@events.com',      'Clients', '+359881000003', 'Varna',
     'Event organiser. Work with photographers on a regular basis.'),
    ('georgi_client', 'Georgi',  'Hristov',   'georgi@mail.com',       'Clients', '+359881000004', 'Burgas',
     'Looking for aerial shots of our new building complex.'),
    ('anna_wedding',  'Anna',    'Todorova',  'anna@mail.com',         'Clients', '+359881000005', 'Sofia',
     'Bride-to-be. Interested in full-day wedding coverage.'),
    ('nikola_biz',    'Nikola',  'Angelov',   'nikola@biz.com',        'Clients', '+359881000006', 'Stara Zagora',
     'Business owner. Need branding and product photos for our online store.'),
    ('diana_art',     'Diana',   'Marinova',  'diana@art.com',         'Clients', '+359881000007', 'Sofia',
     'Artist and creative. Looking for expressive portrait sessions.'),
]

FAVOURITES = {
    'sofia_bride':   {'packages': ['Wedding photography', 'Wedding Premium']},
    'peter_corp':    {'packages': ['Corporate events', 'Real estate Interior']},
    'elena_events':  {'packages': ['Corporate events', 'Birthday']},
    'georgi_client': {'packages': ['Drone photography & videography']},
    'anna_wedding':  {'packages': ['Wedding photography', 'Wedding Premium', 'Family session']},
    'nikola_biz':    {'packages': ['Real estate Interior', 'Corporate events']},
    'diana_art':     {'packages': ['Family session', 'Birthday']},
    'alex_lens':     {'packages': ['Highlight film (3\u20135 min)', 'Wedding Premium']},
    'maria_photo':   {'packages': ['Family session', 'Wedding photography']},
    'ivan_shoot':    {'packages': ['Drone photography & videography', 'Highlight film (3\u20135 min)']},
}


def forwards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Profile = apps.get_model('accounts', 'Profile')
    ServicePackage = apps.get_model('bookings', 'ServicePackage')
    Production = apps.get_model('productions', 'Production')
    Equipment = apps.get_model('inventory', 'Equipment')

    hashed_pw = make_password('Test1234!')

    for (username, first, last, email, group_name, phone, city, bio) in USERS:
        u, created = User.objects.get_or_create(
            username=username,
            defaults=dict(
                first_name=first,
                last_name=last,
                email=email,
                password=hashed_pw,
                is_active=True,
            )
        )
        if not created and not u.password.startswith('pbkdf2'):
            u.password = hashed_pw
            u.save()

        try:
            grp = Group.objects.get(name=group_name)
            u.groups.add(grp)
        except Group.DoesNotExist:
            pass

        profile, _ = Profile.objects.get_or_create(user=u)
        if not profile.phone:
            profile.phone = phone
        if not profile.city:
            profile.city = city
        if not profile.bio:
            profile.bio = bio
        profile.save()

    # ── Фаворити: пакети ─────────────────────────────────────────────────────
    packages_map = {p.name: p for p in ServicePackage.objects.all()}

    for username, favs in FAVOURITES.items():
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            continue
        for pkg_name in favs.get('packages', []):
            pkg = packages_map.get(pkg_name)
            if pkg:
                profile.favorite_packages.add(pkg)

    # ── Фаворити: продукции ──────────────────────────────────────────────────
    productions = list(Production.objects.all())
    if productions:
        prod_assignments = {
            'sofia_bride':   productions[:2],
            'anna_wedding':  productions[:3],
            'peter_corp':    productions[2:5],
            'elena_events':  productions[1:4],
            'georgi_client': productions[3:6],
            'nikola_biz':    productions[2:6],
            'diana_art':     productions[1:5],
            'alex_lens':     productions[:5],
            'maria_photo':   productions[1:6],
            'ivan_shoot':    productions[3:],
        }
        for username, prod_list in prod_assignments.items():
            try:
                profile = Profile.objects.get(user__username=username)
                for prod in prod_list:
                    profile.favorite_productions.add(prod)
            except Profile.DoesNotExist:
                continue

    # ── Фаворити: оборудване ─────────────────────────────────────────────────
    all_equipment = list(Equipment.objects.all())
    if all_equipment:
        eq_assignments = {
            'sofia_bride':   all_equipment[:2],
            'peter_corp':    all_equipment[1:3],
            'elena_events':  all_equipment[2:4],
            'georgi_client': all_equipment[3:5] if len(all_equipment) > 4 else all_equipment[-2:],
            'anna_wedding':  all_equipment[:3],
            'nikola_biz':    all_equipment[2:5] if len(all_equipment) > 4 else all_equipment[-3:],
            'diana_art':     all_equipment[1:4],
            'alex_lens':     all_equipment[:4],
            'maria_photo':   all_equipment[1:5] if len(all_equipment) > 4 else all_equipment[1:],
            'ivan_shoot':    all_equipment[3:] if len(all_equipment) > 3 else all_equipment[-2:],
        }
        for username, eq_list in eq_assignments.items():
            try:
                profile = Profile.objects.get(user__username=username)
                for eq in eq_list:
                    profile.favorite_equipment.add(eq)
            except Profile.DoesNotExist:
                continue


def backwards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    usernames = [u[0] for u in USERS]
    User.objects.filter(username__in=usernames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_options_profile_favorite_equipment_and_more'),
        ('accounts', '0002_create_groups'),
        ('bookings', '0006_bookingrequest_user_alter_bookingrequest_city_and_more'),
        ('inventory', '0004_equipment_cover_image'),
        ('productions', '0006_alter_category_cover_image_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
