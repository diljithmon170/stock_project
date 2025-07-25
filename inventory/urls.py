from django.urls import path
from . import views
from .views import (
    ProductEditView, ProductDeleteView,
    TransactionEditView, TransactionDeleteView,
    transaction_detail,
    # ...other views...
)

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('product/<int:pk>/edit/', ProductEditView.as_view(), name='edit_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('transaction/<int:pk>/edit/', TransactionEditView.as_view(), name='edit_transaction'),
    path('transaction/<int:pk>/delete/', TransactionDeleteView.as_view(), name='delete_transaction'),
    path('transaction/<int:pk>/', transaction_detail, name='transaction_detail'),
]
