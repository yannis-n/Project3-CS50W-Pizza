from django.test import TestCase, Client
from django.db.models import Max

from .models import *
from django.contrib.auth.models import User

class OrdersTestCase(TestCase):
    #
    # @classmethod
    # def setUp(self):
    #     pizza = Category.objects.create(name="Pizza")
    #     sub = Category.objects.create(name="Sub")
    #
    #     ham = Topping.objects.create(name="ham", category="pizza")
    #     extra_cheese = Topping.objects.create(name="ham", special_price=0.50)
    #
    #     Menu_Item.objects.create(name="margarita",
    #                              category=pizza,
    #                              small_price=2.50,
    #                              large_price=5.00,
    #                             )
    #     Menu_Item.objects.create(name="tuna sandwich",
    #                              category=sub,
    #                              one_size_price=2.50,
    #                             )
    #
    #     Menu_Item.objects.create(name="steak sandwich",
    #                              category=sub,
    #                              one_size_price=2.50,
    #                              special_toppings=extra_cheese
    #                             )
    #     pass
    #
    #     def test_index(self):
    #         # c = Client()
    #         # response = c.get("/")
    #         self.assertTrue(True)
            # self.assertEqual(response.status_code, 200)
            # self.assertEqual(tesponse.context["menu"].count(),3)


    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")

        test_user1 = User.objects.create_user(username='testuser1')
        test_user2 = User.objects.create_user(username='testuser2')
        test_user1.save()
        test_user2.save()
        test_user1.set_password('12345')
        test_user2.set_password('12345')
        test_user1.save()
        test_user2.save()


        pizza = Category.objects.create(name="Pizza")
        sub = Category.objects.create(name="Sub")

        ham = Topping.objects.create(name="ham", category=pizza)
        extra_cheese = Topping.objects.create(name="extra_cheese", special_price=0.50)

        Menu_Item.objects.create(name="margarita",
                                 category=pizza,
                                 small_price=2.50,
                                 large_price=5.00,
                                )
        Menu_Item.objects.create(name="tuna sandwich",
                                 category=sub,
                                 one_size_price=2.50,
                                )

        steak_sandwich = Menu_Item.objects.create(name="steak_sandwich",
                                 category=sub,
                                 one_size_price=2.50,
                                 # special_toppings=extra_cheese
                                )

        steak_sandwich.special_toppings.add(extra_cheese)
        steak_sandwich.save()


    def test_category_name(self):
        category = Category.objects.get(pk=1)
        expected_name = f'{category.name}'
        self.assertEquals(expected_name, str(category))

    def test_topping_name(self):
        topping = Topping.objects.get(pk=1)
        expected_name = f'{topping.name}'
        self.assertEquals(expected_name, str(topping))

    def test_menu_item_name(self):
        item = Menu_Item.objects.get(pk=1)
        expected_name = f'{item.category}: {item.name}'
        self.assertEquals(expected_name, str(item))

    def test_index(self):
        c = Client()
        logged_in = c.login(username='testuser1', password='12345')
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['menu'])
        self.assertTemplateUsed('orders/index.html')
        self.assertEquals(response.context['menu'].count(),3)

    def test_index_no_login(self):
        c = Client()
        response = c.get("/")
        self.assertTemplateUsed('orders/login.html')

    def test_menu_item(self):
        i = Menu_Item.objects.get(name="margarita")
        c = Client()
        logged_in = c.login(username='testuser1', password='12345')
        response = c.get(f'/{i.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['menu_item'])
        self.assertEqual(response.context['toppings'].count(),1)

    def test_menu_item_no_login(self):
        i = Menu_Item.objects.get(name="margarita")
        c = Client()
        response = c.get(f'/{i.id}')
        self.assertTemplateUsed('orders/login.html')

    def test_invalid_menu_item(self):
        max_id = Menu_Item.objects.all().aggregate(Max("id"))['id__max']
        c = Client()
        logged_in = c.login(username='testuser1', password='12345')
        response = c.get(f'/{max_id + 1}')
        self.assertEqual(response.status_code, 404)

    def test_add_to_cart(self):
        menu_item = Menu_Item.objects.get(name="margarita")
        c = Client()
        logged_in = c.login(username='testuser1', password='12345')
        response = c.post(f'/add_to_cart/{menu_item.id}', {'size':'small', 'amount':1})
        shopping_cart_item = Shopping_Cart_Item.objects.get(pk=1)
        self.assertIsNotNone(shopping_cart_item)
        self.assertEquals(shopping_cart_item.price,2.50)

    def test_add_to_cart_with_special_toppings(self):
        menu_item = Menu_Item.objects.get(name="steak_sandwich")
        special_topping = Topping.objects.get(name="extra_cheese")
        c = Client()
        logged_in = c.login(username='testuser1', password='12345')
        response = c.post(f'/add_to_cart/{menu_item.id}', {'size':'one_size', 'amount':2, 'special_toppings':special_topping.id})
        shopping_cart_item = Shopping_Cart_Item.objects.get(pk=1)
        self.assertIsNotNone(shopping_cart_item)
        self.assertEquals(shopping_cart_item.price,5.50)
