from math import prod

from django.shortcuts import Http404
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response

from .models import Product
from .permissions import IsOwner, IsSeller
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]
    authentication_classes = [authentication.SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class ProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner, IsSeller]
    authentication_classes = [authentication.SessionAuthentication]

    def get_object(self):
        try:
            product = Product.objects.get(id=self.kwargs.get("product_id")).first()
        except:
            raise Http404("Product not found")
        return product
