from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from model import EmailAction
from server.environment import EmailEnvironment
import requests
from fastapi.responses import HTMLResponse

# ================================
# FASTAPI INIT (IMPORTANT FIX)
# ================================
app = FastAPI(
    title="Email Triage Environment",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json"
)

# ================================
# CORS (IMPORTANT FOR HF)
# ================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# ENVIRONMENT
# ================================
env = EmailEnvironment()


# ================================
# ROOT (REQUIRED FOR HF)
# ================================

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head><title>Email API</title></head>
        <body>
            <h1>✅ Email Triage API Running</h1>
            <p>Use <a href="/docs">/docs</a> to access API</p>
        </body>
    </html>
    """


# ================================
# HEALTH CHECK
# ================================
@app.get("/health")
def health():
    return {"status": "healthy"}


# ================================
# RESET
# ================================
@app.post("/reset")
def reset(task_type: str = "easy"):
    obs = env.reset(task_type)
    return obs


# ================================
# STEP
# ================================
@app.post("/step")
def step(action: EmailAction):
    result = env.step(action)
    return result


# ================================
# TASKS
# ================================
@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {
                "name": "easy",
                "description": "Classify email category",
                "action_schema": {"category": "string"}
            },
            {
                "name": "medium",
                "description": "Classify + assign priority",
                "action_schema": {
                    "category": "string",
                    "priority": "string"
                }
            },
            {
                "name": "hard",
                "description": "Full email handling",
                "action_schema": {
                    "category": "string",
                    "priority": "string",
                    "action": "string",
                    "response": "string"
                }
            }
        ]
    }


# ================================
# GRADER
# ================================
@app.post("/grader")
def grader(action: EmailAction, task_type: str = "hard"):
    VALID_CATEGORIES = ["billing", "technical", "spam", "hr", "general"]

    if action.category not in VALID_CATEGORIES:
        return {"error": "Invalid category"}

    try:
        env.reset(task_type)
        result = env.step(action)

        return {
            "task": task_type,
            "score": result.reward
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Invalid action input"
        }


# ================================
# BASELINE
# ================================
@app.get("/baseline")
def run_baseline():
    scores = {}

    def simple_policy(observation):
        text = (observation.subject + " " + observation.body).lower()

        if any(word in text for word in ["refund", "payment", "charged"]):
            return EmailAction(
                category="billing",
                priority="high",
                action="reply",
                response="We will resolve your billing issue."
            )

        elif any(word in text for word in ["error", "bug", "crash"]):
            return EmailAction(
                category="technical",
                priority="high",
                action="reply",
                response="We are investigating the issue."
            )

        elif any(word in text for word in ["win", "free", "offer", "virus", "medication", "lottery"]):
            return EmailAction(
                category="spam",
                priority="low",
                action="ignore",
                response=""
            )

        else:
            return EmailAction(
                category="general",
                priority="low",
                action="reply",
                response="Thank you for reaching out."
            )

    for task in ["easy", "medium", "hard"]:
        obs = env.reset(task)
        action = simple_policy(obs)
        result = env.step(action)

        scores[task] = result.reward

    return {"baseline_scores": scores}