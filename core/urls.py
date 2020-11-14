from django.urls import path
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    CatalogView,
    Get_Order
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/<int:quantity>/', CheckoutView.add_to_cart, name='add-to-cart'),
    path('add-to-cart/<slug>/', CheckoutView.add_to_cart, name='add-to-cart-slug'),
    path('add-single-item-to-cart/<slug>/', OrderSummaryView.add_single_item_to_cart, name='add-single-item-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('order-summary/async-remove-from-cart/', OrderSummaryView.async_remove_from_cart, name='async-remove-from-cart'),
    path('order-summary/pay/<orderID>/<authorizationID>', OrderSummaryView.pay, name='pay-transaction'),
    path('order-summary/resume', OrderSummaryView.resume, name='pay-resume'),
    path('remove-item-from-cart/<slug>/', CheckoutView.remove_single_item_from_cart, name='remove-item-from-cart'),
    path('remove-item-from-cart-summary/<slug>/', OrderSummaryView.remove_single_item_from_cart, name='remove-item-from-cart-summary'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('order-summary/send-mail/', OrderSummaryView.email, name='send-mail'),
]
