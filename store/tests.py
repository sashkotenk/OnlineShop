from django.test import TestCase, Client
from django.urls import reverse
from store.views import PRODUCTS

class StoreAppTests(TestCase):
    def setUp(self):
        # Налаштовуємо тестового клієнта для імітації HTTP-запитів
        self.client = Client()

    def test_home_redirects_to_all_items(self):
        # Тестуємо, що при зверненні до головної сторінки відбувається редірект на сторінку з усіма товарами
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('all_items'))

    def test_about_page(self):
        # Тестуємо сторінку "Про нас" - перевіряємо код відповіді та використання правильного шаблону
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_all_items_view(self):
        response = self.client.get(reverse('all_items'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
        # Перевіряємо, що в контексті передається повний список PRODUCTS
        self.assertEqual(len(response.context['products']), len(PRODUCTS))

    def test_popular_items_view(self):
        response = self.client.get(reverse('popular_items'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
        # Вибірка популярних: rating == 5
        popular = [p for p in PRODUCTS if p.get('rating') == 5]
        self.assertEqual(len(response.context['products']), len(popular))

    def test_new_arrivals_view(self):
        response = self.client.get(reverse('new_arrivals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
        # Новинки: is_new == True, але не більше 2
        arrivals = [p for p in PRODUCTS if p.get('is_new')]
        self.assertLessEqual(len(response.context['products']), 2)
        self.assertListEqual(response.context['products'], arrivals[:2])

    def test_product_detail_valid_and_invalid(self):
        # Вірний ID
        prod = PRODUCTS[0]
        response = self.client.get(reverse('product_detail', args=[prod['id']]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/detail.html')
        self.assertEqual(response.context['product']['id'], prod['id'])
        response = self.client.get(reverse('product_detail', args=[9999]))
        # очікуємо 404 Not Found
        self.assertEqual(response.status_code, 404)

    def test_add_to_cart_and_cart_view(self):
        prod_id = PRODUCTS[1]['id']
        # додаємо 3 одиниці
        response = self.client.get(reverse('add_to_cart', args=[prod_id]) + '?qty=3')
        # має редіректитись у cart
        self.assertRedirects(response, reverse('cart'))
        # дивимось сесію
        session = self.client.session
        self.assertIn(str(prod_id), session['cart'])
        self.assertEqual(session['cart'][str(prod_id)], 3)

        # Перевірка відображення корзини
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')
        self.assertIn('items', response.context)
        # Має бути хоча б один елемент
        self.assertTrue(len(response.context['items']) >= 1)

    def test_remove_from_cart(self):
        prod_id = PRODUCTS[1]['id']
        # Спочатку додати
        session = self.client.session
        session['cart'] = {str(prod_id): 2}
        session.save()

        # Видалити
        response = self.client.get(reverse('remove_from_cart', args=[prod_id]))
        self.assertRedirects(response, reverse('cart'))
        session = self.client.session
        # Після видалення товару в корзині не мусить бути
        self.assertNotIn(str(prod_id), session.get('cart', {}))
