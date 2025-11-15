from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.AccountListView.as_view(), name='account_list'),
    path('accounts/add/', views.AccountCreateView.as_view(), name='account_create'),
    path('accounts/edit/<int:pk>/', views.AccountUpdateView.as_view(), name='account_update'),
    path('accounts/delete/<int:pk>/', views.AccountDeleteView.as_view(), name='account_delete'),
]
