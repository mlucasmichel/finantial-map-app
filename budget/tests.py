from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal
from budget.models import Account, Category, Transaction

User = get_user_model()


class TransactionSignalTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.income_category = Category.objects.create(name='Salary', type='I')
        self.expense_category = Category.objects.create(name='Groceries', type='E')
        self.account1 = Account.objects.create(user=self.user, name='Checking', balance=Decimal('100.00'))
        self.account2 = Account.objects.create(user=self.user, name='Savings', balance=Decimal('500.00'))

    def test_create_expense_transaction_updates_balance(self):
        # Initial balance
        self.assertEqual(self.account1.balance, Decimal('100.00'))

        # Create expense transaction
        Transaction.objects.create(
            user=self.user,
            account=self.account1,
            category=self.expense_category,
            amount=Decimal('25.00'),
            date='2025-01-01',
            description='Weekly groceries'
        )
        # Refresh account balance from DB
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('75.00'))

    def test_create_income_transaction_updates_balance(self):
        # Initial balance
        self.assertEqual(self.account1.balance, Decimal('100.00'))

        # Create income transaction
        Transaction.objects.create(
            user=self.user,
            account=self.account1,
            category=self.income_category,
            amount=Decimal('150.00'),
            date='2025-01-05',
            description='Monthly salary'
        )
        # Refresh account balance from DB
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('250.00'))
    
    def test_delete_expense_transaction_reverts_balance(self):
        # create expense transaction
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account1,
            category=self.expense_category,
            amount=Decimal('30.00'),
            date='2025-01-10',
            description='Dinner out'
        )
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('70.00'))

        # delete transaction
        transaction.delete()
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('100.00'))

    def test_delete_income_transaction_reverts_balance(self):
        # create income transaction
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account1,
            category=self.income_category,
            amount=Decimal('80.00'),
            date='2025-01-12',
            description='Freelance work'
        )
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('180.00'))

        # delete transaction
        transaction.delete()
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('100.00'))

    def test_update_transaction_amount_correctly_changes_balance(self):
        # create initial transaction
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account1,
            category=self.expense_category,
            amount=Decimal('20.00'),
            date='2025-01-15',
            description='Snacks'
        )
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('80.00'))

        # update transaction amount
        transaction.amount = Decimal('50.00')
        transaction.save()
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('50.00'))

    def test_update_transaction_account_correctly_updates_balances(self):
        # create initial transaction in account1
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account1,
            category=self.expense_category,
            amount=Decimal('20.00'),
            date='2025-01-15',
            description='Transfer'
        )
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('80.00'))
        self.assertEqual(self.account2.balance, Decimal('500.00'))

        # update transaction to account2
        transaction.account = self.account2
        transaction.save()
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('100.00'))
        self.assertEqual(self.account2.balance, Decimal('480.00'))

    def test_update_transaction_type_correctly_updates_balance(self):
        # create initial expense transaction
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account1,
            category=self.expense_category,
            amount=Decimal('50.00'),
            date='2025-01-20',
            description='Clothes'
        )
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('50.00'))

        # change transaction to income type (to simulate a refund)
        transaction.category = self.income_category
        transaction.save()
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, Decimal('150.00'))
    

class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
    def test_dashboard_view_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse('account_login') in response.url)

    def test_dashboard_view_loads_for_logged_in_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/dashboard.html')
    
    def test_transaction_create_view_loads(self):
        response = self.client.get(reverse('transaction_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/transaction_form.html')
