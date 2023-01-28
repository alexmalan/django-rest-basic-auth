"""
Product tests.
"""
# django
from django.conf import settings
from django.urls import reverse
# rest framework
from rest_framework.test import APITestCase

from apps.products.models import Product
# local api
from apps.users.models import User


class ProductsManagementTests(APITestCase):
    """
    Test CRUD operations for users
    ( GET {{apiUrl}}/api/product/list/ ) - List
    ( POST {{apiUrl}}/api/product/create/ ) - Create
    ( PUT {{apiUrl}}/api/product/<int:product_id>/ ) - Update
    ( DELETE {{apiUrl}}/api/product/<int:product_id>/ ) - Delete
    ( POST {{apiUrl}}/api/product/<int:product_id>/buy/ ) - Update
    """

    user1_seller = {
        "id": 1,
        "username": "test1@email.com",
        "password": "test1234",
        "role": "SELLER",
    }

    user2_seller = {
        "id": 2,
        "username": "test2@email.com",
        "password": "test1234",
        "role": "SELLER",
    }

    user3_buyer = {
        "id": 3,
        "username": "test3@email.com",
        "password": "test1234",
        "role": "BUYER",
        "deposit": 100,
    }

    product_1 = {
        "id": 100,
        "name": "Product 1",
        "amount": 10,
        "cost": 10,
    }

    product_2 = {
        "id": 101,
        "name": "Product 2",
        "amount": 20,
        "cost": 20,
    }

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=getattr(settings, "TOKEN", ""))
        self.client.post(reverse("user-register"), self.user1_seller, format="json")
        self.client.post(reverse("user-register"), self.user2_seller, format="json")
        self.client.post(reverse("user-register"), self.user3_buyer, format="json")

    def tearDown(self):
        self.client.logout()

    def test_product_list_success(self):
        """
        Product list success.
        """
        user_login = reverse("user-login")
        product_create = reverse("product-create")
        product_list = reverse("product-list")
        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")
        self.client.post(product_create, self.product_2, format="json")

        response = self.client.get(product_list, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        product_1 = response.json()[0]
        product_2 = response.json()[0]
        user = User.objects.get(username=self.user1_seller["username"])

        self.assertTrue(product_1["name"], self.product_1["name"])
        self.assertTrue(product_1["cost"], self.product_1["cost"])
        self.assertTrue(product_1["amount"], self.product_1["amount"])
        self.assertTrue(product_1["id"], user.id)

        self.assertTrue(product_2["name"], self.product_2["name"])
        self.assertTrue(product_2["cost"], self.product_2["cost"])
        self.assertTrue(product_2["amount"], self.product_2["amount"])
        self.assertTrue(product_2["id"], user.id)

        self.assertTrue(user.role, self.user1_seller["role"])

    def test_product_create_success(self):
        """
        Product create success.
        """
        user_login = reverse("user-login")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user1_seller, format="json")

        response = self.client.post(product_create, self.product_1, format="json")
        product_1 = response.json()
        user = User.objects.get(username=self.user1_seller["username"])

        self.assertEqual(response.status_code, 201)
        self.assertTrue(product_1["name"], self.product_1["name"])
        self.assertTrue(product_1["cost"], self.product_1["cost"])
        self.assertTrue(product_1["amount"], self.product_1["amount"])
        self.assertTrue(product_1["id"], user.id)

        self.assertTrue(user.role, self.user1_seller["role"])

    def test_product_create_invalid_payload(self):
        """
        Product create invalid payload.
        """
        user_login = reverse("user-login")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user1_seller, format="json")

        product_altered = {"name": "Product 1", "quantitie": 29}
        response = self.client.post(product_create, product_altered, format="json")
        user = User.objects.get(username=self.user1_seller["username"])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["message"]["amount"][0], "This field is required."
        )

        self.assertTrue(user.role, self.user1_seller["role"])

    def test_product_create_invalid_user_role(self):
        """
        Product create invalid user role.
        """
        user_login = reverse("user-login")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user3_buyer, format="json")
        response = self.client.post(product_create, self.product_1, format="json")

        user = User.objects.get(username=self.user3_buyer["username"])

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["error"]["message"],
            "You do not have permission to perform this action.",
        )

        self.assertTrue(user.role, self.user3_buyer["role"])

    def test_product_update_success(self):
        """
        Product update success.
        """
        user_login = reverse("user-login")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")

        product_payload = {
            "name": "Product updated",
            "amount": 300,
            "cost": 300,
        }
        product_id = Product.objects.get(name=self.product_1["name"]).id
        product_update = reverse(
            "product-update-delete", kwargs={"product_id": product_id}
        )
        response = self.client.put(product_update, product_payload, format="json")
        json_response = response.json()
        user = User.objects.get(username=self.user1_seller["username"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["name"], product_payload["name"])
        self.assertEqual(json_response["cost"], product_payload["cost"])
        self.assertEqual(json_response["amount"], product_payload["amount"])
        self.assertEqual(json_response["user"], user.id)

        self.assertTrue(user.role, self.user1_seller["role"])

    def test_product_update_invalid_product_id(self):
        """
        Product update invalid product id.
        """
        user_login = reverse("user-login")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")

        product_payload = {
            "name": "Product updated",
            "amount": 300,
            "cost": 300,
        }
        product_id = (
            Product.objects.filter(name=self.product_1["name"]).first().id + 123
        )
        product_update = reverse(
            "product-update-delete", kwargs={"product_id": product_id}
        )
        response = self.client.put(product_update, product_payload, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"][0], "Product not found")

    def test_product_update_invalid_user_owner(self):
        """
        Product update invalid owner.
        """
        user_login = reverse("user-login")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user3_buyer, format="json")
        self.client.post(product_create, self.product_1, format="json")

        product_payload = {
            "name": "Product updated",
            "amount": 300,
            "cost": 300,
        }
        product_update = reverse("product-update-delete", kwargs={"product_id": 1})
        response = self.client.put(product_update, product_payload, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json_response["error"]["message"],
            "You do not have permission to perform this action.",
        )

    def test_product_update_invalid_user_role(self):
        """
        Product update invalid user role.
        """
        user_login = reverse("user-login")
        user_logout = reverse("user-logout")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")
        self.client.post(user_logout, format="json")

        product_payload = {
            "name": "Product updated",
            "amount": 300,
            "cost": 300,
        }

        product_id = Product.objects.get(name=self.product_1["name"]).id
        self.client.post(user_login, self.user2_seller, format="json")
        product_update = reverse(
            "product-update-delete", kwargs={"product_id": product_id}
        )
        response = self.client.put(product_update, product_payload, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json_response["error"]["message"],
            "You do not have permission to perform this action.",
        )

    def test_product_delete_success(self):
        """
        Product delete success.
        """
        user_login = reverse("user-login")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")

        product_id = Product.objects.get(name=self.product_1["name"]).id
        product_delete = reverse(
            "product-update-delete", kwargs={"product_id": product_id}
        )
        response = self.client.delete(product_delete, format="json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data["message"], "Product deleted successfully")

    def test_product_delete_invalid_product_id(self):
        """
        Product delete invalid product id.
        """
        user_login = reverse("user-login")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")

        product_id = Product.objects.get(name=self.product_1["name"]).id
        product_delete = reverse(
            "product-update-delete", kwargs={"product_id": product_id + 112}
        )
        response = self.client.delete(product_delete, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"][0], "Product not found")

    def test_product_delete_invalid_user_role(self):
        """
        Product delete invalid user role.
        """
        user_login = reverse("user-login")
        user_logout = reverse("user-logout")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")
        self.client.post(user_logout, format="json")
        self.client.post(user_login, self.user3_buyer, format="json")

        product_id = Product.objects.get(name=self.product_1["name"]).id
        product_delete = reverse(
            "product-update-delete", kwargs={"product_id": product_id}
        )
        response = self.client.delete(product_delete, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["error"]["message"],
            "You do not have permission to perform this action.",
        )

    def test_product_delete_invalid_user_owner(self):
        """
        Product delete invalid owner.
        """
        user_login = reverse("user-login")
        user_logout = reverse("user-logout")
        product_create = reverse("product-create")

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")
        self.client.post(user_logout, format="json")
        self.client.post(user_login, self.user2_seller, format="json")

        product_id = Product.objects.get(name=self.product_1["name"]).id
        product_delete = reverse(
            "product-update-delete", kwargs={"product_id": product_id}
        )
        response = self.client.delete(product_delete, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["error"]["message"],
            "You do not have permission to perform this action.",
        )

    def test_product_buy_success(self):
        """
        Product buy success.
        """
        user_login = reverse("user-login")
        user_logout = reverse("user-logout")
        product_create = reverse("product-create")
        buy_payload = {"quantity": 1}

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")
        self.client.post(user_logout, self.product_1, format="json")
        self.client.post(user_login, self.user3_buyer, format="json")

        product_id = Product.objects.get(name=self.product_1["name"]).id
        product_buy = reverse("product-buy", kwargs={"product_id": product_id})
        response = self.client.post(product_buy, buy_payload, format="json")
        json_response = response.json()["response"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["product"]["name"], "Product 1")
        self.assertEqual(
            json_response["product"]["amount"], self.product_1["amount"] - 1
        )
        self.assertEqual(json_response["product"]["cost"], self.product_1["cost"])
        self.assertEqual(json_response["product"]["id"], product_id)
        self.assertEqual(
            sum(json_response["change"]),
            self.user3_buyer["deposit"] - self.product_1["cost"],
        )
        self.assertEqual(
            json_response["spending"], self.product_1["cost"] * buy_payload["quantity"]
        )

    def test_product_buy_invalid_payload(self):
        """
        Product buy invalid payload.
        """
        user_login = reverse("user-login")
        user_logout = reverse("user-logout")
        product_create = reverse("product-create")

        buy_payload = {"quantity": "asasas"}

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")
        self.client.post(user_logout, self.product_1, format="json")
        self.client.post(user_login, self.user3_buyer, format="json")

        product_id = Product.objects.get(name=self.product_1["name"]).id
        product_buy = reverse("product-buy", kwargs={"product_id": product_id})
        response = self.client.post(product_buy, buy_payload, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"][0], "Invalid input.")

    def test_product_buy_invalid_user_role(self):
        """
        Product buy invalid user role.
        """
        product_id = 1
        user_login = reverse("user-login")
        user_logout = reverse("user-logout")
        product_create = reverse("product-create")

        buy_payload = {"quantity": 1}

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")
        self.client.post(user_logout, self.product_1, format="json")
        self.client.post(user_login, self.user2_seller, format="json")

        product_id = Product.objects.get(name=self.product_1["name"]).id
        product_buy = reverse("product-buy", kwargs={"product_id": product_id})
        response = self.client.post(product_buy, buy_payload, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json_response["error"]["message"],
            "You do not have permission to perform this action.",
        )

    def test_product_buy_quantity_not_available(self):
        """
        Product buy quantity not available.
        """
        user_login = reverse("user-login")
        user_logout = reverse("user-logout")
        product_create = reverse("product-create")

        buy_payload = {"quantity": 102021}

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")
        self.client.post(user_logout, self.product_1, format="json")
        self.client.post(user_login, self.user3_buyer, format="json")

        product_id = Product.objects.get(name=self.product_1["name"]).id
        product_buy = reverse("product-buy", kwargs={"product_id": product_id})
        response = self.client.post(product_buy, buy_payload, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json_response["message"][0],
            "The requested quantity exceeds the available quantity.",
        )

    def test_product_buy_low_deposit(self):
        """
        Product buy low deposit.
        """
        product_id = 1
        user_login = reverse("user-login")
        user_reset = reverse("user-reset")
        user_logout = reverse("user-logout")
        product_create = reverse("product-create")

        buy_payload = {"quantity": 1}

        self.client.post(user_login, self.user1_seller, format="json")
        self.client.post(product_create, self.product_1, format="json")
        self.client.post(user_logout, self.product_1, format="json")
        self.client.post(user_login, self.user3_buyer, format="json")
        self.client.post(user_reset, format="json")

        product_id = Product.objects.get(name=self.product_1["name"]).id
        product_buy = reverse("product-buy", kwargs={"product_id": product_id})
        response = self.client.post(product_buy, buy_payload, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json_response["message"][0],
            "Not enough deposit available. Please insert more coins.",
        )
