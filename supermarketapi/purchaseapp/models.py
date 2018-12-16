from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator


class CheckoutManager(models.Manager):
    """A manager that defines main logic of application. It counts costs and products"""
    def get_cost_of_orders(self, user):
        orders = Order.objects.filter(user=user)

        #it counts sum of products...
        costs = []
        for order in orders:
            if order.product.by_weight:
                costs.append(float(order.product.cost) * float(order.weight))
            else:
                costs.append(float(order.product.cost) * float(order.amount))
        cost = sum(costs)

        #get dict of goods ('prod': 'amount')
        goods_dict = CheckoutManager._get_goods_dict(orders)
        #count cost's value with discounts
        for product in goods_dict:
            try:
                #try to get discount
                discount = Discounts.objects.get(product=product)
                #if successful, count number of discounts goods we have ordered
                number_of_discounted_goods = goods_dict[product] // discount.quantity
                #subtract discounts.coef*product.cost*number_of_discounted_goods from the cost
                cost -= number_of_discounted_goods*float(product.cost)*float(discount.coef)
            except ObjectDoesNotExist:
                pass

        return round(cost, 2)

    def get_goods(self, user):
        #get users orders
        orders = Order.objects.filter(user=user)
        #get dict of goods
        goods_dict = CheckoutManager._get_goods_dict(orders)
        #create dict of bonus goods
        extra_goods_dict = dict()
        #look for promotional products...
        for product in goods_dict:
            try:
                #try to find product in promotional products
                promo_product = PromoProduct.objects.get(product=product)
                extra = promo_product.extra_product
                #count how many extra products must be added to the order
                quantity = extra.quantity_extra*(goods_dict[product]//promo_product.quantity_required)
                extra_goods_dict[extra.product] = quantity
            except ObjectDoesNotExist:
                pass

        return (goods_dict.items(), extra_goods_dict.items())

    def _get_goods_dict(users_orders):
        """Get dict with goods"""
        goods_dict = dict()
        for order in users_orders:
            #set addend as weight or amount
            addend = order.weight if order.product.by_weight else order.amount
            #add to dict's value
            goods_dict[order.product] = goods_dict.get(order.product, 0) + addend
        return goods_dict


class Product(models.Model):
    """Product model"""
    name = models.CharField(max_length=1, unique=True)
    cost = models.DecimalField(decimal_places=2, max_digits=5)
    by_weight = models.BooleanField(default=False)

class Order(models.Model):
    """Order model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    amount = models.SmallIntegerField(default=None,
                                      blank=True,
                                      null=True,
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(20)])
    weight = models.DecimalField(decimal_places=1, max_digits=3, default=None, blank=True, null=True)

    objects = models.Manager()
    checkout = CheckoutManager()

class Discounts(models.Model):
    """Discounts cut prices for goods defined in 'product' field in case of wholesales.
    Discount applies to each n-th good, n set in 'quantity' field"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    coef = models.DecimalField(decimal_places=2, max_digits=3)

class Extra(models.Model):
    """This instance contains extra product which can be added free after order promoproduct"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity_extra = models.SmallIntegerField(default=1)

class PromoProduct(models.Model):
    """This instance contains products which allow us to win an extraproduct"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity_required = models.SmallIntegerField(default=2)

    extra_product = models.OneToOneField(Extra, on_delete=models.CASCADE)