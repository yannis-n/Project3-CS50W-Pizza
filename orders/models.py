from django.db import models
from django.conf import settings



class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Categories"


    def __str__(self):
        return f"{self.name}"


class Topping(models.Model):
    name = models.CharField(max_length=64)
    category = models.ManyToManyField(Category, related_name="toppings", blank=True, null=True)
    special_price = models.DecimalField(max_digits=5,decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Menu_Item(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    small_price = models.DecimalField(max_digits=5,decimal_places=2, blank=True, null=True)
    large_price = models.DecimalField(max_digits=5,decimal_places=2, blank=True, null=True)
    one_size_price = models.DecimalField(max_digits=5,decimal_places=2, blank=True, null=True)
    number_of_toppings = models.PositiveIntegerField(default=0)
    special_toppings = models.ManyToManyField(Topping, blank=True, related_name="items")

    def __str__(self):
        return f"{self.category}: {self.name}"

class Order(models.Model):
    COMPLETED = "completed"
    PENDING = "pending"

    STATUS=[
    (COMPLETED, "completed"),
       (PENDING, "pending")
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    transaction=models.CharField(max_length=64, choices = STATUS, default=PENDING)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} in {self.datetime}    Status:{self.transaction}"

class Shopping_Cart_Item(models.Model):
    SMALL = "small"
    LARGE = "large"
    ONE_SIZE = "one size"
    PIZZA_SIZE=[
    (SMALL, "small"),
       (LARGE, "large"),
       (ONE_SIZE, "one size")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu_Item, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    toppings = models.ManyToManyField(Topping, blank=True)
    size = models.CharField(max_length=64, choices = PIZZA_SIZE)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    cart = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, related_name="items_in_order", null=True)

    def __str__(self):
        return f"Item:#{self.id} Ordered by:{self.user} {self.item.name}"
