from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "category_model.pkl")

# Training data: product name -> category
TRAINING_DATA = [
    # Food & Groceries
    ("milk", "Food & Groceries"), ("bread", "Food & Groceries"), ("eggs", "Food & Groceries"),
    ("cheese", "Food & Groceries"), ("butter", "Food & Groceries"), ("yogurt", "Food & Groceries"),
    ("rice", "Food & Groceries"), ("pasta", "Food & Groceries"), ("flour", "Food & Groceries"),
    ("sugar", "Food & Groceries"), ("salt", "Food & Groceries"), ("oil", "Food & Groceries"),
    ("chicken", "Food & Groceries"), ("beef", "Food & Groceries"), ("fish", "Food & Groceries"),
    ("salmon", "Food & Groceries"), ("shrimp", "Food & Groceries"), ("pork", "Food & Groceries"),
    ("apple", "Food & Groceries"), ("banana", "Food & Groceries"), ("orange", "Food & Groceries"),
    ("tomato", "Food & Groceries"), ("potato", "Food & Groceries"), ("onion", "Food & Groceries"),
    ("carrot", "Food & Groceries"), ("lettuce", "Food & Groceries"), ("cucumber", "Food & Groceries"),
    ("cereal", "Food & Groceries"), ("oatmeal", "Food & Groceries"), ("granola", "Food & Groceries"),
    ("frozen pizza", "Food & Groceries"), ("ice cream", "Food & Groceries"),
    ("canned beans", "Food & Groceries"), ("soup", "Food & Groceries"),
    # Beverages
    ("water", "Beverages"), ("juice", "Beverages"), ("soda", "Beverages"),
    ("coffee", "Beverages"), ("tea", "Beverages"), ("beer", "Beverages"),
    ("wine", "Beverages"), ("energy drink", "Beverages"), ("smoothie", "Beverages"),
    ("cola", "Beverages"), ("sprite", "Beverages"), ("fanta", "Beverages"),
    # Household
    ("detergent", "Household"), ("soap", "Household"), ("shampoo", "Household"),
    ("toothpaste", "Household"), ("toilet paper", "Household"), ("paper towel", "Household"),
    ("dish soap", "Household"), ("sponge", "Household"), ("trash bags", "Household"),
    ("cleaning spray", "Household"), ("bleach", "Household"), ("laundry", "Household"),
    ("towel", "Household"), ("napkins", "Household"), ("tissues", "Household"),
    # Snacks
    ("chips", "Snacks"), ("chocolate", "Snacks"), ("cookies", "Snacks"),
    ("candy", "Snacks"), ("nuts", "Snacks"), ("popcorn", "Snacks"),
    ("crackers", "Snacks"), ("gum", "Snacks"), ("pretzel", "Snacks"),
    ("biscuit", "Snacks"), ("wafer", "Snacks"), ("bar", "Snacks"),
    # Health & Beauty
    ("vitamin", "Health & Beauty"), ("medicine", "Health & Beauty"),
    ("bandaid", "Health & Beauty"), ("cream", "Health & Beauty"),
    ("lotion", "Health & Beauty"), ("sunscreen", "Health & Beauty"),
    ("deodorant", "Health & Beauty"), ("razor", "Health & Beauty"),
    ("makeup", "Health & Beauty"), ("lipstick", "Health & Beauty"),
    # Other
    ("bag", "Other"), ("battery", "Other"), ("candle", "Other"),
    ("magazine", "Other"), ("toy", "Other"), ("gift card", "Other"),
]


class ProductCategorizer:
    def __init__(self):
        self.pipeline: Pipeline | None = None
        self._load_or_train()

    def _load_or_train(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                self.pipeline = pickle.load(f)
        else:
            self._train()

    def _train(self):
        texts = [item[0] for item in TRAINING_DATA]
        labels = [item[1] for item in TRAINING_DATA]

        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), lowercase=True)),
            ("clf", MultinomialNB(alpha=0.1)),
        ])
        self.pipeline.fit(texts, labels)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump(self.pipeline, f)

    def categorize(self, product_name: str) -> str:
        if not product_name or not self.pipeline:
            return "Other"
        prediction = self.pipeline.predict([product_name.lower()])
        return prediction[0]

    def categorize_batch(self, product_names: list[str]) -> list[str]:
        return [self.categorize(name) for name in product_names]


# Singleton
categorizer = ProductCategorizer()
