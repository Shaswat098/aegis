from django.urls import path
from apps.transactions.api.views import TransactionCreateAPIView

urlpatterns = [
    path('transactions/', TransactionCreateAPIView.as_view(), name='transaction-create'),
]