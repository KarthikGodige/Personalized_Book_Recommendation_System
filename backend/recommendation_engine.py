import pandas as pd
import re

# Load dataset
books = pd.read_csv("dataset/books_cleaned.csv")

print("Dataset loaded successfully!")
print("Number of books:", len(books))


# Create model dataframe
books_model = books[[
    "title",
    "authors",
    "categories",
    "description",
    "average_rating",
    "ratings_count",
    "thumbnail"
]].copy()


# Handle missing values
books_model["authors"] = books_model["authors"].fillna("")
books_model["categories"] = books_model["categories"].fillna("")


# Combine important book information
books_model["content"] = (
    books_model["title"] + " " +
    books_model["authors"] + " " +
    books_model["categories"] + " " +
    books_model["description"]
)


# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Apply text cleaning
books_model["clean_content"] = books_model["content"].apply(clean_text)

print("Text preprocessing completed!")
print(books_model[["title", "clean_content"]].head())

from sklearn.feature_extraction.text import TfidfVectorizer

# Create TF-IDF vectorizer
tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=50000
)

# Convert book text into TF-IDF vectors
tfidf_matrix = tfidf.fit_transform(
    books_model["clean_content"]
)

print("TF-IDF vectorization completed!")
print("TF-IDF matrix shape:", tfidf_matrix.shape)

from sklearn.metrics.pairwise import cosine_similarity

# Calculate similarity between all books
similarity_matrix = cosine_similarity(tfidf_matrix)

print("Cosine similarity completed!")
print("Similarity matrix shape:", similarity_matrix.shape)
# Create title-to-index mapping
indices = pd.Series(
    books_model.index,
    index=books_model["title"]
).drop_duplicates()


# Recommendation function
def recommend_books(title, num_recommendations=5):

    # Check if the book exists
    if title not in indices:
        return []

    # Get the index of the selected book
    idx = indices[title]

    # Get similarity scores
    similarity_scores = list(
        enumerate(similarity_matrix[idx])
    )

    # Sort books by similarity
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove the selected book itself
    similarity_scores = similarity_scores[
        1:num_recommendations + 1
    ]

    # Get indexes of recommended books
    book_indices = [
        item[0] for item in similarity_scores
    ]

    # Return book information
    return books_model.iloc[
        book_indices
    ][
        [
            "title",
            "authors",
            "categories",
            "average_rating"
        ]
    ]
print("\nRecommendations for Gilead:")

print(
    recommend_books("Gilead", 5)
)
# Calculate popularity score
books_model["popularity_score"] = (
    books_model["average_rating"] *
    books_model["ratings_count"].apply(lambda x: x ** 0.5)
)


def personalized_recommend_books(title, num_recommendations=5):

    if title not in indices:
        return []

    idx = indices[title]

    # Get similarity scores
    similarity_scores = list(
        enumerate(similarity_matrix[idx])
    )

    recommendations = []

    for book_index, similarity in similarity_scores:

        if book_index == idx:
            continue

        popularity = books_model.iloc[
            book_index
        ]["popularity_score"]

        recommendations.append(
            (book_index, similarity, popularity)
        )

    # Normalize popularity
    max_popularity = max(
        item[2] for item in recommendations
    )

    final_scores = []

    for book_index, similarity, popularity in recommendations:

        normalized_popularity = (
            popularity / max_popularity
        )

        # 80% content similarity + 20% popularity
        final_score = (
            0.8 * similarity +
            0.2 * normalized_popularity
        )

        final_scores.append(
            (book_index, final_score)
        )

    # Sort by final score
    final_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Select top recommendations
    top_books = final_scores[
        :num_recommendations
    ]

    book_indices = [
        item[0] for item in top_books
    ]

    return books_model.iloc[
        book_indices
    ][
        [
            "title",
            "authors",
            "categories",
            "average_rating"
        ]
    ]
print("\nPersonalized Recommendations for Gilead:")

print(
    personalized_recommend_books(
        "Gilead",
        5
    )
)
import joblib

# Save model components
joblib.dump(tfidf, "models/tfidf_vectorizer.pkl")
joblib.dump(tfidf_matrix, "models/tfidf_matrix.pkl")
joblib.dump(books_model, "models/books_model.pkl")
joblib.dump(indices, "models/indices.pkl")

print("\nModel files saved successfully!")