# QuizApp: Complete Beginner Guide (ITDSE14)

## 0. What you are building
A website where you answer 5 multiple-choice questions one by one and get your score at the end.

| Tool | Real-life comparison | Assignment requirement |
|---|---|---|
| Jira | Task board | Project management (done) |
| Git + GitHub | Shared recipe book | Version control |
| pytest | Taste-testing the food | Software testing |
| GitHub Actions | Robot that tests every change | CI/CD |
| Docker | Lunchbox holding app + everything it needs | Containerization |
| Kubernetes | Manager running 3 copies of the lunchbox | Rollout |

## What is in this folder
| File | What it is |
|---|---|
| app.py | The backend (the "brain"): serves questions, calculates score |
| templates/index.html | The interface you see in the browser |
| tests/test_app.py | 7 automatic tests |
| requirements.txt | List of Python libraries needed |
| Dockerfile | Recipe to build the Docker container |
| .github/workflows/ci.yml | Tells GitHub Actions what to run automatically |
| k8s.yaml | Tells Kubernetes how to run the container |

## 1. Install these first (one time)
1. Python 3.12: python.org (tick "Add to PATH")
2. Git: git-scm.com
3. Docker Desktop: docker.com (then open it and wait until it says "running")
4. Minikube + kubectl: minikube.sigs.k8s.io/docs/start
5. VS Code (optional, to view files): code.visualstudio.com

## 2. Run the app on your computer
Open a terminal inside the quizapp folder:
```
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000 in your browser. Answer the quiz.
SCREENSHOT 1: the quiz question page. SCREENSHOT 2: the result page.
Press Ctrl+C in the terminal to stop.

## 3. Team of 3 + GitHub (Version Control)
1. One member creates a repo on github.com called `quizapp` (New, then Create).
2. Settings > Collaborators > add the other 2 members.
3. In the quizapp folder terminal:
```
git init
git add .
git commit -m "SCRUM-12: initial quiz app"
git branch -M main
git remote add origin https://github.com/USERNAME/quizapp.git
git push -u origin main
```
4. Teammates clone it: `git clone https://github.com/USERNAME/quizapp.git`
5. Each member makes their own change on their own branch, using the Jira ticket number:
```
git checkout -b SCRUM-13-show-score
(edit something small, e.g. a question in app.py)
git add .
git commit -m "SCRUM-13: improve score message"
git push origin SCRUM-13-show-score
```
Then on GitHub click "Compare & pull request", then "Merge".
Suggested split: Member 1 = backend (app.py), Member 2 = interface (index.html), Member 3 = tests, Docker, Kubernetes.
SCREENSHOT 3: GitHub "Commits" page showing 3 different authors.

## 4. Software Testing (pytest)
```
pytest -v
```
You should see 7 passed (green).
SCREENSHOT 4: the terminal output.

### Test case documentation (put this table in your report)
| ID | Test case | Input | Expected result | Status |
|---|---|---|---|---|
| TC1 | Home page loads | GET / | HTTP 200, page contains "QuizApp" | Pass |
| TC2 | Answers hidden | GET /api/questions | 5 questions, no "answer" field | Pass |
| TC3 | Perfect score | All correct answers | Score 5/5 | Pass |
| TC4 | Zero score | All wrong answers | Score 0/5 | Pass |
| TC5 | Partial score | 4 correct, 1 wrong | Score 4/5 | Pass |
| TC6 | Empty submit | No answers | Score 0, no crash | Pass |
| TC7 | Health check | GET /health | {"status":"ok"} | Pass |

Tool used: pytest (Python testing framework). Type: functional/unit testing of API endpoints.

## 5. CI/CD (GitHub Actions)
Nothing to install. The file .github/workflows/ci.yml is already there. When you push to GitHub, it automatically:
1. Installs Python and the libraries
2. Runs the 7 tests
3. Builds the Docker image
On GitHub open the repo > "Actions" tab > click the latest run.
SCREENSHOT 5: the green tick run with all steps. (Red cross? Click it, read the error, fix, push again.)

## 6. Docker
Make sure Docker Desktop is running, then:
```
docker build -t quizapp:1.0 .
docker run -p 5000:5000 quizapp:1.0
```
Open http://localhost:5000. It works, but now from inside a container.
SCREENSHOT 6: terminal showing the build, and the browser. Check with `docker ps` (SCREENSHOT 7).
Stop with Ctrl+C.

Dockerfile explained:
- FROM python:3.12-slim: start with a small computer that has Python
- WORKDIR /app: work inside a folder called /app
- COPY requirements.txt + RUN pip install: install libraries (done first so Docker can reuse it)
- COPY . .: copy your code in
- EXPOSE 5000: the app listens on port 5000
- CMD gunicorn...: start the app

## 7. Kubernetes (Minikube)
```
minikube start
minikube image load quizapp:1.0
kubectl apply -f k8s.yaml
kubectl get pods
kubectl get services
minikube service quizapp-service
```
The last command opens the quiz in your browser, now served by 3 copies.
SCREENSHOT 8: `kubectl get pods` showing 3 pods "Running".
SCREENSHOT 9: the quiz in the browser from Kubernetes.

Prove self-healing (nice bonus): `kubectl delete pod <one-pod-name>` then `kubectl get pods`. A new one appears automatically.
Rolling update: change something, rebuild as quizapp:2.0, `minikube image load quizapp:2.0`, then
`kubectl set image deployment/quizapp quizapp=quizapp:2.0` and `kubectl rollout status deployment/quizapp`.

k8s.yaml explained:
- Deployment: "keep 3 copies of this container running"
- Service: "one stable address that spreads visitors across the 3 copies"
- readinessProbe: Kubernetes only sends visitors to a pod once /health says OK

## 8. Jira
Link the work to Jira (SCRUM-10 to SCRUM-14). Put the ticket number in branch names and commit messages. Mark finished stories Done on the Board. Add Backlog, Board, and Summary screenshots.

## 9. Report structure
1. Title, team members and roles
2. Introduction (what the quiz app does)
3. Jira: backlog, sprint, board screenshots
4. Version control: GitHub commits, branches, pull requests
5. CI/CD: Actions screenshot and explanation
6. Testing: test case table and pytest screenshot
7. Docker: Dockerfile and screenshots
8. Kubernetes: k8s.yaml and screenshots
9. Conclusion and challenges faced

## Common errors
| Error | Fix |
|---|---|
| `pip` or `python` not recognised | Reinstall Python and tick "Add to PATH" (or try `py` / `pip3`) |
| Docker: cannot connect to daemon | Open Docker Desktop and wait until it is running |
| Pods show ErrImagePull | You forgot `minikube image load quizapp:1.0` |
| Port 5000 already in use | Use `-p 5001:5000` and open localhost:5001 |
| GitHub push asks for password | Use a Personal Access Token, or sign in via the browser popup |
