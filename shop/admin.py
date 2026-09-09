from django.contrib import admin
from django.utils.html import format_html
from .models import Category, FoodItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order', 'name')


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'category', 'half_price', 'full_price', 'is_available', 'is_veg')
    list_filter = ('category', 'is_available', 'is_veg')
    search_fields = ('name',)
    list_editable = ('is_available',)
    readonly_fields = ('image_preview',)
    fields = ('category', 'name', 'description', 'image', 'image_preview',
              'half_price', 'full_price', 'is_available', 'is_veg')

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;">', obj.image.url)
        return "—"
    thumbnail.short_description = "Photo"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;">', obj.image.url)
        return "No image uploaded yet"
    image_preview.short_description = "Preview"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('food_item', 'item_name', 'size', 'price', 'quantity')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone_number', 'order_type', 'total_amount', 'status', 'bill_link', 'created_at')
    list_filter = ('status', 'order_type', 'created_at')
    search_fields = ('customer_name', 'phone_number')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('total_amount', 'service_charge', 'created_at', 'bill_link')

    def bill_link(self, obj):
        if obj.bill_pdf:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.bill_pdf.url)
        return "—"
    bill_link.short_description = "Bill"
