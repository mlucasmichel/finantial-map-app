from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Account, Transaction, Budget
from .forms import AccountForm, TransactionForm, BudgetForm

# Create your views here.


# -- (Account Views Start) -- #
# -- Account List View -- #
class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'budget/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).order_by('name')


# -- Account Create View -- #
class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'budget/account_form.html'
    success_url = reverse_lazy('account_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# -- Account Delete View -- #
class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'budget/account_confirm_delete.html'
    success_url = reverse_lazy('account_list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


# -- Account Update View -- #
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'budget/account_form.html'
    success_url = reverse_lazy('account_list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# -- (Account Views End) -- #


# -- (Transaction Views Start) -- #
# -- Transaction List View -- #
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'budget/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date')


# -- Transaction Create View -- #
class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# -- Transaction Update View -- #
class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


# -- Transaction Delete View -- #
class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'budget/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

# -- (Transaction Views End) -- #


# -- (Budget Views Start) -- #
# -- Budget List View -- #
class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budget/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).order_by('-year', '-month', 'category__name')


# -- Budget Create View -- #
class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget/budget_form.html'
    success_url = reverse_lazy('budget_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# -- Budget Update View -- #
class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget/budget_form.html'
    success_url = reverse_lazy('budget_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


# -- Budget Delete View -- #
class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'budget/budget_confirm_delete.html'
    success_url = reverse_lazy('budget_list')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

# -- (Budget Views End) -- #
