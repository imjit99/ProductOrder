from django.db import models
from django.contrib.auth.models import User
import uuid

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Itemorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    special_instruction = models.TextField(blank=True, null=True)
    order_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # class Meta:
    #     unique_together = ('user', 'product', 'order_date')

    def save(self, *args, **kwargs):
        # Automatically calculate and set total_price before saving
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} by {self.user}"
