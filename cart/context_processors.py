from .models import Cart


def cart_context(request):
    """Add cart information to template context"""
    cart = None
    total_items = 0
    total_price = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            total_items = cart.total_items
            total_price = cart.total_price
        except Cart.DoesNotExist:
            pass
    else:
        # Handle session-based cart for anonymous users
        if request.session.session_key:
            try:
                cart = Cart.objects.get(session_key=request.session.session_key)
                total_items = cart.total_items
                total_price = cart.total_price
            except Cart.DoesNotExist:
                pass
    
    return {
        'cart': cart,
        'cart_total_items': total_items,
        'cart_total_price': total_price,
    }