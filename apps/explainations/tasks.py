from celery import shared_task
from apps.transactions.models import RiskAssessment
from apps.explainations.services.explaination_service import build_explaination


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=10, max_retries=3)
def generate_explaination_task(self, risk_id):
    try:
        risk = RiskAssessment.objects.get(id=risk_id)

        explanation = build_explaination(
            risk.transaction,
            risk.fraud_probability,
            risk.risk_level,
            risk.decision
        )

        risk.explanation = explanation
        risk.save()

    except Exception as e:
        raise self.retry(exc=e)