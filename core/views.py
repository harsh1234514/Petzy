from django.shortcuts import render
from products.models import Product, Category


def home(request):
    """Homepage view with featured products and categories"""
    featured_products = Product.objects.filter(
        featured=True, 
        is_active=True
    ).select_related('category')[:8]
    
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    
    return render(request, 'core/home.html', context)
