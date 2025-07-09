from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Cart, CartItem
from products.models import Product


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Create session if it doesn't exist
        if not request.session.session_key:
            request.session.create()
        
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )
    
    return cart


def cart_detail(request):
    """Display cart contents"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def add_to_cart(request):
    """Add product to cart via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        if not product.is_in_stock:
            return JsonResponse({
                'success': False,
                'message': 'Product is out of stock'
            })
        
        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_total_items': cart.total_items,
            'cart_total_price': float(cart.total_price)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@require_POST
def remove_from_cart(request):
    """Remove item from cart via AJAX"""
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('cart_item_id')
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_total_items': cart.total_items,
            'cart_total_price': float(cart.total_price)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@require_POST
def update_cart(request):
    """Update cart item quantity via AJAX"""
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('cart_item_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({
                'success': False,
                'message': 'Quantity must be at least 1'
            })
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated',
            'cart_total_items': cart.total_items,
            'cart_total_price': float(cart.total_price)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


def clear_cart(request):
    """Clear all items from cart"""
    cart = get_or_create_cart(request)
    cart.clear()
    messages.success(request, 'Cart cleared successfully!')
    return redirect('cart:cart_detail')


# Traditional form-based views for fallback
def add_to_cart_form(request, product_id):
    """Add product to cart via form submission"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if not product.is_in_stock:
        messages.error(request, 'Product is out of stock')
        return redirect('products:product_detail', slug=product.slug)
    
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart:cart_detail')


def remove_from_cart_form(request, cart_item_id):
    """Remove item from cart via form submission"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('cart:cart_detail')


def update_cart_form(request):
    """Update cart quantities via form submission"""
    cart = get_or_create_cart(request)
    
    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            cart_item_id = key.split('_')[1]
            quantity = int(value)
            
            try:
                cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
            except CartItem.DoesNotExist:
                continue
    
    messages.success(request, 'Cart updated successfully!')
    return redirect('cart:cart_detail')
