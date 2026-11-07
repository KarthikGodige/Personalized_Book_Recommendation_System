# Personalized Book Recommendation System

An NLP-powered book recommendation web application that helps users discover books based on their reading interests and previously selected books.

## Features

- **Book-Based Recommendations:** Find similar books by entering a book title.
- **Interest-Based Recommendations:** Discover books by selecting preferred categories.
- **TF-IDF Vectorization:** Convert book information into numerical text features.
- **Cosine Similarity:** Measure similarity between books and user interests.
- **Popularity-Based Ranking:** Combine relevance and popularity to improve recommendations.
- **Interactive Web Interface:** View book covers, authors, categories, ratings, and recommendation scores.

## Technologies Used

| Area | Technologies |
|---|---|
| Programming Language | Python, JavaScript |
| NLP and Machine Learning | Scikit-learn, TF-IDF, Cosine Similarity |
| Data Processing | Pandas, NumPy |
| Backend | Flask, Flask-CORS |
| Frontend | HTML, CSS, JavaScript |
| Model Persistence | Joblib |

## Dataset

The project uses a dataset containing 5,197 books.

Dataset source: [Hugging Face – Book Recommender Dataset](https://huggingface.co/datasets/svastikkka/BOOK-RECOMMENDER-DATASET)

## Project Structure

```text
Personalized_Book_Recommendation_System/
├── backend/
│   ├── app.py
│   └── recommendation_engine.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── dataset/
│   └── books_cleaned.csv
├── models/
│   ├── books_model.pkl
│   ├── indices.pkl
│   ├── tfidf_matrix.pkl
│   └── tfidf_vectorizer.pkl
├── .gitignore
└── README.md
```

## Installation and Setup

1. Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

2. Navigate into the project:

```bash
cd Personalized_Book_Recommendation_System
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install flask flask-cors pandas numpy scikit-learn joblib
```

5. Start the Flask backend:

```bash
python backend/app.py
```

6. Open `frontend/index.html` in your browser.

## Recommendation Methodology

### Book-Based Recommendation

The system combines content similarity and normalized popularity:

**Final Score = 0.80 × Content Similarity + 0.20 × Normalized Popularity**

### Interest-Based Recommendation

The system combines category matching, NLP similarity, and popularity:

**Final Score = 0.50 × Interest Match + 0.30 × NLP Content Similarity + 0.20 × Normalized Popularity**

## Future Enhancements

- User authentication and personalized profiles.
- User feedback-based recommendations.
- Collaborative filtering.
- Advanced NLP models.
- Deployment as a publicly accessible web application.

## Author

**Karthik Godige**

GitHub: [KarthikGodige](https://github.com/KarthikGodige)

LinkedIn: [Godige Karthik](https://www.linkedin.com/in/godige-karthik-b6353b368/)

---

*Developed as an NLP course-end project.*