from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Account
from .forms import AccountForm

# Create your views here.


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
