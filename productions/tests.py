from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Category, Production

User = get_user_model()


class PortfolioTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='photographer', password='pass123')
        from django.contrib.auth.models import Group
        group, _ = Group.objects.get_or_create(name='Photographers')
        self.user.groups.add(group)

        self.category = Category.objects.create(name="Weddings")
        self.production = Production.objects.create(
            title="John & Jane Wedding",
            category=self.category,
            is_featured=True,
            slug="john-jane-wedding",
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Weddings")

    def test_production_str(self):
        self.assertEqual(str(self.production), "John & Jane Wedding")

    def test_production_slug_auto(self):
        prod = Production.objects.create(
            title="Auto Slug Test",
            category=self.category,
        )
        self.assertEqual(prod.slug, "auto-slug-test")

    def test_category_list_view(self):
        response = self.client.get(reverse('productions:category_list'))
        self.assertEqual(response.status_code, 200)

    def test_production_detail_view(self):
        response = self.client.get(
            reverse('productions:production_detail', kwargs={'slug': self.production.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_category_create_requires_login(self):
        response = self.client.get(reverse('productions:category_create'))
        self.assertEqual(response.status_code, 302)

    def test_category_create_authenticated(self):
        self.client.login(username='photographer', password='pass123')
        response = self.client.get(reverse('productions:category_create'))
        self.assertEqual(response.status_code, 200)

    def test_category_edit_requires_login(self):
        # URL ползва slug, не pk!
        response = self.client.get(
            reverse('productions:category_edit', kwargs={'slug': self.category.slug})
        )
        self.assertEqual(response.status_code, 302)

    def test_category_delete_requires_login(self):
        # URL ползва slug, не pk!
        response = self.client.get(
            reverse('productions:category_delete', kwargs={'slug': self.category.slug})
        )
        self.assertEqual(response.status_code, 302)