from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # quantity = models.PositiveIntegerField()
    description = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
