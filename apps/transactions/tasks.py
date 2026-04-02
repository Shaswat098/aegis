from celery import shared_task
from apps.ml.encoders.location_encoder import encode_location
from apps.transactions.models import Transaction, RiskAssessment, AuditLog
from apps.ml.inference import predict 
from apps.risk_engine.services.risk_service import calculate_risk
from apps.explainations.tasks import generate_explaination_task

@shared_task(bind = True,
             autoretry_for = (Exception,),
             retry_backoff = 5,
             max_retries = 3,
             )

def process_transaction_task(self,transaction_id: int):
    """
    Async task to 
      - call ML model
      - calculate risk
      - call LLM
    """
    try:
        transaction = Transaction.objects.get(id=transaction_id)

        features = {
            "amount": float(transaction.amount),
            "location": transaction.location,
            "device" : transaction.device,
        }

        if hasattr(transaction, "risk"):
            return


        # ML prediction
        fraud_prob = predict(features)

        # Risk scoring
        risk_score, risk_level, decision = calculate_risk(fraud_prob)

        risk = RiskAssessment.objects.create(
                transaction=transaction,
                fraud_probability=fraud_prob,
                risk_score=risk_score,
                risk_level=risk_level,
                decision=decision,
                explaination="Generating...",
                model_version="v1.0"
        )

        generate_explaination_task.delay(risk.id)

        # Update transaction

        transaction.status = "PROCESSED",
        transaction.save()

        # Audit log
        AuditLog.objects.create(
            transaction=transaction,
            action="PROCESSED",
            metadata = {
                "fraud_probability": fraud_prob,
                "risk_score": risk_score,
                "decision": decision
            }
        )
      
    except Exception as e:
        raise self.retry(exc=e)

