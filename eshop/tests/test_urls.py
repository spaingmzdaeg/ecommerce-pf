from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import *
#from eshop.views import store, cart, checkout
#from ..views import store, cart, checkout

class TestUrls(SimpleTestCase):
    def test_home_page_is_resolves(self):
        url = reverse('store')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, store)

    def test_cart_is_resolves(self):
        url = reverse('cart')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, cart)

    def test_checkout_is_resolves(self):
        url = reverse('checkout')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, checkout)        

'''
por si nos falta argumentos
    def test_checkout_is_resolves(self):
        url = reverse('checkout' , args=['some-checkout'])
        #print(resolve(url))
        self.assertEquals(resolve(url).func, checkout)     '''

'''
si usaras as view() en tu url
    def test_home_page_url_is_resolved(self):
        url = reverse('cart')
        #print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, cart)'''