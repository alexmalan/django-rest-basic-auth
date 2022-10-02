from .models import Product
from django.shortcuts import Http404

def buy_product(user=None, payload=None):
    """
    Buy product using payload data
    User has to have the role of a BUYER

    :param dict payload: Request data payload
    :param User user: User instance
    """
    if payload is None or not isinstance(payload, dict):
        raise Http404("Invalid input")

    # retrieve the product
    product = Product.objects.filter(id=payload["product_id"]).first()

    if product:
        spending = product.cost * payload["quantity"]

        # check if the amount is enough
        if product.amount < payload["quantity"]:
            raise Http404("The requested quantity exceeds the available quantity.")

        # check if the user has enough money
        if user.deposit < spending:
            raise Http404("Not enough deposit available. Please insert more coins.")

        # update the product amount
        if product.amount == payload["quantity"]:
            product.amount = 0
        else:
            product.amount -= payload["quantity"]

        # update the user deposit
        user.deposit -= spending
        change = user.deposit
        change_list = []

        for i in [100, 50, 20, 10, 5]:
            while change >=i:
                change_list.append(i)
                change -= i
        
        try:
            product.save()
            user.save()
        except Exception:
            raise Http404("Error while saving the product or user")

        return change_list, spending, product
    return False, False, False