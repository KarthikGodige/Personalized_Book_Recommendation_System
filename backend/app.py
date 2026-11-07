from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Load saved model components
tfidf_matrix = joblib.load("models/tfidf_matrix.pkl")
tfidf = joblib.load("models/tfidf_vectorizer.pkl")
books_model = joblib.load("models/books_model.pkl")
indices = joblib.load("models/indices.pkl")

print("Model loaded successfully!")


@app.route("/health")
def health():
    return jsonify({
        "status": "API is running successfully"
    })


@app.route("/recommend")
def recommend():

    title = request.args.get("title")
    limit = int(request.args.get("limit", 5))

    if not title:
        return jsonify({
            "error": "Please provide a book title"
        }), 400

    if title not in indices:
        return jsonify({
            "error": "Book not found"
        }), 404

    # Get selected book index
    idx = indices[title]

    # Calculate similarity
    similarity_scores = cosine_similarity(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    # Get maximum popularity
    max_popularity = books_model["popularity_score"].max()

    final_scores = []

    for book_index, similarity in enumerate(similarity_scores):

        # Skip selected book
        if book_index == idx:
            continue

        popularity = books_model.iloc[
            book_index
        ]["popularity_score"]

        # Normalize popularity
        normalized_popularity = (
            popularity / max_popularity
        )

        # Personalized score
        final_score = (
            0.8 * similarity +
            0.2 * normalized_popularity
        )

        final_scores.append(
            (book_index, final_score)
        )

    # Sort by personalized score
    final_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Select top recommendations
    top_books = final_scores[:limit]

    recommendations = []

    for book_index, score in top_books:

        book = books_model.iloc[book_index]

        recommendations.append({
            "title": book["title"],
            "authors": book["authors"],
            "categories": book["categories"],
            "average_rating": float(book["average_rating"]),
            "recommendation_score": round(float(score), 3)
        })

    return jsonify({
        "selected_book": title,
        "recommendations": recommendations
    })
@app.route("/recommend-by-interests")
def recommend_by_interests():

    interests = request.args.get("interests", "")
    limit = int(request.args.get("limit", 5))

    if not interests:
        return jsonify({
            "error": "Please select at least one interest"
        }), 400

    selected_interests = [
        interest.strip().lower()
        for interest in interests.split(",")
        if interest.strip()
    ]

    if not selected_interests:
        return jsonify({
            "error": "Please select at least one interest"
        }), 400

    # Create user interest text
    interest_text = " ".join(selected_interests)

    # Convert user interests into TF-IDF vector
    interest_vector = tfidf.transform([interest_text])

    # Calculate NLP similarity between interests and every book
    content_scores = cosine_similarity(
        interest_vector,
        tfidf_matrix
    ).flatten()

    # Maximum popularity for normalization
    max_popularity = books_model["popularity_score"].max()

    recommendations = []

    for book_index, book in books_model.iterrows():

        category = str(book["categories"]).lower()

        # Find matching interests
        matched_interests = []

        for interest in selected_interests:

            if interest in category:
                matched_interests.append(interest)

        # Skip books that don't match any selected category
        if len(matched_interests) > 0:
            interest_score = (
        len(matched_interests) /
        len(selected_interests)
    )
        else:
            interest_score = 0

        # Interest category match
        interest_score = (
            len(matched_interests) /
            len(selected_interests)
        )

        # NLP content similarity
        content_score = content_scores[book_index]

        # Popularity score
        popularity = book["popularity_score"]

        if max_popularity > 0:
            normalized_popularity = (
                popularity / max_popularity
            )
        else:
            normalized_popularity = 0

        # Final recommendation score
        final_score = (
            0.50 * interest_score +
            0.30 * content_score +
            0.20 * normalized_popularity
        )

        recommendations.append({
            "index": int(book_index),
            "title": book["title"],
            "authors": book["authors"],
            "categories": book["categories"],
            "average_rating": float(book["average_rating"]),
            "thumbnail": book["thumbnail"],

            "interest_match": round(
                interest_score * 100, 1
            ),

            "content_similarity": round(
                content_score * 100, 1
            ),

            "recommendation_score": round(
                float(final_score),
                3
            ),

            "matched_interests": matched_interests
        })

    # Highest recommendation score first
    recommendations.sort(
        key=lambda x: x["recommendation_score"],
        reverse=True
    )

    # Keep requested number of books
    recommendations = recommendations[:limit]

    # Remove internal index
    for book in recommendations:
        book.pop("index", None)

    return jsonify({
        "selected_interests": selected_interests,
        "recommendations": recommendations
    })


if __name__ == "__main__":
    app.run(debug=True)