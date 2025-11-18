from django import forms
from datetime import date
from .models import Account, Transaction, Category, Budget


# -- Account Form -- #
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Cash, Bank, etc.'}),
            'balance': forms.NumberInput(attrs={'placeholder': '0.00'})
        }

    def clean_balance(self):
        balance = self.cleaned_data.get('balance')
        if balance is not None and balance < 0:
            raise forms.ValidationError("Initial balance cannot be negative.")
        return balance


# -- Transaction Form -- #
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'category', 'amount', 'description', 'date']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Grocery shopping, Salary, etc.'}),
            'amount': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['account'].queryset = Account.objects.filter(user=user)

        self.fields['category'].queryset = Category.objects.all().order_by('name')


# -- Budget Form -- #

MONTH_CHOICES = [
    (1, 'January'), (2, 'February'), (3, 'March'),
    (4, 'April'), (5, 'May'), (6, 'June'),
    (7, 'July'), (8, 'August'), (9, 'September'),
    (10, 'October'), (11, 'November'), (12, 'December')
]

YEAR_CHOICES = [(year, year) for year in range(date.today().year, date.today().year + 6)]


class BudgetForm(forms.ModelForm):
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        initial=date.today().month,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        initial=date.today().year,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Budget
        fields = ['category', 'limit_amount', 'month', 'year']
        widgets = {
            'limit_amount': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01', 'min': '0'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.filter(type='E').order_by('name')
        self.fields['limit_amount'].widget.attrs.update({'class': 'form-control'})
        if user:
            self.initial['user'] = user

    def clean(self):
        cleaned_data = super().clean()

        if self.instance.pk is None or self.has_changed():
            user = self.initial.get('user')
            category = cleaned_data.get('category')
            month = int(cleaned_data.get('month'))
            year = int(cleaned_data.get('year'))

            if user and category and month and year:
                queryset = Budget.objects.filter(
                    user=user,
                    category=category,
                    month=month,
                    year=year
                )

                if self.instance.pk:
                    queryset = queryset.exclude(pk=self.instance.pk)

                if queryset.exists():
                    raise forms.ValidationError(
                        f"A budget for {category.name} already exists for {month}/{year}. Please edit the existing budget."
                    )
        return cleaned_data
