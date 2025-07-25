from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
from django.db import models

class Product(models.Model):  # prodmast
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )  # Ensure price is always positive
    stock = models.IntegerField(default=0)  # New field to track stock quantity

    def __str__(self):
        return self.name


class StockTransaction(models.Model):  # stckmain
    TRANSACTION_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} on {self.date}"


class StockDetail(models.Model):  # stckdetail
    transaction = models.ForeignKey(StockTransaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Always positive
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )  # Always positive

    def __str__(self):
        return f"{self.product.name} x {self.quantity} @ {self.rate}"
