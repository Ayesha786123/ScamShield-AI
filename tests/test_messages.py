from src.predict import predict_message


TEST_MESSAGES = [

    # SCAMS
    (
        "Your SBI account will be blocked today. "
        "Verify your account immediately using "
        "https://example.com",
        1
    ),

    (
        "Congratulations! You have won Rs 5,00,000 "
        "in our lottery. Pay the registration fee "
        "to claim your prize.",
        1
    ),

    (
        "Your bank account has been suspended. "
        "Share the OTP immediately to reactivate it.",
        1
    ),

    (
        "Your KYC has expired. Update your banking "
        "details now or your account will be blocked.",
        1
    ),

    (
        "You have received a cashback reward. "
        "Click here and enter your card number "
        "and CVV to claim it.",
        1
    ),

    (
        "Your parcel is waiting for delivery. "
        "Pay the processing fee immediately using "
        "https://example.com",
        1
    ),

    (
        "Congratulations! You have been selected "
        "for a work from home job. Pay a registration "
        "fee to receive your salary.",
        1
    ),

    (
        "This is the bank security department. "
        "Tell me the OTP you just received to prevent "
        "your account from being blocked.",
        1
    ),

    # LEGITIMATE
    (
        "Your monthly bank statement is now available "
        "in your official banking application.",
        0
    ),

    (
        "Your order has been shipped and will arrive "
        "tomorrow.",
        0
    ),

    (
        "Your appointment is scheduled for tomorrow "
        "at 10 AM.",
        0
    ),

    (
        "Thank you for your payment. Your transaction "
        "was successful.",
        0
    ),

    (
        "Your electricity bill of Rs 850 is due on "
        "25 August.",
        0
    ),

    (
        "Your flight booking has been confirmed. "
        "Your ticket is available in the airline app.",
        0
    ),

    (
        "Your monthly salary has been credited to "
        "your bank account.",
        0
    ),

    (
        "Reminder: your college examination starts "
        "tomorrow at 9 AM.",
        0
    )
]


def main():

    total = len(TEST_MESSAGES)
    correct = 0
    false_negatives = 0
    false_positives = 0

    print("=" * 70)
    print("SCAMSHIELD AI TEST")
    print("=" * 70)

    for message, actual in TEST_MESSAGES:

        result = predict_message(message)

        predicted = (
            1
            if result["risk_level"] in ["HIGH", "CRITICAL"] or result.get("prediction") == "SCAM"
            else 0
        )

        if predicted == actual:
            correct += 1

        elif actual == 1:
            false_negatives += 1

        else:
            false_positives += 1

        print("\n" + "-" * 70)

        print("Message:")
        print(message)

        print(
            "\nActual:",
            "SCAM" if actual else "LEGITIMATE"
        )

        print(
            "Predicted:",
            "SCAM" if predicted else "LEGITIMATE"
        )

        print(
            "Risk:",
            result["risk_score"]
        )

        print(
            "Level:",
            result["risk_level"]
        )

        print(
            "Type:",
            result["scam_type"]
        )

    accuracy = (correct / total) * 100

    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    print("Total:", total)
    print("Correct:", correct)
    print("Accuracy:", f"{accuracy:.2f}%")
    print("False Negatives:", false_negatives)
    print("False Positives:", false_positives)


if __name__ == "__main__":
    main()