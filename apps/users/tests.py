# django
from django.conf import settings
from django.urls import reverse
from rest_framework import status

# rest framework
from rest_framework.test import APITestCase

# local api
from apps.users.models import User


class UserManagementTests(APITestCase):
    """
    Test CRUD operations for users
    ( GET {{apiUrl}}/api/product/list/ ) - List
    ( GET {{apiUrl}}/api/product/{product_id} ) - Read
    ( PUT {{apiUrl}}/api/product/{product_id} ) - Update
    ( DELETE {{apiUrl}}/api/product/{product_id} ) - Delete
    ( POST {{apiUrl}}/api/product/create/ ) - Create

    @required: settings.TOKEN - use a access / id TOKEN
    @required: valid product_id on setUp function
    """

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=getattr(settings, "TOKEN", ""))

    def tearDown(self):
        self.client.logout()

    def test_user_register(self):
        """
        Ensure we can get products list.
        """
        breakpoint()

    #     url = reverse('product_list')

    #     response = self.client.get(url, format='json')
    #     self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])

    #     if response.status_code != status.HTTP_401_UNAUTHORIZED:
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertTrue(isinstance(response.data, list))

    #         if len(response.data) > 0:
    #             first_item = response.data[0]
    #             self.assertTrue('id' in first_item)
    #             self.assertTrue('uuid' in first_item)
    #             self.assertTrue('name' in first_item)
    #             self.assertTrue('type' in first_item)
    #             self.assertTrue('price' in first_item)
    #     else:
    #         print('UNAUTHORIZED')

    # def test_product_details(self):
    #     """
    #     Ensure product details are returned correctly.
    #     """

    #     url = reverse('product_details', kwargs={'product_id': self.product_id})

    #     response = self.client.get(url, format='json')
    #     self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])

    #     if response.status_code != status.HTTP_401_UNAUTHORIZED:
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertTrue(isinstance(response.data, dict))

    #         product = response.data
    #         self.assertTrue('id' in product)
    #         self.assertTrue('uuid' in product)
    #         self.assertTrue('name' in product)
    #         self.assertTrue('type' in product)
    #         self.assertTrue('price' in product)
    #         self.assertTrue('status' in product)
    #         self.assertTrue('created_by' in product)
    #         self.assertTrue('updated_by' in product)
    #         self.assertTrue('created_at' in product)
    #         self.assertTrue('updated_at' in product)
    #     else:
    #         print('UNAUTHORIZED')

    # def test_create_product(self):
    #     """
    #     Ensure product can be created.
    #     """

    #     url = reverse('product_create')
    #     mock_data = {
    #         'name': 'test',
    #         'type': 'SP',
    #         'price': 500,
    #     }

    #     response = self.client.post(url, mock_data, format='json')
    #     self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_401_UNAUTHORIZED])

    #     if response.status_code != status.HTTP_401_UNAUTHORIZED:
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         product = response.data
    #         self.assertEqual(mock_data['name'], str(product['name']))
    #         self.assertEqual(mock_data['type'], str(product['type']))
    #         self.assertEqual(float(mock_data['price']), float(product['price']))
    #     else:
    #         print('UNAUTHORIZED')
