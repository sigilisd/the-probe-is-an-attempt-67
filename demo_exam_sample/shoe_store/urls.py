from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('products/', views.products_list, name='products_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('orders/', views.orders_list, name='orders_list'),
]