from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('clear/', views.clear_cart, name='clear_cart'),
    
    # AJAX endpoints
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart, name='update_cart'),
    
    # Form-based endpoints (fallback)
    path('add-form/<int:product_id>/', views.add_to_cart_form, name='add_to_cart_form'),
    path('remove-form/<int:cart_item_id>/', views.remove_from_cart_form, name='remove_from_cart_form'),
    path('update-form/', views.update_cart_form, name='update_cart_form'),
]