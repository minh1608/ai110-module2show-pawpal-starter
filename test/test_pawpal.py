from datetime import date, timedelta
from pawpal_system import Pet, Task, Scheduler


def test_mark_complete_changes_task_status():
    pet = Pet(pet_id=1, name="Milo", species="Dog", age=3)
    task = Task(
        task_id=1,
        pet=pet,
        task_type="Walk",
        duration=30,
        priority=3,
        due_date=date.today(),
        due_time="08:00",
        frequency="daily",
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(pet_id=1, name="Luna", species="Cat", age=5)
    task = Task(
        task_id=2,
        pet=pet,
        task_type="Feed",
        duration=10,
        priority=5,
        due_date=date.today(),
        due_time="07:30",
        frequency="once",
    )

    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_sort_tasks_by_time_returns_chronological_order():
    pet = Pet(pet_id=1, name="Milo", species="Dog", age=3)

    task1 = Task(
        task_id=1,
        pet=pet,
        task_type="Medication",
        duration=5,
        priority=4,
        due_date=date.today(),
        due_time="09:00",
        frequency="once",
    )

    task2 = Task(
        task_id=2,
        pet=pet,
        task_type="Morning Walk",
        duration=30,
        priority=3,
        due_date=date.today(),
        due_time="08:00",
        frequency="daily",
    )

    task3 = Task(
        task_id=3,
        pet=pet,
        task_type="Feed Breakfast",
        duration=10,
        priority=5,
        due_date=date.today(),
        due_time="07:30",
        frequency="once",
    )

    scheduler = Scheduler([task1, task2, task3])
    sorted_tasks = scheduler.sort_tasks_by_time()

    assert [task.due_time for task in sorted_tasks] == ["07:30", "08:00", "09:00"]


def test_daily_task_completion_creates_next_day_task():
    pet = Pet(pet_id=1, name="Milo", species="Dog", age=3)
    today = date.today()

    task = Task(
        task_id=1,
        pet=pet,
        task_type="Morning Walk",
        duration=30,
        priority=3,
        due_date=today,
        due_time="08:00",
        frequency="daily",
    )

    scheduler = Scheduler([task])
    new_task = scheduler.mark_task_complete(1)

    assert task.completed is True
    assert new_task is not None
    assert new_task.task_type == "Morning Walk"
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.due_time == "08:00"
    assert new_task.completed is False


def test_conflict_detection_flags_same_date_and_time():
    pet1 = Pet(pet_id=1, name="Milo", species="Dog", age=3)
    pet2 = Pet(pet_id=2, name="Luna", species="Cat", age=5)
    today = date.today()

    task1 = Task(
        task_id=1,
        pet=pet1,
        task_type="Morning Walk",
        duration=30,
        priority=3,
        due_date=today,
        due_time="08:00",
        frequency="daily",
    )

    task2 = Task(
        task_id=2,
        pet=pet2,
        task_type="Feed Breakfast",
        duration=10,
        priority=5,
        due_date=today,
        due_time="08:00",
        frequency="once",
    )

    scheduler = Scheduler([task1, task2])
    warnings = scheduler.get_conflict_warnings()

    assert len(warnings) == 1
    assert "Conflict detected" in warnings[0]
    assert "08:00" in warnings[0]