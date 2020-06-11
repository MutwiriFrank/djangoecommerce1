import json
from . models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('cart:', cart)

    ordered_items = []  # empty dictionary
    order = {
        # to avoid an error if a user access the page and is not authenticated, creaate a dictionary just give them default values
        # this is because context is expecting ordered_items and order, since they  rendered in front page
        'get_order_total': 0,
        'get_total_quantity': 0,
        'shipping': False,
    }
    no_cart_items = order['get_total_quantity']

    for i in cart:  # looping through a dictionary
        try:
            print(i)

            no_cart_items += cart[i]["quantity"]

            product = Item.objects.get(id=i)
            total = (product.price * (cart[i]["quantity"]))

            # updating the above order dictionary

            order['get_order_total'] += total
            order['get_total_quantity'] = cart[i]["quantity"]

            ordered_item = {
                'id': product.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url,

                },
                'quantity': cart[i]["quantity"],
                'get_total': total

            }
            ordered_items.append(ordered_item)

            if product.digital == False:
                order['shipping'] = True

   

        except:
            pass
    return {'no_cart_items': no_cart_items, 'order': order, 'ordered_items':ordered_items }

