from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Pet:
    pet_id: int
    name: str
    species: str
    age: int
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        pass

    def get_tasks(self) -> List["Task"]:
        pass


@dataclass
class Task:
    task_id: int
    pet: Pet
    task_type: str
    duration: int
    priority: int
    due_time: str
    completed: bool = False

    def mark_complete(self) -> None:
        pass

    def reschedule(self, new_time: str) -> None:
        pass


class Owner:
    def __init__(self, owner_id: int, name: str):
        self.owner_id = owner_id
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, tasks: Optional[List[Task]] = None):
        self.tasks: List[Task] = tasks if tasks is not None else []

    def sort_tasks_by_priority(self) -> List[Task]:
        pass

    def generate_daily_plan(self) -> List[Task]:
        pass

    def detect_conflicts(self) -> List[Task]:
        pass