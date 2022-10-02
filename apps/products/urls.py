from django.urls import path

from . import views

urlpatterns = [
    path("list/", view=views.ProductListView.as_view()),
    path("create/", view=views.ProductCreateView.as_view()),
    path("<int:product_id>/", view=views.ProductUpdateDeleteView.as_view()),
    path('<int:product_id>/buy/', view=views.ProductBuyView.as_view()),
]
