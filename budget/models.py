from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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
        return f"{self.name} - ({self.get_type_display()})"
    

# -- Account Model -- #
class Account(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    name = models.CharField(
        max_length=50,
        null=False
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - ({self.user.username})"