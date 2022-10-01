from django.contrib.auth import login, logout
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializer


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
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        user = User.objects.filter(username=username, password=password).first()
        if user is not None:
            login(request, user)
            return Response(
                {"success": f"Welcome {request.user}: {request.user.role}"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


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
