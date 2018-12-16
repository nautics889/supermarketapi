from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from purchaseapp.tests import fixtures
from purchaseapp.models import Product, Order

class CheckoutViewTestCase(TestCase):
    """Test checkout view"""
    def setUp(self):
        self.user = User(**fixtures.USER_DATA)
        self.user.save()

        self.product = Product(**fixtures.CORRECT_PRODUCT_A)
        self.product.save()

        self.post_data = {
            'product': self.product.id,
            'amount': 3
        }
        self.incorrect_post_data = {
            'product': self.product.id,
            'weight': 3
        }

    def test_make_order(self):
        """Try to make a common order"""
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('ordering'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_make_incorrect_order(self):
        """Try to make incorrect order with wrong specified amount"""
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('ordering'), self.incorrect_post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_order(self):
        """Try to reset user's order"""
        self.client.force_login(user=self.user)
        self.client.post(reverse('ordering'), self.post_data)
        self.client.post(reverse('reset_ordering'))
        self.assertEqual(len(Order.objects.filter(user=self.user)), 0)

class ProductAndDiscountsViewSetsTestCase(TestCase):
    def setUp(self):
        self.admin_user = User(**fixtures.ADMIN_USER_DATA)
        self.admin_user.is_superuser = True
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.user = User(**fixtures.USER_DATA)
        self.user.save()

        self.product = Product(**fixtures.CORRECT_PRODUCT_B)
        self.product.save()

    def test_add_product(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.post(reverse('add_product'), fixtures.CORRECT_PRODUCT_A)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_product_not_admin(self):
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('add_product'), fixtures.CORRECT_PRODUCT_A)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_discount(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.post(reverse('add_discount'), dict(product=self.product.id, **fixtures.CORRECT_DISCOUNT))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_discount_not_admin(self):
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('add_discount'), dict(product=self.product.id, **fixtures.CORRECT_DISCOUNT))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)