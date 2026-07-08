from typing import Literal
from pydantic import BaseModel

class PlanStep(BaseModel):
    agent: Literal["general","coding","research","knowledge",]
    task: str


class SupervisorPlan(BaseModel):
    plan: list[PlanStep]