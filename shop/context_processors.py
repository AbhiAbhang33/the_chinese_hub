from django.conf import settings
from .cart import Cart


def cart_count(request):
    try:
        cart = Cart(request)
        return {
            'cart_item_count': len(cart),
            'cart_total_price': cart.total_price(),
        }
    except Exception:
        return {'cart_item_count': 0, 'cart_total_price': 0}


def shop_contact(request):
    return {
        'shop_name': settings.SHOP_NAME,
        'owner_name': settings.OWNER_NAME,
        'owner_phone_display': settings.OWNER_PHONE_DISPLAY,
        'owner_phone_tel': settings.OWNER_PHONE_TEL,
        'service_charge': settings.SERVICE_CHARGE,
    }
