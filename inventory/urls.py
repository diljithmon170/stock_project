from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
]
