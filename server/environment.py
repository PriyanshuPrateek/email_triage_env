import json
from typing import Dict

from model import EmailAction, EmailObservation, EmailState, StepResult


class EmailEnvironment:

    def __init__(self):
        with open("email_dataset_fixed.json", "r", encoding="utf-8") as f:
            self.dataset = json.load(f)

        self.state: EmailState = None

    # ================================
    # RESET
    # ================================
    def reset(self, task_type: str = "easy") -> EmailObservation:

        # deterministic for reproducibility
        email = self.dataset[0]

        self.state = EmailState(
            email_data=email,
            step_count=0,
            max_steps=1,
            task_type=task_type
        )

        return EmailObservation(
            email_id=email["id"],
            subject=email["subject"],
            body=email["body"],
            sender=email["sender"],
            task_type=task_type,
            step_count=0
        )

    # ================================
    # STEP
    # ================================
    def step(self, action: EmailAction) -> StepResult:

        if self.state is None:
            raise ValueError("Call reset() first.")

        gt = self.state.email_data["ground_truth"]
        task = self.state.task_type

        reward = 0.0
        done = True

        if task == "easy":
            if action.category == gt["category"]:
                reward = 1.0

        elif task == "medium":
            if action.category == gt["category"]:
                reward += 0.6
            if action.priority == gt["priority"]:
                reward += 0.4

        elif task == "hard":

            if action.category == gt["category"]:
                reward += 0.3

            if action.priority == gt["priority"]:
                reward += 0.2

            if action.action == gt["action"]:
                reward += 0.2

            keywords = gt.get("response_requirements", [])

            if action.response and keywords:
                match_count = sum(
                    1 for k in keywords if k.lower() in action.response.lower()
                )
                reward += 0.3 * (match_count / len(keywords))

        self.state.step_count += 1

        email = self.state.email_data

        observation = EmailObservation(
            email_id=email["id"],
            subject=email["subject"],
            body=email["body"],
            sender=email["sender"],
            task_type=self.state.task_type,
            step_count=self.state.step_count
        )

        return StepResult(
            observation=observation,
            reward=round(reward, 3),
            done=done,
            info={"task": task}
        )