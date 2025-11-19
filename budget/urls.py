from django.urls import path
from . import views

urlpatterns = [
    # -- Account URLs -- #
    path('accounts/', views.AccountListView.as_view(), name='account_list'),
    path('accounts/add/', views.AccountCreateView.as_view(), name='account_create'),
    path('accounts/edit/<int:pk>/', views.AccountUpdateView.as_view(), name='account_update'),
    path('accounts/delete/<int:pk>/', views.AccountDeleteView.as_view(), name='account_delete'),

    # -- Transaction URLs -- #
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/edit/<int:pk>/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/delete/<int:pk>/', views.TransactionDeleteView.as_view(), name='transaction_delete'),

    # -- Budget URLs -- #
    path('budgets/', views.BudgetListView.as_view(), name='budget_list'),
    path('budgets/add/', views.BudgetCreateView.as_view(), name='budget_create'),
    path('budgets/edit/<int:pk>/', views.BudgetUpdateView.as_view(), name='budget_update'),
    path('budgets/delete/<int:pk>/', views.BudgetDeleteView.as_view(), name='budget_delete'),
]
