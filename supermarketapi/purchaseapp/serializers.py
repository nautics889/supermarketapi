from rest_framework import serializers
from .models import Order, Product, Discounts

class OrderSerializer(serializers.ModelSerializer):
    #required only one of fields below
    amount = serializers.IntegerField(required=False)
    weight = serializers.FloatField(required=False)

    def validate(self, data):
        """Validate amount or weight values accordingly to data['product'].by_weight"""
        if data.get('product').by_weight:
            if data.get('weight', 0) <= 0:
                raise serializers.ValidationError('Weight must be positive number')
            elif data.get('weight', 0) >= 100:
                raise serializers.ValidationError('Weight must be less than 100')
        else:
            if data.get('amount', 0) <= 0:
                raise serializers.ValidationError('Amount must be positive number')
            elif data.get('amount', 0) >= 20:
                raise serializers.ValidationError('Amount must be less than 20')

        return data

    class Meta:
        model = Order
        fields = ('product', 'amount', 'weight')

class ProductSerializer(serializers.ModelSerializer):
    by_weight = serializers.BooleanField(required=False)

    class Meta:
        model = Product
        fields = ('name', 'cost', 'by_weight')

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discounts
        fields = ('product', 'quantity', 'coef')