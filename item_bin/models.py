from random import choices

from django.db import models
from django.template.defaultfilters import default


class Item(models.Model):
    CURRENCY_CHOICES = (
        ('usd', 'US Dollar'),
        ('eur', 'Euro'),
    )

    name = models.CharField(max_length=40, verbose_name='Name')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Item price')
    quantity = models.PositiveIntegerField(verbose_name='Quantity', default=1)
    description = models.TextField(verbose_name='Description of item')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd', verbose_name='Currency')

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name='items')
    user = models.CharField(max_length=40, verbose_name='User')

    def __str__(self):
        return self.user

    objects = models.Manager()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Discount(models.Model):
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Discount in percents.')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Order')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return str(self.order)


class Tax(models.Model):
    tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tax in percents.')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Order')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Taxes'

    def __str__(self):
        return str(self.order)
