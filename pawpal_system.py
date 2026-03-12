import json
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
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

    def to_dict(self) -> dict:
        """Convert this pet and its tasks to a dictionary."""
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @staticmethod
    def from_dict(data: dict) -> "Pet":
        """Create a Pet object from a dictionary."""
        pet = Pet(
            pet_id=data["pet_id"],
            name=data["name"],
            species=data["species"],
            age=data["age"],
        )

        for task_data in data.get("tasks", []):
            task = Task.from_dict(task_data, pet)
            pet.add_task(task)

        return pet


@dataclass
class Task:
    task_id: int
    pet: Pet
    task_type: str
    duration: int
    priority: int
    due_date: date
    due_time: str
    frequency: str = "daily"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reschedule(self, new_time: str) -> None:
        """Update the task due time."""
        self.due_time = new_time

    def to_dict(self) -> dict:
        """Convert this task to a dictionary."""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "duration": self.duration,
            "priority": self.priority,
            "due_date": self.due_date.isoformat(),
            "due_time": self.due_time,
            "frequency": self.frequency,
            "completed": self.completed,
        }

    @staticmethod
    def from_dict(data: dict, pet: Pet) -> "Task":
        """Create a Task object from a dictionary and linked pet."""
        return Task(
            task_id=data["task_id"],
            pet=pet,
            task_type=data["task_type"],
            duration=data["duration"],
            priority=data["priority"],
            due_date=date.fromisoformat(data["due_date"]),
            due_time=data["due_time"],
            frequency=data.get("frequency", "daily"),
            completed=data.get("completed", False),
        )


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

    def to_dict(self) -> dict:
        """Convert this owner and all pets to a dictionary."""
        return {
            "owner_id": self.owner_id,
            "name": self.name,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    def save_to_json(self, filename: str = "data.json") -> None:
        """Save owner, pets, and tasks to a JSON file."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=2)

    @staticmethod
    def load_from_json(filename: str = "data.json") -> Optional["Owner"]:
        """Load owner, pets, and tasks from a JSON file."""
        path = Path(filename)
        if not path.exists():
            return None

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        owner = Owner(
            owner_id=data["owner_id"],
            name=data["name"],
        )

        for pet_data in data.get("pets", []):
            pet = Pet.from_dict(pet_data)
            owner.add_pet(pet)

        return owner


class Scheduler:
    def __init__(self, tasks: Optional[List[Task]] = None):
        """Initialize the scheduler with an optional task list."""
        self.tasks: List[Task] = tasks if tasks is not None else []

    def sort_tasks_by_time(self) -> List[Task]:
        """Return tasks sorted by due date and due time."""
        return sorted(self.tasks, key=lambda task: (task.due_date, task.due_time))

    def filter_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks that belong to a specific pet."""
        return [task for task in self.tasks if task.pet.name == pet_name]

    def filter_tasks_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [task for task in self.tasks if task.completed == completed]

    def mark_task_complete(self, task_id: int) -> Optional[Task]:
        """Mark a task complete and create the next recurring task if needed."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.mark_complete()

                if task.frequency == "daily":
                    new_date = task.due_date + timedelta(days=1)
                elif task.frequency == "weekly":
                    new_date = task.due_date + timedelta(days=7)
                else:
                    return None

                new_task_id = max(existing_task.task_id for existing_task in self.tasks) + 1

                new_task = Task(
                    task_id=new_task_id,
                    pet=task.pet,
                    task_type=task.task_type,
                    duration=task.duration,
                    priority=task.priority,
                    due_date=new_date,
                    due_time=task.due_time,
                    frequency=task.frequency,
                    completed=False,
                )

                self.tasks.append(new_task)
                task.pet.add_task(new_task)
                return new_task

        return None

    def sort_tasks_by_priority(self) -> List[Task]:
        """Return tasks sorted by priority, due date, and due time."""
        return sorted(
            self.tasks,
            key=lambda task: (-task.priority, task.due_date, task.due_time),
        )

    def generate_daily_plan(self) -> List[Task]:
        """Generate a daily plan from the current task list."""
        return self.sort_tasks_by_priority()

    def detect_conflicts(self) -> List[Task]:
        """Return tasks that share the same due date and due time."""
        conflicts: List[Task] = []
        seen_slots = {}

        for task in self.tasks:
            slot = (task.due_date, task.due_time)
            if slot in seen_slots:
                conflicts.append(task)
                if seen_slots[slot] not in conflicts:
                    conflicts.append(seen_slots[slot])
            else:
                seen_slots[slot] = task

        return conflicts

    def get_conflict_warnings(self) -> List[str]:
        """Return readable warning messages for tasks with the same date and time."""
        warnings: List[str] = []
        grouped_tasks = {}

        for task in self.tasks:
            slot = (task.due_date, task.due_time)
            grouped_tasks.setdefault(slot, []).append(task)

        for (due_date, due_time), tasks in grouped_tasks.items():
            if len(tasks) > 1:
                task_descriptions = [
                    f"{task.task_type} for {task.pet.name}" for task in tasks
                ]
                warning_message = (
                    f"Conflict detected on {due_date} at {due_time}: "
                    + ", ".join(task_descriptions)
                )
                warnings.append(warning_message)

        return warnings