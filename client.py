import requests

BASE_URL = "http://127.0.0.1:8000"


# ================================
# SIMPLE BASELINE POLICY
# ================================
def simple_policy(observation):
    """
    Basic rule-based policy (not smart, just baseline)
    """

    text = (observation["subject"] + " " + observation["body"]).lower()

    # Very basic rules
    if "refund" in text or "payment" in text or "charged" in text:
        category = "billing"
        priority = "high"
        action = "reply"

    elif "error" in text or "bug" in text or "crash" in text:
        category = "technical"
        priority = "high"
        action = "reply"

    elif any(word in text for word in ["win", "free", "offer", "virus", "medication", "prize", "lottery"]):
        category = "spam"
        priority = "low"
        action = "ignore"
    else:
        category = "general"
        priority = "low"
        action = "reply"

    return {
        "category": category,
        "priority": priority,
        "action": action,
        "response": "We will look into your issue."
    }


# ================================
# RUN EPISODE
# ================================
def run_task(task_type):
    print(f"\nRunning task: {task_type.upper()}")

    # Reset environment
    res = requests.post(f"{BASE_URL}/reset", params={"task_type": task_type})
    obs = res.json()

    # Get action from policy
    action = simple_policy(obs)

    # Step
    res = requests.post(f"{BASE_URL}/step", json=action)
    result = res.json()

    print("Reward:", result["reward"])
    return result["reward"]


# ================================
# MAIN
# ================================
if __name__ == "__main__":

    scores = {}

    for task in ["easy", "medium", "hard"]:
        score = run_task(task)
        scores[task] = score

    print("\nFinal Scores:")
    print(scores)