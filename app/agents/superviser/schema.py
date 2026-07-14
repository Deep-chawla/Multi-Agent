from typing import Literal
from pydantic import BaseModel,Field

class PlanStep(BaseModel):
    id:int
    agent: Literal["general","coding","research","knowledge",]
    task: str
    depends_on:list[int] = Field(default_factory=list)


class TaskExecution(BaseModel):
    step: PlanStep
    status: Literal[
        "PENDING",
        "READY",
        "RUNNING",
        "WAITING",
        "COMPLETED",
        "FAILED",
    ] = "PENDING"
    result: str | None = None
    clarification: str | None = None
    error: str | None = None

class SupervisorPlan(BaseModel):
    plan: list[PlanStep]