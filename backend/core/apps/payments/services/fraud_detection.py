def evaluate_payment(payment):
    """
    Simulated fraud detection rules
    """

    # Rule 1 — High amount transactions
    if payment.amount > 100000:
        return True

    # Rule 2 — unsupported currency
    if payment.currency not in ["INR", "USD"]:
        return True

    return False