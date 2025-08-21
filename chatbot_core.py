# chatbot_core.py
# here I handle the NLP logic for the FAQ chatbot and fallback messages

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# make sure nltk resources are downloaded safely
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

# get list of common English stopwords to ignore
STOPWORDS = set(stopwords.words("english"))

def normalize(text: str) -> set:
    """clean text: lowercase, tokenize, remove stopwords & non-alpha tokens"""
    tokens = [t.lower() for t in word_tokenize(text)]  # split text into words
    return {t for t in tokens if t.isalpha() and t not in STOPWORDS}  # only keep meaningful words

def jaccard(a: set, b: set) -> float:
    """calculate similarity between two sets of words"""
    if not a and not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))  # intersection / union

# --- FAQ knowledge base ---
FAQ_KB = [
    ("hello", "Hello! How can I help you today?"),
    ("hi", "Hello! How can I help you today?"),
    ("hey", "Hello! How can I help you today?"),
    ("support hours", "Our support team is available 24/7 to assist you."),
    ("reset password", "To reset your password, go to Settings > Security > Reset Password with you Credentials."),
    ("contact support", "You can contact support at support@example.com or contact +91 xxxxx xxxxx for your querry."),
    ("Refund policy", "Our refund policy allows refunds within 30 days of purchase *My Orders > Help > raise a Refund querry or Contact Support."),
    ("Return policy", "Our return policy allows return within 07 days of purchase *My Orders > Help > raise a Return querry or Contact Support."),
    ("update profile", "To update your profile, go to Settings > Profile and make changes."),
    ("orders", "You can view your orders in the 'My Orders' section of your account."),
    ("goodbye", "Goodbye! Have a great day."),
    ("bye", "Goodbye! Have a great day."),
]

# prepare normalized questions once to speed up matching
KB = [(normalize(q), ans) for q, ans in FAQ_KB]

# fallback message if bot can't understand user
FALLBACK_MESSAGE = (
    "I couldn’t understand that. Please choose one of the options below:\n\n"
    "➡️ Support hours\n"
    "➡️ Reset password\n"
    "➡️ Contact support\n"
    "➡️ Refund policy\n"
    "➡️ Update profile\n"
    "➡️ Orders"
)

def faq_match(user_text: str, threshold: float = 0.3) -> str | None:
    """try to find best match from FAQ using Jaccard similarity"""
    user_norm = normalize(user_text)
    best_score, best_answer = 0.0, None

    for qset, ans in KB:
        score = jaccard(user_norm, qset)  # compare user input with FAQ question
        if score > best_score:
            best_score, best_answer = score, ans  # keep best match

    return best_answer if best_score >= threshold else None  # return if good enough

def get_response(user_message: str) -> str:
    """
    main function to get bot reply:
    1) check FAQ match
    2) if no match, return fallback message
    """
    if not user_message or not user_message.strip():
        return "⚠️ Please type a message."  # handle empty input

    kb_ans = faq_match(user_message, threshold=0.3)
    return kb_ans if kb_ans else FALLBACK_MESSAGE  # return answer or fallback
