from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from .utils import *
import datetime

# Create your views here.


def store(request):
    products = Item.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        ordered_items = order.orderitem_set.all()
        no_cart_items = Order.get_total_quantity
    else:
        cookieData = cookieCart(request)
        no_cart_items = cookieData['no_cart_items']
    context = {
        "no_cart_items": no_cart_items,
        "products": products,
    }

    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        ordered_items = order.orderitem_set.all()
        no_cart_items = order.get_total_quantity


        # get_or_create method is that it actually  returns a tuple of(object, created)
        # The first element is an instance of the model you are trying to retrieve
        # and the second is a boolean flag to tell if the instance was created or not.
        # True means the instance was created by the get_or_create method and False means
        # it was retrieved from the database.

    else:

        cookieData = cookieCart(request)
        ordered_items = cookieData['ordered_items']
        no_cart_items = cookieData['no_cart_items']
        order = cookieData['order']



    context = {
        'no_cart_items': no_cart_items,
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
        cookieData = cookieCart(request)
        no_cart_items = cookieData['no_cart_items']
        ordered_items = cookieData['ordered_items']
        order = cookieData['order']
    context = {
        "ordered_items": ordered_items,
        "order": order,
        "no_cart_items": no_cart_items,

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


def process_order(request):
    # print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        name = data['form']['name']
        email = data['form']['email']
        phone = data['form']['phone']

        customer, created = Customer.objects.get_or_create(phone = phone)
        customer.name = name
        customer.email = email
        customer.phone = phone
        customer.save()

        cookieData = cookieCart(request)
        ordered_items = cookieData['ordered_items']
        order = Order.objects.create(customer=customer, complete=False)

        for item in ordered_items:
            product = Item.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(product=product, order=order)
            quantity = item['quantity']

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_order_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            location=data['shipping']['location'],
            road=data['shipping']['road'],
            landmark=data['shipping']['landmark'],

        )
        

    return JsonResponse('Payment submitted ...', safe=False)
