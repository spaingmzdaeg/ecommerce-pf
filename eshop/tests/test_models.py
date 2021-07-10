from django.http import response
from django.test import TestCase
from ..models import *
#from eshop.models import *
#from .. models import Customer, Product

class TestAppModels(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(
            name = "Nintendo Switch", price=200.00, digital=False, image="/product_pics/ns.png"
        )

        self.product2 = Product.objects.create(
            name = "Mario Kart 8 Deluxe", price=59.99, digital=False
        )

        self.product3 = Product.objects.create(
            name = "Splatoon 2", price=9.99, digital=False, image=""
        )

        self.product4 = Product.objects.create(
            name = "Super Mario Maker", price=9.99, digital=True, image=""
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

        self.orderitem2 = OrderItem.objects.create(
            product=self.product2, quantity = 1, order=self.order1
        )

        self.order2 = Order.objects.create(
            customer=self.customer1, complete=False
        )

        self.orderitem3 = OrderItem.objects.create(
            product=self.product4, quantity = 1, order=self.order2
        )

        self.shippingaddress1 = ShippingAddress.objects.create(
            customer=self.customer1, order=self.order1, address="NYC Department #21", city="New York",
            state="New York", zipcode="23400"
        )



    def test_model_str_customer(self):
        self.assertEquals(str(self.customer1), "peter-parker")

    def test_model_str_product(self):
        self.assertEquals(str(self.product1), "Nintendo Switch")

    def test_model_str_order(self):
        self.assertEquals(str(self.order1), "1-peter-parker")

    def test_model_str_order_item(self):
        self.assertEquals(str(self.orderitem1), "1")

    def test_model_str_shipping_address(self):
        self.assertEquals(str(self.shippingaddress1), "NYC Department #21")

    def test_get_absolute_url_product(self):
        self.assertEquals(self.product1.get_absolute_url(), '/product/1')

    def test_image_url(self):
        self.assertEquals(self.product1.imageURL, "/media/product_pics/ns.png")

    def test_image_url_default(self):
        self.assertEquals(self.product2.imageURL, "/media/default/placeholder.png")

    def test_image_url_empty(self):
        self.assertEquals(self.product3.imageURL, "")         

    def test_product_is_assigned_slug_on_creation(self):
        self.assertEquals(self.product1.slug, 'nintendo-switch')

    def test_get_cart_total_order(self):
        self.assertEquals(self.order1.get_cart_total, 459.99)

    def test_get_cart_items_order(self):
        self.assertEquals(self.order1.get_cart_items, 3)

    def test_get_total_order_item(self):
        self.assertEquals(self.orderitem1.get_total, 400)

    def test_shipping(self):
        self.assertEquals(self.order1.shipping, True)    

    def test_shipping_false(self):
        self.assertEquals(self.order2.shipping, False)    