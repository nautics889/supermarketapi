from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status, viewsets
from .serializers import (OrderSerializer,
                          ProductSerializer,
                          DiscountSerializer)
from .models import Order, Product, Discounts


class CheckoutView(APIView):
    """Handle order requests"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order.html'
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        """Handle get-request"""
        #get product to display for user
        product_queryset = Product.objects.all()
        #get total sum of user's orders
        total_sum = Order.checkout.get_cost_of_orders(request.user)
        #get list of goods
        goods, extra_goods = Order.checkout.get_goods(request.user)
        return Response({'products': product_queryset,
                         'total_sum': total_sum,
                         'goods': goods,
                         'extra_goods': extra_goods})

    def post(self, request):
        """Handle post-request"""
        product_queryset = Product.objects.all()
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            #save order if it's valid
            serializer.save(user=request.user)
            #get total sum of user's orders
            total_sum = Order.checkout.get_cost_of_orders(request.user)
            #get list of goods
            goods, extra_goods = Order.checkout.get_goods(request.user)
            return Response({'products': product_queryset,
                             'total_sum': total_sum,
                             'goods': goods,
                             'extra_goods': extra_goods}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_ordering(request):
    """An endpoint for reset an order list"""
    Order.objects.filter(user=request.user).delete()
    return HttpResponseRedirect(reverse('ordering'))

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAdminUser,)

class DiscountsViewSet(viewsets.ModelViewSet):
    queryset = Discounts.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (permissions.IsAdminUser,)