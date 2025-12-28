from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Transaction

# -- pre_save signal to revert the old amount before updating a Transaction -- #
@receiver(pre_save, sender=Transaction)
def revert_old_amount_on_update(sender, instance, **kwargs):
    """
    Before a transaction is updated, revert the old amount from the associated account.
    """
    if instance.pk:
        try:
            # Get the state of the transaction before the update
            old_transaction = Transaction.objects.get(pk=instance.pk)
            old_account = old_transaction.account

            # Revert the old amount from the account balance
            if old_transaction.category.type == 'I':
                old_account.balance -= old_transaction.amount
            else:
                old_account.balance += old_transaction.amount

            old_account.save()
        
        except Transaction.DoesNotExist:
            pass  # Transaction is new, no need to revert anything


# -- post_save signal to update account balance -- #
@receiver(post_save, sender=Transaction)
def update_account_balance_on_save(sender, instance, created, **kwargs):
    """
    Update the account balance when a transaction is created or updated.
    """
    new_account = instance.account

    # apply the new amount to the account balance
    if instance.category.type == 'I':
        new_account.balance += instance.amount
    else:
        new_account.balance -= instance.amount

    new_account.save()


# -- post_delete signal to update account balance -- #
@receiver(post_delete, sender=Transaction)
def update_account_balance_on_delete(sender, instance, **kwargs):
    """
    Update the account balance when a transaction is deleted.
    """
    account = instance.account

    # revert the amount from the account balance
    if instance.category.type == 'I':
        account.balance -= instance.amount
    else:
        account.balance += instance.amount

    account.save()
