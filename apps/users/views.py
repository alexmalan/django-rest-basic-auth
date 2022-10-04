from django.contrib.auth import login, logout
from rest_framework import authentication, generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from common.permissions import IsBuyer, IsOwner, IsSeller

from .models import User
from .serializers import RegisterSerializer
from .services import deposit_amount, reset_amount


# REGISTER
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer


# LOGIN
class UserLoginView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(
            username=request.data.get("username", None),
            password=request.data.get("password", None),
        ).first()
        if user:
            login(request, user)
            return Response(
                {"success": f"Welcome {request.user}: {request.user.role}"},
                status=status.HTTP_200_OK,
            )
        raise ValidationError("Invalid Credentials")


# STATUS
class CheckUserStatusView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_class = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]

    def get(self, request, *args, **kwargs):
        return Response(
            {"success": f"Logged in as: {request.user} : {request.user.role}"},
            status=status.HTTP_200_OK,
        )


# LOGOUT
class UserLogoutView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(
            {"success": "Logged Out Successfully"}, status=status.HTTP_200_OK
        )


# REMOVE
class UserRemoveView(generics.RetrieveUpdateDestroyAPIView):
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
    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
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
    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        response = reset_amount(request.user)

        if response:
            return Response(
                {
                    "success": f"Deposit reset successful. Your available balance is {request.user.deposit}"
                },
                status=status.HTTP_200_OK,
            )
        raise ValidationError("Something went wrong")
