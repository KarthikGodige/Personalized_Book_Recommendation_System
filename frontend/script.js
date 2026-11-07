const selectedInterests = [];


/* ================================
   INTEREST SELECTION
================================ */

document.querySelectorAll(".interest-btn").forEach(function(button) {

    button.addEventListener("click", function() {

        const interest = button.dataset.interest;

        if (selectedInterests.includes(interest)) {

            const index = selectedInterests.indexOf(interest);

            selectedInterests.splice(index, 1);

            button.classList.remove("selected");

        } else {

            if (selectedInterests.length >= 5) {

                document.getElementById("message").textContent =
                    "You can select up to 5 interests.";

                return;
            }

            selectedInterests.push(interest);

            button.classList.add("selected");
        }

        if (selectedInterests.length > 0) {

            document.getElementById("message").textContent =
                selectedInterests.length +
                " interest(s) selected";

        } else {

            document.getElementById("message").textContent = "";
        }
    });

});


/* ================================
   BOOK SEARCH
================================ */

async function getRecommendations() {

    const bookInput =
        document.getElementById("bookInput");

    const message =
        document.getElementById("message");

    const recommendations =
        document.getElementById("bookRecommendations");

    const title = bookInput.value.trim();

    if (!title) {

        message.textContent =
            "Please enter a book title.";

        recommendations.innerHTML = "";

        return;
    }

    message.textContent =
        "Finding recommendations...";

    recommendations.innerHTML = "";

    try {

        const url =
            "http://127.0.0.1:5000/recommend?title=" +
            encodeURIComponent(title) +
            "&limit=5";

        const response = await fetch(url);

        const data = await response.json();

        if (!response.ok) {

            message.textContent =
                data.error || "Something went wrong.";

            return;
        }

        message.textContent =
            "📚 Books recommended for \"" +
            data.selected_book +
            "\"";

        data.recommendations.forEach(function(book) {

            const card =
                document.createElement("div");

            card.className = "book-card";

            card.innerHTML =
                "<h3>" +
                book.title +
                "</h3>" +

                "<p><strong>Author:</strong> " +
                (book.authors || "Unknown") +
                "</p>" +

                "<p><strong>Category:</strong> " +
                (book.categories || "Unknown") +
                "</p>" +

                "<p class=\"rating\">⭐ " +
                book.average_rating +
                "</p>" +

                "<p><strong>Recommendation Score:</strong> " +
                book.recommendation_score +
                "</p>";

            recommendations.appendChild(card);
        });

    } catch (error) {

        console.error("Book recommendation error:", error);

        message.textContent =
            "Unable to connect to the recommendation server.";
    }
}


/* ================================
   INTEREST RECOMMENDATIONS
================================ */

async function getInterestRecommendations() {

    const message =
        document.getElementById("message");

    const recommendations =
        document.getElementById("interestRecommendations");

    if (selectedInterests.length === 0) {

        message.textContent =
            "Please select at least one interest.";

        recommendations.innerHTML = "";

        return;
    }

    message.textContent =
        "Finding books based on your interests...";

    recommendations.innerHTML = "";

    const query =
        selectedInterests
            .map(function(interest) {
                return encodeURIComponent(interest);
            })
            .join(",");

    try {

        const url =
            "http://127.0.0.1:5000/recommend-by-interests" +
            "?interests=" +
            query +
            "&limit=6";

        const response = await fetch(url);

        const data = await response.json();

        if (!response.ok) {

            message.textContent =
                data.error || "Something went wrong.";

            return;
        }

        message.textContent =
            "✨ Recommendations for: " +
            data.selected_interests.join(", ");

        data.recommendations.forEach(function(book) {

            const card =
                document.createElement("div");

            card.className = "book-card";

            let whyText =
                "Related through NLP similarity";

            if (
                book.matched_interests &&
                book.matched_interests.length > 0
            ) {
                whyText =
                    book.matched_interests.join(", ");
            }

            card.innerHTML =
    "<img src=\"" +
    (book.thumbnail || "https://via.placeholder.com/120x180?text=No+Cover") +
    "\" alt=\"Book cover\" class=\"book-cover\">" +

    "<h3>" +
    book.title +
    "</h3>" +

                "<p><strong>Author:</strong> " +
                (book.authors || "Unknown") +
                "</p>" +

                "<p><strong>Category:</strong> " +
                (book.categories || "Unknown") +
                "</p>" +

                "<p class=\"rating\">⭐ " +
                book.average_rating +
                "</p>" +

                "<p><strong>🎯 Interest Match:</strong> " +
                book.interest_match +
                "%</p>" +

                "<p><strong>🧠 NLP Similarity:</strong> " +
                book.content_similarity +
                "%</p>" +

                "<p><strong>💡 Why:</strong> " +
                whyText +
                "</p>" +

                "<p><strong>🏆 Recommendation Score:</strong> " +
                book.recommendation_score +
                "</p>";

            recommendations.appendChild(card);
        });

    } catch (error) {

        console.error(
            "Interest recommendation error:",
            error
        );

        message.textContent =
            "Unable to connect to the recommendation server.";
    }
}