from django import forms
from .models import Account, Transaction, Category


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
