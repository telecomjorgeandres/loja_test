from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('new/', views.product_create, name='product_create'),
     # NEW: URL for showing products listed by the current logged-in user
    path('my-products/', views.my_products, name='my_products'),
    # NEW: URL for editing an existing product
    path('<int:pk>/edit/', views.product_update, name='product_update'),
    # NEW: URL for deleting a product
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    ]
