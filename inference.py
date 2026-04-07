import requests

BASE_URL = "https://prateek12345-email_env.hf.space"

def run(task_type="hard"):
    # Reset environment
    res = requests.post(f"{BASE_URL}/reset", params={"task_type": task_type})
    obs = res.json()

    text = (obs["subject"] + " " + obs["body"]).lower()

    # Simple policy (same as baseline)
    if any(word in text for word in ["refund", "payment", "charged"]):
        action = {
            "category": "billing",
            "priority": "high",
            "action": "reply",
            "response": "We will resolve your billing issue."
        }

    elif any(word in text for word in ["error", "bug", "crash"]):
        action = {
            "category": "technical",
            "priority": "high",
            "action": "reply",
            "response": "We are investigating the issue."
        }

    elif any(word in text for word in ["win", "free", "offer", "virus", "medication", "lottery"]):
        action = {
            "category": "spam",
            "priority": "low",
            "action": "ignore",
            "response": ""
        }

    else:
        action = {
            "category": "general",
            "priority": "low",
            "action": "reply",
            "response": "Thank you for reaching out."
        }

    # Step
    res = requests.post(f"{BASE_URL}/step", json=action)
    result = res.json()

    return result


if __name__ == "__main__":
    output = run("hard")
    print(output)