from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
import os

from .models import Category, FoodItem, Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm
from .whatsapp import send_pdf_to_whatsapp
from .pdf_utils import generate_order_bill_pdf


# ============================================================
# HOME
# ============================================================

def home(request):

    categories = Category.objects.prefetch_related(
        Prefetch(
            'items',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    return render(
        request,
        'shop/home.html',
        {
            'categories': categories,
            'show_sticky_cart': True,
        }
    )


# ============================================================
# ADD TO CART
# ============================================================

@require_POST
def add_to_cart(request, item_id):

    food_item = get_object_or_404(
        FoodItem,
        id=item_id,
        is_available=True
    )

    size = request.POST.get(
        'size',
        'FULL'
    ).upper()

    try:
        quantity = int(
            request.POST.get(
                'quantity',
                1
            )
        )
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, quantity)

    if size == 'HALF' and not food_item.has_half_option():
        size = 'FULL'

    cart = Cart(request)

    cart.add(
        food_item,
        size,
        quantity
    )

    messages.success(
        request,
        f"Added {food_item.name} ({size.title()}) to your cart."
    )

    next_url = request.POST.get('next') or 'home'

    return redirect(next_url)


# ============================================================
# VIEW CART
# ============================================================

def view_cart(request):

    cart = Cart(request)

    grand_total = (
        cart.total_price()
        + settings.SERVICE_CHARGE
    )

    return render(
        request,
        'shop/cart.html',
        {
            'cart': cart,
            'grand_total': grand_total,
            'show_sticky_cart': False,
        }
    )


# ============================================================
# UPDATE CART ITEM
# ============================================================

@require_POST
def update_cart_item(request, key):

    cart = Cart(request)

    try:
        quantity = int(
            request.POST.get(
                'quantity',
                1
            )
        )
    except (TypeError, ValueError):
        quantity = 1

    cart.update(
        key,
        quantity
    )

    return redirect('view_cart')


# ============================================================
# REMOVE FROM CART
# ============================================================

def remove_from_cart(request, key):

    cart = Cart(request)

    cart.remove(key)

    messages.info(
        request,
        "Item removed from cart."
    )

    return redirect('view_cart')


# ============================================================
# CHECKOUT
# ============================================================

def checkout(request):

    cart = Cart(request)

    if cart.is_empty():

        messages.warning(
            request,
            "Your cart is empty. Add some items first!"
        )

        return redirect('home')


    # --------------------------------------------------------
    # POST
    # --------------------------------------------------------

    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        if form.is_valid():

            # Create order
            order = form.save(
                commit=False
            )

            order.save()


            # ------------------------------------------------
            # CREATE ORDER ITEMS
            # ------------------------------------------------

            for cart_item in cart:

                OrderItem.objects.create(
                    order=order,
                    food_item_id=cart_item['item_id'],
                    item_name=cart_item['name'],
                    size=cart_item['size'],
                    price=cart_item['price'],
                    quantity=cart_item['quantity'],
                )


            # ------------------------------------------------
            # RECALCULATE TOTAL
            # ------------------------------------------------

            order.recalculate_total()


            # ------------------------------------------------
            # CLEAR CART
            # ------------------------------------------------

            cart.clear()


            # ------------------------------------------------
            # GENERATE PDF BILL
            # ------------------------------------------------

            generate_order_bill_pdf(order)


            # ------------------------------------------------
            # REDIRECT TO SUCCESS PAGE
            # ------------------------------------------------

            return redirect(
                'order_success',
                order_id=order.id
            )


    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    else:

        form = CheckoutForm()


    grand_total = (
        cart.total_price()
        + settings.SERVICE_CHARGE
    )

    return render(
        request,
        'shop/checkout.html',
        {
            'form': form,
            'cart': cart,
            'grand_total': grand_total,
            'show_sticky_cart': False,
        }
    )


# ============================================================
# SEND BILL PDF TO CUSTOMER WHATSAPP
# ============================================================

def send_bill_whatsapp(request, order_id):

    # --------------------------------------------------------
    # GET ORDER
    # --------------------------------------------------------

    order = get_object_or_404(
        Order,
        id=order_id
    )


    # --------------------------------------------------------
    # PDF LOCATION
    # --------------------------------------------------------

    filename = (
        f"order_{order.id}_bill.pdf"
    )

    pdf_path = os.path.join(
        settings.MEDIA_ROOT,
        "bills",
        filename
    )


    # --------------------------------------------------------
    # CHECK PDF EXISTS
    # --------------------------------------------------------

    if not os.path.exists(pdf_path):

        print(
            "PDF NOT FOUND:"
        )

        print(
            pdf_path
        )

        return redirect(
            "order_success",
            order_id=order.id
        )


    # --------------------------------------------------------
    # CUSTOMER PHONE
    # --------------------------------------------------------

    phone = order.phone_number


    # --------------------------------------------------------
    # WHATSAPP CAPTION
    # --------------------------------------------------------

    caption = (
        f"Thank you for your order!\n"
        f"Order #{order.id}\n"
        f"Fresh Made To Order"
    )


    # --------------------------------------------------------
    # SEND PDF
    # --------------------------------------------------------

    success = send_pdf_to_whatsapp(
        phone_number=phone,
        pdf_path=pdf_path,
        filename=filename,
        caption=caption,
    )


    if success:

        print(
            "PDF sent successfully!"
        )

    else:

        print(
            "Failed to send PDF"
        )


    # --------------------------------------------------------
    # RETURN TO ORDER SUCCESS
    # --------------------------------------------------------

    return redirect(
        "order_success",
        order_id=order.id
    )


# ============================================================
# ORDER SUCCESS
# ============================================================

def order_success(request, order_id):

    # --------------------------------------------------------
    # GET ORDER
    # --------------------------------------------------------

    order = get_object_or_404(
        Order,
        id=order_id
    )


    # --------------------------------------------------------
    # BILL URL
    # --------------------------------------------------------

    bill_url = None

    if order.bill_pdf:

        bill_url = request.build_absolute_uri(
            order.bill_pdf.url
        )


    # --------------------------------------------------------
    # RENDER PAGE
    # --------------------------------------------------------

    return render(
        request,
        'shop/order_success.html',
        {
            'order': order,
            'bill_url': bill_url,

            # IMPORTANT:
            # Shop WhatsApp number
            'OWNER_WHATSAPP_NUMBER': (
                settings.OWNER_WHATSAPP_NUMBER
            ),
        }
    )