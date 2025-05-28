from django.urls import path
from . import views

urlpatterns = [
     # Головна сторінка, редіректить на список усіх товарів
    path("", views.home, name="home"),
    # Сторінка "Про нас"
    path("about/", views.about, name="about"),
    # Відображення всіх товарів магазину
    path("shop/all/", views.all_items, name="all_items"),
    # Відображення популярних товарів (рейтинг 5)
    path("shop/popular/", views.popular_items, name="popular_items"),
    # Відображення новинок (до 2 штук)
    path("shop/new/", views.new_arrivals, name="new_arrivals"),
    # Детальна сторінка конкретного товару за його ID (pk)
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
     # Перегляд вмісту корзини
    path("cart/", views.cart_view, name="cart"),
    # Видалення товару з корзини за ID
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    # Додавання товару в корзину за ID
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
]
