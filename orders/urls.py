from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<uuid:order_id>/', views.order_detail, name='order_detail'),
]