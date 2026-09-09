from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    """e.g. Starters, Noodles, Rice, Manchurian, Soups, Beverages"""
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order on the menu page")

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='food_items/', blank=True, null=True)

    # Some items are single-price only (e.g. a drink) so half price is optional.
    half_price = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True,
        validators=[MinValueValidator(0)],
        help_text="Leave blank if this item has no 'half' option"
    )
    full_price = models.DecimalField(
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Full / single price"
    )

    is_available = models.BooleanField(default=True)
    is_veg = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category__order', 'name']

    def __str__(self):
        return self.name

    def has_half_option(self):
        return self.half_price is not None


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('OUT_FOR_DELIVERY', 'Out for delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    ORDER_TYPE_CHOICES = [
        ('DELIVERY', 'Home Delivery'),
        ('PICKUP', 'Self Pickup'),
    ]

    customer_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default='DELIVERY')
    notes = models.CharField(max_length=255, blank=True)

    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    service_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    bill_pdf = models.FileField(upload_to='bills/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def items_subtotal(self):
        return self.total_amount - self.service_charge

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} - ₹{self.total_amount}"

    def recalculate_total(self):
        from django.conf import settings
        items_total = sum(item.subtotal() for item in self.items.all())
        self.service_charge = settings.SERVICE_CHARGE
        self.total_amount = items_total + self.service_charge
        self.save(update_fields=['total_amount', 'service_charge'])
        return self.total_amount


class OrderItem(models.Model):
    SIZE_CHOICES = [
        ('HALF', 'Half'),
        ('FULL', 'Full'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=150)  # snapshot, survives menu edits
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, default='FULL')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.item_name} ({self.size}) x{self.quantity}"
