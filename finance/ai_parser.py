import re

from rapidfuzz import process

from .models import Category


EXPENSE_WORDS = [
    "spent",
    "pay",
    "paid",
    "bought",
    "purchase",
]

INCOME_WORDS = [
    "salary",
    "received",
    "income",
    "got",
    "earned",

]


CATEGORY_KEYWORDS = {
    "Food": [
        "food",
        "rice",
        "biriyani",
        "hotel",
        "tea",
        "juice",
        "coffee",
    ],

    "Fuel": [
        "petrol",
    ],

    "Travel": [
        "bus",
        "train",
        "flight",
        "travel",
    ],


    "Shopping": [
        "dress",
        "shirt",
        "shoe",
        "shopping",
    ],

    "Catering": [
        "catering", 
        "event",
    ],
}


def detect_amount(text):

    match = re.search(r'\d+', text)

    if match:
        return float(match.group())

    return 0


def detect_type(text):

    text = text.lower()

    for word in EXPENSE_WORDS:

        if word in text:
            return "expense"

    for word in INCOME_WORDS:

        if word in text:
            return "income"

    return "expense"


def detect_category(user, text):

    categories = Category.objects.filter(
        user=user
    )

    if not categories.exists():
        return None

    text = text.lower()

    # keyword match
    for category_name, keywords in CATEGORY_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:

                matched = categories.filter(
                    name__iexact=category_name
                ).first()

                if matched:
                    return matched

    # fuzzy fallback
    category_names = list(
        categories.values_list("name", flat=True)
    )

    result = process.extractOne(
        text,
        category_names,
    )

    if result and result[1] > 60:

        matched_name = result[0]

        return categories.filter(
            name=matched_name
        ).first()

    return categories.filter(
        name__iexact="Other"
    ).first()


def parse_transaction_text(user, text):

    amount = detect_amount(text)

    transaction_type = detect_type(text)

    category = detect_category(user, text)

    return {
        "amount": amount,
        "type": transaction_type,
        "category": category.id if category else None,
        "category_name": category.name if category else "Other",
        "note": text,
    }