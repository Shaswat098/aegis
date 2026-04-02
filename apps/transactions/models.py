from django.db import models
from django.utils import timezone
from apps.users.models import User

class Transaction(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSED", "Processed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=255)
    device = models.CharField(max_length=100)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    # For idempotency
    external_id = models.CharField(max_length=255, unique=True)

    # For faster queries
    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["status"]),
            models.Index(fields=["user", "timestamp"]), 
        ]

    def __str__(self):
        return f"{self.user_id} - {self.amount}"
    

class RiskAssessment(models.Model):

    RISK_LEVELS = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    DECISION_CHOICES = [
        ("APPROVE", "Approve"),
        ("FLAG", "Flag"),
        ("BLOCK", "Block"),
    ]

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="risk"
    )

    fraud_probability = models.FloatField()
    risk_score = models.FloatField(default=0.0)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)

    decision = models.CharField(max_length=20, choices=DECISION_CHOICES)

    explaination = models.TextField()

    model_version = models.CharField(max_length=50)

    evaluated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["risk_level"]),
            models.Index(fields=["decision"]),
        ]

class AuditLog(models.Model):
    
    ACTION_cHOICES = [
        ("CREATED","Created"),
        ("UPDATED","Updated"),
        ("PROCESSED","Processed"),
    ]

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    action = models.CharField(max_length=20, choices=ACTION_cHOICES)

    metadata = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)


class TransactionFeature(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)

    features = models.JSONField()