from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("<int:menu_item_id>", views.menu_item, name="menu_item"),
    path("add_to_cart/<int:menu_item_id>", views.add_to_cart, name="add_to_cart"),
    path("cart", views.cart, name="cart"),
    path("delete_cart_item/<int:item_id>", views.delete_cart_item, name="delete_cart_item"),
    path("order", views.order, name="order"),
    path("view_orders", views.view_orders, name="view_orders"),
    path("view_order/<int:order_id>", views.view_order, name="view_order"),
    path("order_completed/<int:order_id>", views.order_completed, name="order_completed"),
    path("history", views.history, name="history")

]
