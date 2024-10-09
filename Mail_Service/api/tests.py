from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User

from services.models import Field


class FieldTest(APITestCase):

    url = reverse('fields')

    def setUp(self):
        """Создаем пользователя"""

        self.client = APIClient()
        self.client.login(username='adminuser', password='adminpassword')
        self.admin = User.objects.create_superuser(username='adminuser', password='adminpassword')
        self.field = Field.objects.create(
            field_name='Email',
            field_type='EMAIL'
        )

    def test_status_ok(self):
        """Логиним админа, и проверяем статус код"""

        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_field_data(self):
        """Логиним не стафф-юзера, и проверяем статус код"""

        request = self.client.get(self.url)
        self.assertEqual(request.data[0].get('field_name'), 'Email')
        self.assertEqual(request.data[0].get('field_type'), 'EMAIL')