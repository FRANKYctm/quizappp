import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app, QUESTIONS

client = app.test_client()
ALL_RIGHT = {str(q["id"]): q["answer"] for q in QUESTIONS}


def test_home_page_loads():                       # TC1
    r = client.get("/")
    assert r.status_code == 200 and b"QuizApp" in r.data


def test_questions_returned_without_answers():    # TC2
    data = client.get("/api/questions").get_json()
    assert len(data) == len(QUESTIONS)
    assert all("answer" not in q for q in data)


def test_perfect_score():                         # TC3
    r = client.post("/api/submit", json={"answers": ALL_RIGHT}).get_json()
    assert r["score"] == r["total"] == len(QUESTIONS)


def test_zero_score():                            # TC4
    wrong = {str(q["id"]): "wrong" for q in QUESTIONS}
    assert client.post("/api/submit", json={"answers": wrong}).get_json()["score"] == 0


def test_partial_score():                         # TC5
    partial = dict(ALL_RIGHT); partial["1"] = "wrong"
    assert client.post("/api/submit", json={"answers": partial}).get_json()["score"] == len(QUESTIONS) - 1


def test_empty_submission_does_not_crash():       # TC6
    r = client.post("/api/submit", json={})
    assert r.status_code == 200 and r.get_json()["score"] == 0


def test_health_endpoint():                       # TC7
    assert client.get("/health").get_json() == {"status": "ok"}
