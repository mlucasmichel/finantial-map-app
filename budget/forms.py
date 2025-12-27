from django import forms
from datetime import date
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm, ResetPasswordForm, SetPasswordForm
from .models import Account, Transaction, Category, Budget


# -- Custom Signup Form for Allauth -- #
class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-field'
        self.fields['email'].widget.attrs['class'] = 'form-field'
        self.fields['password1'].widget.attrs['class'] = 'form-field'
        self.fields['password2'].widget.attrs['class'] = 'form-field'


# -- Custom Login Form for Allauth -- #
class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        self.fields['login'].widget.attrs['class'] = 'form-field'
        self.fields['password'].widget.attrs['class'] = 'form-field'
        self.fields['remember'].widget.attrs['class'] = 'form-checkbox'


# -- Custom Password Change Form for Allauth -- #
class CustomPasswordChangeForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-field'


# -- Custom Password Reset Form for Allauth -- #
class CustomPasswordResetForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-field'


# -- Custom Set Password Form for Allauth -- #
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)

        self.fields['password'].widget.attrs['class'] = 'form-field'
        self.fields['password2'].widget.attrs['class'] = 'form-field'


# -- Account Form -- #
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Cash, Bank, etc.'}),
            'balance': forms.NumberInput(attrs={'placeholder': '0.00'})
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name) < 3:
            raise forms.ValidationError(
                "Account name must be at least 3 characters long.")
        return name

    def clean_balance(self):
        balance = self.cleaned_data.get('balance')
        if balance is not None and balance < 0:
            raise forms.ValidationError("Initial balance cannot be negative.")
        return balance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-field'})
        self.fields['balance'].widget.attrs.update({'class': 'form-field'})


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

        self.fields['category'].queryset = Category.objects.all().order_by(
            'name')

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-field'})


# -- Transaction Filter Form -- #
class TransactionFilterForm(forms.Form):
    accounts = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        required=False,
        label='Accounts',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    categories = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        label='Categories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    start_date = forms.DateField(
        required=False,
        label='Start Date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-field'})
    )
    end_date = forms.DateField(
        required=False,
        label='End Date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-field'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['accounts'].queryset = Account.objects.filter(
                user=user).order_by('name')
            self.fields['categories'].queryset = Category.objects.all().order_by(
                'name')


# -- Budget Form -- #
MONTH_CHOICES = [
    (1, 'January'), (2, 'February'), (3, 'March'),
    (4, 'April'), (5, 'May'), (6, 'June'),
    (7, 'July'), (8, 'August'), (9, 'September'),
    (10, 'October'), (11, 'November'), (12, 'December')
]

YEAR_CHOICES = [(year, year)
                for year in range(date.today().year, date.today().year + 6)]


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
            'limit_amount': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01', 'min': '0', 'class': 'form-field'}),
            'category': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.filter(
            type='E').order_by('name')

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
