from django.contrib import admin
from django.contrib.auth.models import User


from .models import *

class  Shopping_Cart_ItemInline(admin.TabularInline):
    model= Shopping_Cart_Item.toppings.through
    extra = 1

class Shopping_Cart_ItemAdmin(admin.ModelAdmin):
    list_display=['user', 'item', 'amount','price','size', 'price']
    list_filter=['user','item']
    filter_horizontal = ("toppings",)

class OrderAdmin(admin.ModelAdmin):
    Inlines = [
        Shopping_Cart_ItemInline
    ]

class ToppingInline(admin.TabularInline):
    model = Topping.category.through
    extra = 1

class Menu_ItemInline(admin.StackedInline):
    model = Menu_Item.special_toppings.through
    extra = 1

class ToppingAdmin(admin.ModelAdmin):
      inlines = [Menu_ItemInline]
      inlines = [Shopping_Cart_ItemInline]
      filter_horizontal = ("category",)

class Menu_ItemAdmin(admin.ModelAdmin):
    list_display=['name', 'category', 'small_price','large_price','one_size_price', 'number_of_toppings']
    list_filter=['category']
    filter_horizontal = ("special_toppings",)


# class Shopping_CartAdmin(admin.ModelAdmin):
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         if db_field.name == "toppings":
#             kwargs["queryset"] = db_field.name.filter(category = self.item.category)
#         return super(MyModelAdmin, self).formfield_formanytomany(db_field, request, **kwargs)

admin.site.register(Category)
admin.site.register(Shopping_Cart_Item,Shopping_Cart_ItemAdmin)
admin.site.register(Topping, ToppingAdmin)
admin.site.register(Menu_Item, Menu_ItemAdmin)
admin.site.register(Order, OrderAdmin)
