from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignUpForm
from .models import *
from django.core.exceptions import PermissionDenied
from django.db.models import Sum




# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    context = {
        "user":request.user,
        "menu":Menu_Item.objects.all(),
        "categories":Category.objects.all(),
        "items":Shopping_Cart_Item.objects.filter(user=User.objects.get(pk=request.user.id)).filter(cart=None).count()
    }
    return render(request, "orders/index.html", context)

def login_view(request):
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user is not None:
          login(request, user)
          return HttpResponseRedirect(reverse("index"))
      else:
          return render(request, "orders/login.html", {"message": "Invalid credentials."})

def logout_view(request):
      logout(request)
      return render(request, "orders/login.html", {"message": "Logged out."})

def register_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        form = SignUpForm()
    return render(request, 'orders/register.html', {'form': form})

def menu_item(request, menu_item_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    try:
        menu_item = Menu_Item.objects.get(pk=menu_item_id)
    except:
        raise Http404("Menu item no longer exists")
    context = {
        "menu_item": menu_item,
        "toppings":menu_item.category.toppings.all(),
        "special_toppings":menu_item.special_toppings.all(),
        "items":Shopping_Cart_Item.objects.filter(user=User.objects.get(pk=request.user.id)).filter(cart=None).count()
    }
    return render(request, "orders/menu_item.html", context)

def add_to_cart(request, menu_item_id):
    total_price = 0
    toppings_in_item = list()
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    try:
        menu_item = Menu_Item.objects.get(pk=menu_item_id)
        user = User.objects.get(pk=request.user.id)
        size = request.POST["size"]
        amount = int(request.POST.get("amount", 0))
        price = getattr(menu_item, size+"_price", False)*amount

    except menu_item.DoesNotExist:
        return HttpResponseRedirect(reverse("menu_item", args=(menu_item.id,)))
    special_toppings = request.POST.getlist("special_toppings", False)
    toppings = request.POST.getlist("toppings")


    if toppings:
        if len(toppings) != menu_item.number_of_toppings:
            return HttpResponseRedirect(reverse("menu_item", args=(menu_item.id,)))
        for topping in toppings:
            toppings_in_item.append(Topping.objects.get(pk=int(topping)))


    if special_toppings:
        for topping in special_toppings:

            special_topping = Topping.objects.get(pk=int(topping))

            total_price += special_topping.special_price
            toppings_in_item.append(special_topping)


    total_price += price
    shopping_cart_item = Shopping_Cart_Item(user=user,
                                            item=menu_item,
                                            amount=amount,
                                            size=size,
                                            price=total_price)

    shopping_cart_item.save()

    for topping in toppings_in_item:

        shopping_cart_item.toppings.add(topping)

    shopping_cart_item.save()

    return HttpResponseRedirect(reverse("index"))

def cart(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    user = User.objects.get(pk=request.user.id)
    cart = Shopping_Cart_Item.objects.all().filter(user=user).filter(cart=None)

    context = {
        "total_price": cart.aggregate(total_price=Sum('price'))['total_price'],
        "cart": cart,
        "items":Shopping_Cart_Item.objects.filter(user=User.objects.get(pk=request.user.id)).filter(cart=None).count()
    }
    return render(request, "orders/cart.html", context)

def order(request):
    user = User.objects.get(pk=request.user.id)
    cart = Shopping_Cart_Item.objects.all().filter(user=user).filter(cart=None)

    new_order = Order(user=user)
    new_order.save()

    for item in cart:
        item.cart=new_order
        item.save()

    return HttpResponseRedirect(reverse("index"))

def view_orders(request):
    if request.user.is_staff:
        orders = Order.objects.all()

        context = {
            "orders":orders
        }
        return render(request, "orders/view_orders.html", context)
    else:
        raise PermissionDenied

def view_order(request, order_id):
    if request.user.is_staff:
        order = Order.objects.get(pk=order_id)
        context = {
            "order":order
        }
        return render(request, "orders/view_order.html", context)
    else:
        raise PermissionDenied
