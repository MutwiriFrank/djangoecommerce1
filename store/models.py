from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=13, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.name

    @property  # decorator to help us assign image_url as a variable
    def image_url(self):  # so that we don't get an error in case an image fails to load,
        try:     # instead we get an empty string
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)
    complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.transaction_id)

    @property
    def get_order_total(self):  # total price
        order_items = self.orderitem_set.all()
        total = sum(item.get_total for item in order_items)
        return total


    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for item in order_items:
            if item.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_total_quantity(self):
        order_items = self.orderitem_set.all()
        total_quantity = sum(item.quantity for item in order_items)
        return total_quantity


class OrderItem(models.Model):
    product = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        return self.product.name

    @property  # allows us to call get tottal as a variable intead of gettotal()
    def get_total(self):
        total = self.product.price * self.quantity
        return total





class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=103, blank=False, null=False)
    road = models.CharField(max_length=130, null=False)
    landmark = models.CharField(max_length=130, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        return self.location
