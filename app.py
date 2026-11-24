from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

QUESTIONS = [
    {"id": 1, "text": "What is 2 + 2?", "options": ["3", "4", "5", "22"], "answer": "4"},
    {"id": 2, "text": "What is the capital of France?", "options": ["Rome", "Madrid", "Paris", "Berlin"], "answer": "Paris"},
    {"id": 3, "text": "Which language is used to style web pages?", "options": ["HTML", "CSS", "Python", "SQL"], "answer": "CSS"},
    {"id": 4, "text": "What does Git do?", "options": ["Version control", "Image editing", "Video calls", "Cooking"], "answer": "Version control"},
    {"id": 5, "text": "Which tool packages an app into a container?", "options": ["Jira", "Docker", "Excel", "Zoom"], "answer": "Docker"},
]


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/questions")
def get_questions():
    # Never send the correct answer to the browser
    return jsonify([{k: v for k, v in q.items() if k != "answer"} for q in QUESTIONS])


@app.post("/api/submit")
def submit():
    answers = (request.get_json(silent=True) or {}).get("answers", {})
    score, review = 0, []
    for q in QUESTIONS:
        given = answers.get(str(q["id"]))
        correct = given == q["answer"]
        score += correct
        review.append({"id": q["id"], "text": q["text"], "your_answer": given,
                       "correct_answer": q["answer"], "correct": correct})
    return jsonify({"score": score, "total": len(QUESTIONS), "review": review})


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
