from pydantic import BaseModel, Field
from typing import List, Optional, Dict


# ================================
# CONSTANTS (IMPORTANT)
# ================================

CATEGORIES = ["billing", "technical", "spam", "hr", "general"]
PRIORITIES = ["low", "medium", "high"]
ACTIONS = ["reply", "escalate", "ignore"]


# ================================
# ACTION (Agent Output)
# ================================

class EmailAction(BaseModel):
    """
    Action taken by the agent.
    Supports all tasks (easy → hard).
    """
    category: str = Field(..., description="Predicted category of email")
    priority: Optional[str] = Field(None, description="Predicted priority level")
    action: Optional[str] = Field(None, description="What to do with email")
    response: Optional[str] = Field("", description="Generated response text")


# ================================
# OBSERVATION (What agent sees)
# ================================

class EmailObservation(BaseModel):
    """
    Observation sent to the agent.
    IMPORTANT: No ground truth here.
    """
    email_id: str
    subject: str
    body: str
    sender: str

    task_type: str  # easy / medium / hard
    step_count: int

    allowed_actions: List[str] = Field(default_factory=lambda: ACTIONS)


# ================================
# STATE (Internal environment state)
# ================================

class EmailState(BaseModel):
    """
    Internal state (not exposed fully to agent).
    """
    email_data: Dict  # full dataset entry (contains ground truth)
    step_count: int
    max_steps: int
    task_type: str


# ================================
# STEP RESULT (Return format)
# ================================

class StepResult(BaseModel):
    """
    Output of env.step()
    """
    observation: EmailObservation
    reward: float
    done: bool
    info: Dict = Field(default_factory=dict)