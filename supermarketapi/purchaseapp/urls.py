from django.urls import path
from .views import CheckoutView, reset_ordering, ProductViewSet, DiscountsViewSet

product_list = ProductViewSet.as_view({
    'post': 'create'
})
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

discounts_list = DiscountsViewSet.as_view({
    'post': 'create'
})
discounts_detail = DiscountsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('reset/', reset_ordering, name='reset_ordering'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('product/', product_list, name='add_product'),
    path('discount/<int:pk>/', discounts_detail, name='discount_detail'),
    path('discount/', discounts_list, name='add_discount'),
    path('', CheckoutView.as_view(), name='ordering'),
]