"""
User views.
"""
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from rest_framework import authentication, generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from common.permissions import IsBuyer

from .models import User
from .serializers import RegisterSerializer
from .services import deposit_amount, reset_amount


# REGISTER
class UserRegisterView(generics.CreateAPIView):
    """
    User registration.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer


# LOGIN
class UserLoginView(generics.RetrieveAPIView):
    """
    User login.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        Login user.

        ```
        :param Request request: client request with authorization in header
        :return: Empty response with status 200
        :raise: Validation error with status 400

        ```
        """
        user = User.objects.filter(
            username=request.data.get("username"),
        ).first()

        if user and check_password(request.data.get("password"), user.password):
            login(request, user)
            return Response(
                {"success": f"Welcome {request.user}: {request.user.role}"},
                status=status.HTTP_200_OK,
            )
        raise ValidationError("Invalid Credentials")


# STATUS
class CheckUserStatusView(generics.RetrieveAPIView):
    """
    Check user status.

    * Requires session authentication.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_class = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]

    def get(self, request, *args, **kwargs):
        """
        Retrieve user status.

        ```
        :param Request request: client request with authorization in header
        :return: Response with status 200
        ```
        """
        return Response(
            {"success": f"Logged in as: {request.user} : {request.user.role}"},
            status=status.HTTP_200_OK,
        )


# LOGOUT
class UserLogoutView(generics.RetrieveAPIView):
    """
    Logout user.

    * Requires session authentication.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request):
        """
        Logout user.

        ```
        :param Request request: client request with authorization in header
        :return: Response with status 200
        ```
        """
        logout(request)
        return Response(
            {"success": "Logged Out Successfully"}, status=status.HTTP_200_OK
        )


# REMOVE
class UserRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """
    Remove user.

    * Requires session authentication.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(
            {"success": "User Removed Successfully"}, status=status.HTTP_200_OK
        )


class UserDepositView(generics.GenericAPIView):
    """
    Deposit amount in user account.

    * Requires session authentication.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request):
        """
        User deposit.

        ```
        :param Request request: client request with authorization in header
        :return: Response with status 200
        :raise: Validation error with status 400
        ```
        """
        if request.data is None or not request.data["amount"]:
            raise ValidationError("Invalid input")

        response = deposit_amount(request.user, request.data["amount"])

        if response:
            return Response(
                {
                    "success": f"Deposit successful. Your new balance is {request.user.deposit}"
                },
                status=status.HTTP_200_OK,
            )


class UserResetView(generics.GenericAPIView):
    """
    Reset user deposit amount.

    * Requires session authentication.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request):
        """
        Reset user deposit.

        ```
        :param Request request: client request with authorization in header
        :return: Response with status 200
        :raise: Validation error with status 400
        ```
        """
        response = reset_amount(request.user)

        if response:
            return Response(
                {
                    "success": f"Deposit reset successful. Your available balance is {request.user.deposit}"
                },
                status=status.HTTP_200_OK,
            )
        raise ValidationError("Something went wrong")
