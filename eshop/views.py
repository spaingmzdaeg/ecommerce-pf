from django.shortcuts import get_object_or_404, render
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookie_cart, cart_data, guess_order

# Create your views here.


def store(request):
    data = cart_data(request)
    cart_items = data['cartItems']
    

    products = Product.objects.only('name', 'price', 'image','product_id')
    context = {'products': products, 'cartitems': cart_items}
    return render(request, 'eshop/store.html', context)


def cart(request):
    data = cart_data(request)
    
    cart_items = data['cartItems']
    order = data['order']
    items = data['items']
     

    context = {'items': items, 'order': order, 'cartitems': cart_items}
    return render(request, 'eshop/cart.html', context)


def checkout(request):
    data = cart_data(request)

    cart_items = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartitems': cart_items}
    return render(request, 'eshop/checkout.html', context)


def product_detail(request, id):
    data = cart_data(request)
    cart_items = data['cartItems']
    context = {'product': get_object_or_404(Product, product_id=id), 'cartitems':cart_items}
    return render(request, 'eshop/product_details.html', context)


def update_item(request):
    data = json.loads(request.body)  # Return a Python dictionary
    product_id = data['productId']  # get value from dictionary
    action = data['action']
    print('Action:', action)
    print('ProductId:', product_id)

    customer = request.user.customer
    product = Product.objects.get(product_id=product_id)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)





def process_order(request):
    #print('Data:', request.body)
    data = ''
    try:
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)  # Return a Python dictionary
        #data = json.loads(data)
        print('Data:', data)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)       
            
        else:
            customer, order = guess_order(request, data)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        
        order.save() 

        if order.shipping == True:
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    # get value from dictionary
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode']
                )

    except ValueError:
        print ('Decoding json has failed')     
    

    return JsonResponse(data, safe=False)