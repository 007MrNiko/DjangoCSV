from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from main.models import Schemas, SchemasColumn, DataSets


class DjangoCSV(TestCase):
    def setUp(self):
        client = Client()
        user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com"
        )
        user.set_password("tester123")
        user.save()

        schema = Schemas.objects.create(
            user=user,
            name="Schema1"
        )
        schema.save()

        column = SchemasColumn.objects.create(
            schema = schema,
            name="Column1",
            order=0
        )

        column.save()

    def test_database_user(self):
        user = User.objects.get(username="Tester")
        self.assertEqual(user.email, "tester@gmail.com")

    def test_database_schema(self):
        user = User.objects.get(username="Tester")
        schema = Schemas.objects.get(name="Schema1")
        self.assertEqual(schema.user.username, user.username)

    def test_login_logout_page(self):
        user = User.objects.get(email="tester@gmail.com")
        self.client.login(username=user.username, password="tester123")

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/home.html")

        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertURLEqual(response.url, "/login/")
