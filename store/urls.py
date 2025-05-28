from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("shop/all/", views.all_items, name="all_items"),
    path("shop/popular/", views.popular_items, name="popular_items"),
    path("shop/new/", views.new_arrivals, name="new_arrivals"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
]
