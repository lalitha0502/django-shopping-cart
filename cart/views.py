# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem
from django.http import HttpResponse

def product_list(request):
    products = Product.objects.all()
    return render(request, 'cart/index.html', {'products': products})

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user
    )
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')

def remove_single_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:view_cart')

def home(request):
    return HttpResponse('Hello, World!')

