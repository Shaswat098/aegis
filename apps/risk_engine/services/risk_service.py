def calculate_risk(probability : float):
    """
    Converts the output of ML Model to business friendly decision
    """

    score = int(probability * 100)

    if score < 30:
        return score, "LOW", "APPROVE"
    elif score < 70:
        return score, "MEDIUM", "FLAG"
    else:
        return score, "HIGH", "BLOCK"