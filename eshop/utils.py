import json
from . models import *

def cookie_cart(request):
    try:
        # Return a python dictionary
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart', cart)
    items = []  # List
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']

    for i in cart:
        try:
            cart_items += cart[i]['quantity']
            product = Product.objects.get(product_id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'product_id': product.product_id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems':cart_items, 'order':order, 'items':items}

def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        # items = OrderItem.objects.select_related('order').all()
        # items = OrderItem.objects.all().select_related('order')
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request) #Return A dictionary
        cart_items = cookie_data['cartItems']
        order = cookie_data['order']
        items = cookie_data['items']
    return {'cartItems':cart_items, 'order':order, 'items':items}   

def guess_order(request, data):
    print('User is not logged in')
    print('COOKIES:', request.COOKIES)

    first_name = data['form']['firstname']
    last_name = data['form']['lastname']
    email = data['form']['email']

    cookie_data = cookie_cart(request) # Return a Dictionary
    items = cookie_data['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )

    customer.first_name = first_name
    customer.last_name = last_name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False
    )

    for item in items:
        product = Product.objects.get(product_id=item['product']['product_id'])
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order        