
from django.urls import path
from . import views

urlpatterns = [
    #Leave as empty string for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('product/<str:id>', views.product_detail, name="product_detail"),
    path('updateitem/', views.update_item, name="update_item"),
    path('processorder/', views.process_order, name="process_order"),
    

]
