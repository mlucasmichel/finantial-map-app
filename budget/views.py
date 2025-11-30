from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Sum
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from calendar import month_name

from .models import Account, Transaction, Budget
from .forms import AccountForm, TransactionFilterForm, TransactionForm, BudgetForm

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
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TransactionFilterForm(
            self.request.GET,
            user=self.request.user
            )
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(user=user).select_related('account', 'category').order_by('-date')

        form = TransactionFilterForm(self.request.GET, user=user)

        if form.is_valid():
            accounts = form.cleaned_data.get('accounts')
            categories = form.cleaned_data.get('categories')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            if accounts:
                queryset = queryset.filter(account__in=accounts)
            
            if categories:
                queryset = queryset.filter(category__in=categories)
            
            if start_date and end_date:
                queryset = queryset.filter(date__range=(start_date, end_date))
            elif start_date:
                queryset =queryset.filter(date__gte=start_date)
            elif end_date:
                queryset =queryset.filter(date__lte=end_date)

        return queryset


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


# -- Dashboard View -- #
class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Template view for the user dashboard.
    """
    template_name = 'budget/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = date.today()

        # -- Current Month and Year -- #
        try:
            selected_month = int(self.request.GET.get('month'))
            selected_year = int(self.request.GET.get('year'))
        except (TypeError, ValueError):
            selected_month = today.month
            selected_year = today.year

        try:
            filter_start_date = date(selected_year, selected_month, 1)
            filter_end_date = filter_start_date + relativedelta(months=1) - timedelta(days=1)
        except ValueError:
            filter_start_date = today.replace(day=1)
            filter_end_date = today

        earliest_transaction = Transaction.objects.filter(user=user).order_by('date').first()
        earliest_year = earliest_transaction.date.year if earliest_transaction else today.year
        available_years = range(today.year, earliest_year - 1, -1)

        context['months'] = [(i, month_name[i]) for i in range(1, 13)]
        context['years'] = list(available_years)
        context['selected_month'] = selected_month
        context['selected_year'] = selected_year
        context['filter_start_date'] = filter_start_date
        context['filter_end_date'] = filter_end_date

        # -- User Accounts -- #
        user_accounts = Account.objects.filter(user=user).order_by('name')
        context['accounts'] = user_accounts

        # -- Total balance across all accounts -- #
        balance_summary = Account.objects.filter(user=user).aggregate(total_balance=Sum('balance'))
        context['total_balance'] = balance_summary['total_balance'] or 0.00

        # -- Transactions and Budgets for the Selected month -- #
        monthly_transactions = Transaction.objects.filter(
            user=user,
            date__range=(filter_start_date, filter_end_date)
        )

        # -- Total spending grouped by category -- #
        spending_by_category = monthly_transactions.filter(
            category__type='E'
        ).values(
            'category__name'
        ).annotate(
            total_spent=Sum('amount')
        ).order_by('category__name')

        context['spending_by_category'] = list(spending_by_category)

        # -- Budgets for the Selected month -- #
        budgets = Budget.objects.filter(
            user=user,
            month=selected_month,
            year=selected_year
        ).select_related('category')

        budget_summary_list = []
        spent_map = {item['category__name']: item['total_spent'] for item in spending_by_category}

        for budget in budgets:
            category_name = budget.category.name
            limit = budget.limit_amount
            spent = spent_map.get(category_name, 0)
            remaining = limit - spent

            percent_used = (spent / limit * 100) if limit > 0 else 0

            budget_summary_list.append({
                'category_name': category_name,
                'limit': limit,
                'spent': spent,
                'remaining': remaining,
                'percent_used': percent_used,
                'status': 'danger' if percent_used > 100 else 'warning' if percent_used > 75 else 'success'
            })

        context['budget_summary_list'] = budget_summary_list

        # -- Calculate balance trend at the start of the selected month -- #
        net_change_since_start = Transaction.objects.filter(
            user=user,
            date__gte=filter_start_date
        ).aggregate(Sum('amount'))['amount__sum'] or 0.00

        start_of_month_balance = context['total_balance'] - net_change_since_start

        # -- Get transactions within the selected month -- #
        transactions_in_period = Transaction.objects.filter(
            user=user,
            date__range=(filter_start_date, filter_end_date)
        ).order_by('date', 'pk').values('date', 'amount')

        # -- Calculate balance for chart -- #
        final_chart_labels = []
        final_chart_data = []
        cumulative_balance = start_of_month_balance
        last_date = None

        final_chart_labels.append(filter_start_date.strftime('%Y-%m-%d'))
        final_chart_data.append(round(cumulative_balance, 2))

        for t in transactions_in_period:
            day_str = t['date'].strftime('%Y-%m-%d')
            cumulative_balance += t['amount']
            final_chart_labels.append(day_str)
            final_chart_data.append(round(cumulative_balance, 2))
            last_date = t['date']

        if not last_date or last_date < filter_end_date:
            final_chart_labels.append(filter_end_date.strftime('%Y-%m-%d'))
            final_chart_data.append(round(cumulative_balance, 2))

        context['chart_labels'] = final_chart_labels
        context['chart_data'] = final_chart_data

        return context
