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


# -- Transaction Model -- #
class Transaction(models.Model):
    # -- Foreign Keys -- #
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    # -- Fields -- #
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
    )

    date = models.DateField(
        null=False
    )

    description = models.TextField(
        max_length=255,
        null=False,
        blank=False
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.description} - {self.amount} on {self.date} ({self.user.username})"


# -- Budget Model -- #
class Budget(models.Model):
    # -- Foreign Keys -- #
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='budgets'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='budgets'
    )

    # -- Fields -- #
    limit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0.00
    )

    month = models.IntegerField(
        null=False
        )
    year = models.IntegerField(
        null=False
        )

    class Meta:
        unique_together = ('user', 'category', 'month', 'year')
        ordering = ['-year', '-month', 'category__name']

    def __str__(self):
        return f"Budget for {self.category.name} - {self.month}/{self.year} ({self.user.username})"
