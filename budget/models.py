from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# -- Category Model -- #
class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('I', 'Income'),
        ('E', 'Expense'),
    ]

    name = models.CharField(
        max_length=50,
        unique=True,
        null=False
    )

    type = models.CharField(
        max_length=1,
        choices=CATEGORY_TYPE_CHOICES,
        default='E',
        null=False
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
