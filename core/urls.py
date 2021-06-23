from django.urls import path
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    AddCouponView,
    RequestRefundView,
    CatalogView,
    Get_Order
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('send-mail/', HomeView.send_mail, name='send-mail'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/<int:quantity>/', CheckoutView.add_to_cart, name='add-to-cart'),
    path('add-to-cart/<slug>/', CheckoutView.add_to_cart, name='add-to-cart-slug'),
    path('add-single-item-to-cart/<slug>/', OrderSummaryView.add_single_item_to_cart, name='add-single-item-to-cart'),
    path('order-summary/async-remove-from-cart/', OrderSummaryView.async_remove_from_cart, name='async-remove-from-cart'),
    path('order-summary/pay/<orderID>/<authorizationID>', OrderSummaryView.pay, name='pay-transaction'),
    path('order-summary/has-active-order/', OrderSummaryView.hasActiveOrder, name='has-active-order'),
    path('order-summary/resume', OrderSummaryView.resume, name='pay-resume'),
    path('remove-item-from-cart-summary/<slug>/', OrderSummaryView.remove_single_item_from_cart, name='remove-item-from-cart-summary')
]
