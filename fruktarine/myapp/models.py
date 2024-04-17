from django.db import models
from django.core.validators import RegexValidator


class Product(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(default='', blank=True)
    price = models.FloatField(default=999.99, max_digits=7, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True)
    rating = models.DecimalField(default=5.0, max_digits=3, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Order(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$", max_length=13, unique=True)
    address = models.CharField(max_length=200)
    delivery_date = models.DateField()
    total_price = models.FloatField(max_digits=8, decimal_places=2)
    comment = models.TextField(max_length=300)

    def __str__(self):
        return f'Order #{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_per_product = models.FloatField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Order #{self.order.id} - {self.product.name} ({self.quantity})'
