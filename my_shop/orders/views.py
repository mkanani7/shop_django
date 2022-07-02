from http.client import HTTPResponse
from itertools import product
from django.shortcuts import render

from cart.cart import Cart
from .forms import OrderForm
from .models import OrderItem
from .tasks import order_created

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import weasyprint
from django.conf import settings

from .models import Order


def order_create(request):
    cart = Cart(request)
    if(request.method == 'POST'):
        print("POST")
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         quantity=item['quantity'],
                                         price=item['price'])
            cart.clear()
            print("before task")
            order_created.delay(order.id)
            print("after task")
        return render(request, "orders/order/created.html", {"order": order})
    else:
        print("GET")
        form = OrderForm()

    context = {
        'form': form,
        'cart': cart
    }
    return render(request, "orders/order/create.html", context=context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HTTPResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"filename=order_{order_id}.pdf"
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
