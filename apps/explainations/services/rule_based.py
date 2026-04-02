""" 
For the fallback purpose

"""

def generate_rule_based_explaination(transaction, risk_level, fraud_prob):

    amount = float(transaction.amount)

    if risk_level == "HIGH":
        if amount > 50000:
            return "Transaction flagged due to unusually high amount."
        return "Transaction flagged due to suspicious activity pattern."

    elif risk_level == "MEDIUM":
        return "Transaction shows some unusual patterns and requires review."

    return "Transaction appears normal with low fraud risk."