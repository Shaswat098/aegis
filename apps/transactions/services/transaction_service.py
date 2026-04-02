from apps.transactions.models import Transaction, AuditLog
from apps.transactions.tasks import process_transaction_task
from django.db import transaction as db_transaction

def create_transaction(data:dict) -> Transaction:
    
    # Create transaction
    with db_transaction.atomic():
        transaction, created = Transaction.objects.get_or_create(
            external_id=data['external_id'],
            defaults=data
        )

        if not created:
            return transaction
        # Audit Log
        AuditLog.objects.create(
            transaction=transaction,
            action="CREATED",
            metadata={
                "user_id": transaction.user.id,
                "amount": str(transaction.amount),
                "location": transaction.location,
            }
        )

        # Trigger async proecessing
        process_transaction_task.delay(transaction.id)

        return transaction