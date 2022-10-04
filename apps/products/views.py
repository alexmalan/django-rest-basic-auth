from math import prod

from rest_framework import authentication, generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from common.permissions import IsBuyer, IsOwner, IsSeller

from .models import Product
from .serializers import ProductSerializer
from .services import buy_product


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
    permission_classes = [permissions.IsAuthenticated, IsSeller, IsOwner]
    authentication_classes = [authentication.SessionAuthentication]

    def get_object(self):
        try:
            product = Product.objects.get(id=self.kwargs.get("product_id"))
        except:
            raise ValidationError("Product not found")
        return product

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductBuyView(generics.GenericAPIView):
    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        if not request.data:
            raise ValidationError("Invalid payload")

        if self.kwargs["product_id"]:
            request.data["product_id"] = self.kwargs["product_id"]
        else:
            raise ValidationError("No product provided")

        change_list, spending, product = buy_product(request.user, request.data)

        if product:
            report = {
                "change": change_list,
                "spending": spending,
                "product": ProductSerializer(product).data,
            }

            return Response({"response": report}, status=status.HTTP_200_OK)
        raise ValidationError("Product not found")
