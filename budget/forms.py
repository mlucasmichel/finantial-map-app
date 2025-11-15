from django import forms
from .models import Account

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