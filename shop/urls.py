from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<str:key>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path("send-bill-whatsapp/<int:order_id>/", views.send_bill_whatsapp, name="send_bill_whatsapp"),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
]
