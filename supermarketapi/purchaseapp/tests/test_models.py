from django.test import TestCase
from django.contrib.auth.models import User
from decimal import InvalidOperation

from purchaseapp.models import (Product,
                                Order,
                                Discounts,
                                Extra,
                                PromoProduct,
                                CheckoutManager)
from purchaseapp.tests import fixtures

class ProductTestCase(TestCase):
    """Test product model"""
    def test_correct_product(self):
        num = Product.objects.count()
        self.correct_product = Product(**fixtures.CORRECT_PRODUCT_A)
        self.correct_product.save()
        self.assertEqual(Product.objects.count(), num + 1)

    def test_product_with_incorrect_name(self):
        num = Product.objects.count()
        self.product_with_incorrect_name = Product(**fixtures.PRODUCT_WITH_INCORRECT_NAME)
        self.product_with_incorrect_name.save()
        self.assertEqual(Product.objects.count(), num + 1)

    def test_product_with_incorrect_price(self):
        self.product_with_incorrect_price = Product(**fixtures.PRODUCT_WITH_INCORRECT_PRICE)
        try:
            self.product_with_incorrect_price.save()
        except Exception as e:
            exc = e
        self.assertEqual(exc.__class__, InvalidOperation)

class OrderTestCase(TestCase):
    """Test order model"""
    def setUp(self):
        """Prepare user that commits order and product he orders"""
        self.user = User(**fixtures.USER_DATA)
        self.user.save()

        self.product = Product(**fixtures.CORRECT_PRODUCT_A)
        self.product.save()

    def test_correct_order(self):
        num = Order.objects.count()
        self.correct_order = Order(**fixtures.CORRECT_ORDER,
                                   user=User.objects.get(pk=1),
                                   product=Product.objects.get(pk=1))
        self.correct_order.save()
        self.assertEqual(Order.objects.count(), num + 1)

class DiscountTestCase(TestCase):
    """Test discount model"""
    def setUp(self):
        self.product = Product(**fixtures.CORRECT_PRODUCT_A)
        self.product.save()

    def test_correct_discount(self):
        num = Discounts.objects.count()
        self.correct_discount = Discounts(**fixtures.CORRECT_DISCOUNT,
                                          product=self.product)
        self.correct_discount.save()
        self.assertEqual(Discounts.objects.count(), num + 1)

class PromotionalTestCase(TestCase):
    """Test promotionalproduct and extraproduct models (both)"""
    def setUp(self):
        """Prepare promotional and extra products"""
        self.extra_product = Product(**fixtures.CORRECT_PRODUCT_A)
        self.extra_product.save()

        self.promotional_product = Product(**fixtures.PROMO_PRODUCT)
        self.promotional_product.save()

    def test_correct_promotional(self):
        num_extra = Extra.objects.count()
        num_promo = PromoProduct.objects.count()

        self.extra = Extra(product=self.extra_product)
        self.extra.save()

        self.promo_product = PromoProduct(product=self.promotional_product,
                                          extra_product=self.extra)
        self.promo_product.save()

        self.assertEqual(Extra.objects.count(), num_extra + 1)
        self.assertEqual(PromoProduct.objects.count(), num_promo + 1)

class CheckoutManagerTestCase(TestCase):
    """Test checkout manager (main business logic is here)"""
    def setUp(self):
        """Prepare user and goods"""
        self.user = User(**fixtures.USER_DATA)
        self.user.save()

        self.product_a = Product(**fixtures.CORRECT_PRODUCT_A)
        self.product_a.save()

        self.product_b = Product(**fixtures.CORRECT_PRODUCT_B)
        self.product_b.save()

        self.product_c = Product(**fixtures.CORRECT_PRODUCT_BY_WEIGHT)
        self.product_c.save()

        self.product_d = Product(**fixtures.CORRECT_PRODUCT_D)
        self.product_d.save()

        self.product_e = Product(**fixtures.CORRECT_PRODUCT_E)
        self.product_e.save()

        self.discount_a = Discounts(**fixtures.DISCOUNT_A,
                                    product=self.product_a)
        self.discount_a.save()

        self.discount_b = Discounts(**fixtures.DISCOUNT_B,
                                    product=self.product_b)
        self.discount_b.save()

    #for each case tests are below
    def test_order_a(self):
        order = Order(user=self.user,
                      product=self.product_a,
                      amount=3)
        order.save()
        cost = Order.checkout.get_cost_of_orders(self.user)
        self.assertEqual(cost, 1.3) #every final cost, which we comparing with, counted manually

    def test_order_b(self):
        order = Order(user=self.user,
                      product=self.product_b,
                      amount=2)
        order.save()
        cost = Order.checkout.get_cost_of_orders(self.user)
        self.assertEqual(cost, 0.45)

    def test_order_c(self):
        order = Order(user=self.user,
                      product=self.product_c,
                      weight=2.5)
        order.save()
        cost = Order.checkout.get_cost_of_orders(self.user)
        self.assertEqual(cost, 4.97)

    def test_order_d_and_e(self):
        order = Order(user=self.user,
                      product=self.product_d,
                      amount=1)
        order.save()
        order = Order(user=self.user,
                      product=self.product_e,
                      amount=1)
        order.save()
        cost = Order.checkout.get_cost_of_orders(self.user)
        self.assertEqual(cost, 2.1)