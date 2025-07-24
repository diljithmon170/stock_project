
# Create your views here.
from django.shortcuts import render, redirect
from .models import Product, StockTransaction, StockDetail
from django.forms import modelform_factory, inlineformset_factory

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
            return redirect('transaction_list')
    else:
        form = StockTransactionForm()
        formset = StockDetailFormSet()
    return render(request, 'inventory/add_transaction.html', {'form': form, 'formset': formset})
