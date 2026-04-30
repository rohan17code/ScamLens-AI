def rule_based_check(text):
    text_lower = text.lower()

    dangerous_phrases = [
        "send otp",
        "share otp",
        "enter otp",
        "give otp",
        "provide otp",

        "send password",
        "share password",
        "enter password",
        "provide password",

        "upi pin",
        "atm pin",
        "cvv",
        "card number",
        "bank details",

        "transfer money",
        "send money",
        "pay now",
        "payment required",
        "processing fee"
    ]

    for phrase in dangerous_phrases:
        if phrase in text_lower:
            return (
                "Risk Level: High\n"
                "Reason: This content asks for sensitive information or money, so details should not be shared."
            )

    return None