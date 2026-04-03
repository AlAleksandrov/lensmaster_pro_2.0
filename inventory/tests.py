from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from .models import Equipment

User = get_user_model()


class InventoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='photographer', password='pass123')
        group, _ = Group.objects.get_or_create(name='Photographers')
        self.user.groups.add(group)

        self.item = Equipment.objects.create(
            brand="Sony",
            model="A7 IV",
            equipment_type=Equipment.EquipmentType.CAMERA,
            is_active=True,
        )

    def test_equipment_str(self):
        self.assertEqual(str(self.item), "Sony A7 IV (Camera)")

    def test_equipment_creation(self):
        self.assertEqual(self.item.brand, "Sony")
        self.assertEqual(self.item.equipment_type, "camera")

    def test_internal_id_auto_generated(self):
        self.assertTrue(self.item.internal_id.startswith("INV-"))
        self.assertEqual(len(self.item.internal_id), 12)

    def test_equipment_list_view(self):
        response = self.client.get(reverse('inventory:equipment_list'))
        self.assertEqual(response.status_code, 200)

    def test_equipment_detail_view(self):
        response = self.client.get(
            reverse('inventory:equipment_detail', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_equipment_create_requires_login(self):
        response = self.client.get(reverse('inventory:equipment_create'))
        self.assertEqual(response.status_code, 302)

    def test_equipment_create_authenticated(self):
        self.client.login(username='photographer', password='pass123')
        response = self.client.get(reverse('inventory:equipment_create'))
        self.assertEqual(response.status_code, 200)

    def test_equipment_update_requires_login(self):
        response = self.client.get(
            reverse('inventory:equipment_edit', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_equipment_delete_requires_login(self):
        response = self.client.get(
            reverse('inventory:equipment_delete', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(response.status_code, 302)