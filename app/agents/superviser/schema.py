from typing import Literal
from pydantic import BaseModel,Field

class PlanStep(BaseModel):
    id:int
    agent: Literal["general","coding","research","knowledge",]
    task: str
    depends_on:list[int] = Field(default_factory=list)


class SupervisorPlan(BaseModel):
    plan: list[PlanStep]