from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Category


def all_products(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products, 'categories': categories})

def category_products(request, category_id):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=selected_category)
    return render(request, 'store/home.html', {'products': products, 'categories': categories, 'selected_category': selected_category})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        product.qty = qty
        product.total_price = qty * product.price
        total += product.total_price
        products.append(product)
    return render(request, 'store/cart.html', {'products': products, 'total': total})

def checkout(request):
    request.session['cart'] = {}  # clear cart after order
    return render(request, 'store/checkout_success.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')

def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        cart[str(product_id)] = qty
    else:
        cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')