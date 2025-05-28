from django.shortcuts import render, redirect
from django.http import Http404

# In-memory products for demonstration
PRODUCTS = [
    {"id":1, "sku":"BST-001","name":"Fancy Product","price":"40.00","old_price":None,"rating":None,"image":"https://dummyimage.com/450x300/dee2e6/6c757d.jpg","description":"Fancy Description","is_popular":False,"is_new":False},
    {"id":2, "sku":"BST-002","name":"Special Item","price":"18.00","old_price":"20.00","rating":5,"image":"https://dummyimage.com/450x300/dee2e6/6c757d.jpg","description":"Special Description","is_popular":True,"is_new":False},
    {"id":3, "sku":"BST-003","name":"Sale Item","price":"25.00","old_price":"50.00","rating":None,"image":"https://dummyimage.com/450x300/dee2e6/6c757d.jpg","description":"Sale Description","is_popular":False,"is_new":False},
    {"id":4, "sku":"BST-004","name":"Popular Item","price":"40.00","old_price":None,"rating":5,"image":"https://dummyimage.com/450x300/dee2e6/6c757d.jpg","description":"Popular Description","is_popular":True,"is_new":False},
    {"id":5, "sku":"BST-005","name":"New Arrival 1","price":"30.00","old_price":None,"rating":None,"image":"https://dummyimage.com/450x300/dee2e6/6c757d.jpg","description":"New 1","is_popular":False,"is_new":True},
    {"id":6, "sku":"BST-006","name":"New Arrival 2","price":"35.00","old_price":None,"rating":None,"image":"https://dummyimage.com/450x300/dee2e6/6c757d.jpg","description":"New 2","is_popular":False,"is_new":True},
]

def home(request):
    # Головна сторінка – редірект на сторінку зі всіма товарами
    return redirect("all_items")

def about(request):
    # Сторінка "Про нас"
    return render(request, "about.html")

def all_items(request):
    # Показати всі товари
    return render(request, "store/index.html", {"products": PRODUCTS})

def popular_items(request):
    # Відфільтрувати популярні товари (з рейтингом 5)
    pops = [p for p in PRODUCTS if p["rating"] == 5]
    return render(request, "store/index.html", {"products": pops})

def new_arrivals(request):
    news = [p for p in PRODUCTS if p.get("is_new", False)][:2]
    return render(request, "store/index.html", {"products": news})

def product_detail(request, pk):
    prod = next((p for p in PRODUCTS if p["id"] == pk), None)
    if prod is None:
        # якщо товару з таким pk немає - повертаємо 404
        raise Http404("Product not found")
    return render(request, "store/detail.html", {"product": prod})

def add_to_cart(request, pk):
    # Додати товар до корзини з кількістю qty (за замовчуванням 1)
    qty = int(request.GET.get("qty",1))
    cart = request.session.get("cart", {})
    cart[str(pk)] = cart.get(str(pk),0) + qty
    request.session["cart"] = cart
    return redirect("cart")

def remove_from_cart(request, pk):
    # Видалити товар з корзини
    cart = request.session.get("cart", {})
    cart.pop(str(pk), None)
    request.session["cart"] = cart
    return redirect("cart")

def cart_view(request):
    # Показати корзину: товари, їх кількість, підсумок та загальну суму
    cart = request.session.get("cart", {})
    items=[]; total=0
    for pid, qty in cart.items():
        prod = next((p for p in PRODUCTS if p["id"]==int(pid)), None)
        if prod:
            price=float(prod["price"])
            items.append({"product":prod,"qty":qty,"subtotal":price*qty})
            total+=price*qty
    return render(request, "store/cart.html", {"items":items, "total":total})
