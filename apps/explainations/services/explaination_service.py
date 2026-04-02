from apps.explainations.llm_client import generate_llama_explaination
from apps.explainations.services.rule_based import generate_rule_based_explaination

def build_explaination(transaction, fraud_prob, risk_level, decision):
    prompt = f"""
    A financial transaction has been analyzed for fraud.

    Details:
    - Amount: {transaction.amount}
    - Location: {transaction.location}
    - Device: {transaction.device}
    - Fraud Probability: {fraud_prob:.2f}
    - Risk Level: {risk_level}
    - Decision: {decision}

    Explain in 1 short sentence why this decision was made.
    """

    # LLaMA explaination
    explaination = generate_llama_explaination(prompt)

    if explaination:
        print("[LLAMA EXPLAINATION GENERATED]")
        return explaination
    
    # Fallback
    fallback_explaination = generate_rule_based_explaination(transaction, risk_level, fraud_prob)
    print("[RULE-BASED EXPLAINATION GENERATED]")
    return fallback_explaination
