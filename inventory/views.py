# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, StockTransaction, StockDetail
from django.forms import modelform_factory, inlineformset_factory
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

# Product Form
ProductForm = modelform_factory(Product, exclude=[])

# Stock Forms
StockTransactionForm = modelform_factory(StockTransaction, exclude=[])
StockDetailFormSet = inlineformset_factory(
    StockTransaction, StockDetail, fields=('product', 'quantity', 'rate'), extra=1
)

def home(request):
    return render(request, 'inventory/home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})

def transaction_list(request):
    transactions = StockTransaction.objects.all()
    return render(request, 'inventory/transaction_list.html', {'transactions': transactions})

def add_transaction(request):
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        formset = StockDetailFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            transaction = form.save()
            details = formset.save(commit=False)
            for detail in details:
                detail.transaction = transaction
                detail.save()
                # Update product stock based on transaction type
                product = detail.product
                if transaction.transaction_type == 'IN':
                    product.stock += detail.quantity
                elif transaction.transaction_type == 'OUT':
                    product.stock -= detail.quantity
                product.save()
            return redirect('transaction_list')
    else:
        form = StockTransactionForm()
        formset = StockDetailFormSet()
    return render(request, 'inventory/add_transaction.html', {'form': form, 'formset': formset})

def transaction_detail(request, pk):
    transaction = get_object_or_404(StockTransaction, pk=pk)
    details = StockDetail.objects.filter(transaction=transaction)
    return render(request, 'inventory/transaction_detail.html', {
        'transaction': transaction,
        'details': details
    })

def edit_transaction(request, pk):
    transaction = get_object_or_404(StockTransaction, pk=pk)
    if request.method == 'POST':
        form = StockTransactionForm(request.POST, instance=transaction)
        formset = StockDetailFormSet(request.POST, instance=transaction)
        if form.is_valid() and formset.is_valid():
            # Revert stock changes for old details
            old_details = StockDetail.objects.filter(transaction=transaction)
            for old_detail in old_details:
                product = old_detail.product
                if transaction.transaction_type == 'IN':
                    product.stock -= old_detail.quantity
                elif transaction.transaction_type == 'OUT':
                    product.stock += old_detail.quantity
                product.save()
            form.save()
            formset.save()
            # Apply stock changes for new details
            new_details = StockDetail.objects.filter(transaction=transaction)
            for new_detail in new_details:
                product = new_detail.product
                if transaction.transaction_type == 'IN':
                    product.stock += new_detail.quantity
                elif transaction.transaction_type == 'OUT':
                    product.stock -= new_detail.quantity
                product.save()
            return redirect('transaction_list')
    else:
        form = StockTransactionForm(instance=transaction)
        formset = StockDetailFormSet(instance=transaction)
    return render(request, 'inventory/edit_transaction.html', {'form': form, 'formset': formset})

# Product Edit
class ProductEditView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        messages.success(self.request, "Product updated successfully!")
        return super().form_valid(form)

# Product Delete
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Product deleted successfully!")
        return super().delete(request, *args, **kwargs)

# Transaction Edit
class TransactionEditView(UpdateView):
    model = StockTransaction
    form_class = StockTransactionForm
    template_name = 'inventory/add_transaction.html'
    success_url = reverse_lazy('transaction_list')

    def form_valid(self, form):
        messages.success(self.request, "Transaction updated successfully!")
        return super().form_valid(form)

# Transaction Delete
class TransactionDeleteView(DeleteView):
    model = StockTransaction
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Transaction deleted successfully!")
        return super().delete(request, *args, **kwargs)
