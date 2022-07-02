from unicodedata import category
from django.shortcuts import render, get_object_or_404

from .models import Product

from cart.forms import CartAddProductForm

def product_list(request, category_id=None):
    products = Product.objects.filter(is_available=True)
    if category_id:
        products = products.filter(category=category_id)

    context = {
        'products' : products
    }
    return render(request, "products/list.html", context=context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_product_form = CartAddProductForm()
    context = {
        'product':product,
        'cart_product_form' : cart_product_form
    }
    return render(request, template_name="products/detail.html", context=context)
    