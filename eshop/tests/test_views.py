from django.http import response
from django.test import TestCase, Client, client
from django.urls import reverse
import json

from django.utils import safestring
from ..models import *
#from eshop.models import Product, Customer, Order, OrderItem

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.product1 = Product.objects.create(
            name = "Nintendo Switch", price=200.00, digital=False, image="/product_pics/ns.png"
        )

        self.customer1 = Customer.objects.create(
            first_name = "peter", last_name="parker", email="peterparker@gmail.com"
        )

        self.order1 = Order.objects.create(
            customer=self.customer1, complete=False
        )

        self.orderitem1 = OrderItem.objects.create(
            product=self.product1, quantity = 2, order=self.order1
        )

    def test_store(self):
        response = self.client.get(reverse('store'))
        self.assertEquals(response.status_code, 200)
        #self.assertEquals(response, 'eshop/store.html')
    
    def test_cart(self):
        response =  self.client.get(reverse('cart'))
        self.assertEquals(response.status_code, 200)

    def test_product_detail(self):
       
        response = self.client.get(self.product1.get_absolute_url())
        self.assertEquals(response.status_code, 200)

    def test_checkout(self):
        response = self.client.get(reverse('checkout'))
        self.assertEquals(response.status_code, 200)
