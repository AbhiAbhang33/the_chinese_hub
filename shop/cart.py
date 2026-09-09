"""
Simple session-based shopping cart.
No login required — cart persists in the visitor's browser session.
"""
from decimal import Decimal
from .models import FoodItem

CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def _key(self, item_id, size):
        return f"{item_id}_{size}"

    def add(self, food_item: FoodItem, size: str, quantity: int = 1):
        size = size.upper()
        key = self._key(food_item.id, size)
        price = food_item.half_price if size == 'HALF' and food_item.half_price else food_item.full_price

        if key in self.cart:
            self.cart[key]['quantity'] += quantity
        else:
            self.cart[key] = {
                'item_id': food_item.id,
                'name': food_item.name,
                'size': size,
                'price': str(price),
                'quantity': quantity,
            }
        self.save()

    def update(self, key, quantity):
        if key in self.cart:
            if quantity <= 0:
                del self.cart[key]
            else:
                self.cart[key]['quantity'] = quantity
            self.save()

    def remove(self, key):
        if key in self.cart:
            del self.cart[key]
            self.save()

    def clear(self):
        self.cart = {}
        self.save()

    def save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        for key, item in self.cart.items():
            item = dict(item)
            item['key'] = key
            item['price'] = Decimal(item['price'])
            item['subtotal'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def is_empty(self):
        return len(self.cart) == 0
