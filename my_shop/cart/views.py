from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from products.models import Product
from .forms import CartAddProductForm

@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    product = get_object_or_404(Product, id=product_id)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, cd["quantity"])
    
    return redirect("cart:cart_detail")
    
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
        'quantity': item['quantity'],
        'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})