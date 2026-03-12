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
        """Add a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> List["Task"]:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Task:
    task_id: int
    pet: Pet
    task_type: str
    duration: int
    priority: int
    due_time: str
    frequency: str = "daily"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reschedule(self, new_time: str) -> None:
        """Update the task due time."""
        self.due_time = new_time


class Owner:
    def __init__(self, owner_id: int, name: str):
        self.owner_id = owner_id
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Add a task to the task's assigned pet."""
        task.pet.add_task(task)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, tasks: Optional[List[Task]] = None):
        self.tasks: List[Task] = tasks if tasks is not None else []

    def sort_tasks_by_priority(self) -> List[Task]:
        """Return tasks sorted by priority and due time."""
        return sorted(self.tasks, key=lambda task: (-task.priority, task.due_time))

    def generate_daily_plan(self) -> List[Task]:
        """Generate a daily plan from the current task list."""
        return self.sort_tasks_by_priority()

    def detect_conflicts(self) -> List[Task]:
        """Return tasks that share the same due time."""
        conflicts: List[Task] = []
        seen_times = {}

        for task in self.tasks:
            if task.due_time in seen_times:
                conflicts.append(task)
                if seen_times[task.due_time] not in conflicts:
                    conflicts.append(seen_times[task.due_time])
            else:
                seen_times[task.due_time] = task

        return conflicts