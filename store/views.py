from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *

# Create your views here.


def store(request):
    products = Item.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        ordered_items = order.orderitem_set.all()
        cart_items = Order.get_total_quantity
    else:
        ordered_items = []
        order = {  # to avoid an error if a user access the page and is not authenticated, just give them default values
            # this is because context is expecting ordered_items and order, since they  rendered in front page
            'get_order_total': 0,
            'get_total_quantity': 0,
            'shipping': False,
        }
        cart_items = order['get_total_quantity']
    context = {
        "ordered_items": ordered_items,
        "order": order,
        "products": products,
        "cart_items":cart_items,
    }

    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        ordered_items = order.orderitem_set.all()



        # get_or_create method is that it actually  returns a tuple of(object, created)
        # The first element is an instance of the model you are trying to retrieve
        # and the second is a boolean flag to tell if the instance was created or not.
        # True means the instance was created by the get_or_create method and False means
        # it was retrieved from the database.

    else:
        ordered_items = [ ]
        order = {  # to avoid an error if a user access the page and is not authenticated, just give them default values
            # this is because context is expecting ordered_items and order, since they  rendered in front page
            'get_order_total': 0,
            'get_total_quantity': 0,
            'shipping': False,

        }
    context = {
        "ordered_items": ordered_items,
        "order": order,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        ordered_items = order.orderitem_set.all()
        print(order.shipping)

    else:
        ordered_items = [ ]
        order = {  # to avoid an error if a user access the page and is not authenticated
            'get_order_total': 0,
            'get_total_quantity': 0,
            'shipping': False,

        }
    context = {
        "ordered_items": ordered_items,
        "order": order,


    }
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    # request.body  fetch body(data) sent from cart.js->body: JSON.stringify({'productId': productId, 'action':action})

    # once we parce we get a dictionary which can be accessed as below

    productId = data['productId']
    action = data['action']

    customer = request.user.customer  # will only work on logged in user
    product = Item.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    print('productId', productId)
    print('action', action)

    return JsonResponse('Item was added successfully', safe=False)
