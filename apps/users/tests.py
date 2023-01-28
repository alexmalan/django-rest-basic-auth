"""
User tests.
"""
# django
from django.conf import settings
from django.urls import reverse
# rest framework
from rest_framework.test import APITestCase

# local api
from apps.users.models import User


class UserManagementTests(APITestCase):
    """
    Test CRUD operations for users
    ( POST {{apiUrl}}/api/user/register/ ) - Create
    ( POST {{apiUrl}}/api/user/login/ ) - Read
    ( GET {{apiUrl}}/api/user/status/ ) - Read
    ( POST {{apiUrl}}/api/user/logout/ ) - Read
    ( DELETE {{apiUrl}}/api/user/remove/ ) - Delete
    ( POST {{apiUrl}}/api/user/deposit/ ) - Update
    ( POST {{apiUrl}}/api/user/reset/ ) - Update
    """

    mock_data = {
        "username": "test@email.com",
        "password": "test1234",
    }

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=getattr(settings, "TOKEN", ""))

    def tearDown(self):
        self.client.logout()

    def test_user_register_success(self):
        """
        User register success.
        """
        url = reverse("user-register")

        response = self.client.post(url, self.mock_data, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertTrue("username" in json_response)
        self.assertTrue("deposit" in json_response)
        self.assertTrue("role" in json_response)

        self.assertEqual(json_response["username"], self.mock_data["username"])
        self.assertEqual(json_response["deposit"], 0)
        self.assertEqual(json_response["role"], "BUYER")

    def test_user_register_invalid_payload(self):
        """
        User register with invalid payload.
        """
        url = reverse("user-register")

        mock_data = {
            "username": "user",
            "password": "test",
        }
        response = self.client.post(url, mock_data, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json_response["message"]["username"][0], "Enter a valid email address."
        )

    def test_user_login_success(self):
        """
        User login success.
        """
        url_register = reverse("user-register")
        url_login = reverse("user-login")

        self.client.post(url_register, self.mock_data, format="json")
        response = self.client.post(url_login, self.mock_data, format="json")

        user = User.objects.filter(username=self.mock_data["username"]).get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["success"],
            f"Welcome {self.mock_data['username']}: {user.role}",
        )

    def test_user_login_invalid_payload(self):
        """
        User login with invalid payload.
        """
        url_register = reverse("user-register")
        url_login = reverse("user-login")

        mock_data_altered = {
            "username": "testing",
            "password": "test1234",
        }
        self.client.post(url_register, self.mock_data, format="json")
        response = self.client.post(url_login, mock_data_altered, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"][0], "Invalid Credentials")

    def test_user_status_success(self):
        """
        User status success.
        """
        url_register = reverse("user-register")
        url_login = reverse("user-login")
        url_status = reverse("user-status")

        self.client.post(url_register, self.mock_data, format="json")
        self.client.post(url_login, self.mock_data, format="json")
        response = self.client.get(url_status, format="json")

        user = User.objects.filter(username=self.mock_data["username"]).get()
        self.assertEqual(
            response.json()["success"], f"Logged in as: {user.username} : {user.role}"
        )

    def test_user_status_invalid_request(self):
        """
        User status without being authenticated.
        """
        url_status = reverse("user-status")

        response = self.client.get(url_status, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            json_response["error"]["message"],
            "Authentication credentials were not provided.",
        )

    def test_user_logout_success(self):
        """
        User logout success.
        """
        url_register = reverse("user-register")
        url_login = reverse("user-login")
        url_logout = reverse("user-logout")

        self.client.post(url_register, self.mock_data, format="json")
        self.client.post(url_login, self.mock_data, format="json")

        response = self.client.post(url_logout, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["success"], "Logged Out Successfully")

    def test_user_logout_invalid_request(self):
        """
        User logout without being authenticated.
        """
        url_logout = reverse("user-logout")

        response = self.client.post(url_logout, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json_response["error"]["message"],
            "Authentication credentials were not provided.",
        )

    def test_user_deposit_success(self):
        """
        User deposit action success.
        """
        url_register = reverse("user-register")
        url_login = reverse("user-login")
        url_deposit = reverse("user-deposit")

        self.client.post(url_register, self.mock_data, format="json")
        self.client.post(url_login, self.mock_data, format="json")

        user = User.objects.filter(username=self.mock_data["username"]).get()
        self.assertEqual(user.deposit, 0)

        deposit_data = {"amount": 100}

        response = self.client.post(url_deposit, deposit_data, format="json")
        json_response = response.json()
        user = User.objects.filter(username=self.mock_data["username"]).get()

        self.assertEqual(user.deposit, deposit_data["amount"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_response["success"],
            f"Deposit successful. Your new balance is {user.deposit}",
        )

    def test_user_deposit_invalid_request(self):
        """
        User deposit action without being authenticated.
        """
        url_deposit = reverse("user-deposit")

        deposit_data = {"amount": 100}
        response = self.client.post(url_deposit, deposit_data, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json_response["error"]["message"],
            "Authentication credentials were not provided.",
        )

    def test_user_reset_deposit_success(self):
        """
        User reset deposit action success.
        """
        url_register = reverse("user-register")
        url_login = reverse("user-login")
        url_deposit = reverse("user-deposit")
        url_reset = reverse("user-reset")

        self.client.post(url_register, self.mock_data, format="json")
        self.client.post(url_login, self.mock_data, format="json")

        user = User.objects.filter(username=self.mock_data["username"]).get()
        self.assertEqual(user.deposit, 0)

        deposit_data = {"amount": 100}

        response = self.client.post(url_deposit, deposit_data, format="json")
        json_response = response.json()
        user = User.objects.filter(username=self.mock_data["username"]).get()
        self.assertEqual(user.deposit, deposit_data["amount"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_response["success"],
            f"Deposit successful. Your new balance is {user.deposit}",
        )

        response = self.client.post(url_reset, format="json")
        json_response = response.json()

        user = User.objects.filter(username=self.mock_data["username"]).get()

        self.assertEqual(user.deposit, 0)
        self.assertEqual(
            json_response["success"],
            f"Deposit reset successful. Your available balance is {user.deposit}",
        )

    def test_user_reset_deposit_invalid_request(self):
        """
        User reset deposit action without being authenticated.
        """
        url_reset = reverse("user-reset")
        response = self.client.post(url_reset, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json_response["error"]["message"],
            "Authentication credentials were not provided.",
        )

    def test_user_delete_success(self):
        """
        User delete success.
        """
        url_register = reverse("user-register")
        url_login = reverse("user-login")
        url_remove = reverse("user-remove")

        self.client.post(url_register, self.mock_data, format="json")
        self.client.post(url_login, self.mock_data, format="json")

        user = User.objects.filter(username=self.mock_data["username"]).get()
        self.assertEqual(user.is_active, True)

        response = self.client.delete(url_remove, format="json")
        json_response = response.json()

        user = User.objects.filter(username=self.mock_data["username"])

        self.assertEqual(len(user), 0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["success"], "User Removed Successfully")

    def test_user_delete_invalid_request(self):
        """
        User delete without being authenticated.
        """
        url_remove = reverse("user-remove")

        response = self.client.delete(url_remove, format="json")
        json_response = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json_response["error"]["message"],
            "Authentication credentials were not provided.",
        )
