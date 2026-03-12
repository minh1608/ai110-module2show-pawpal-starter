from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(tasks):
    print("\nToday's Schedule")
    print("=" * 40)
    for task in tasks:
        status = "Done" if task.completed else "Pending"
        print(
            f"{task.due_time} | {task.pet.name:<10} | "
            f"{task.task_type:<12} | Priority {task.priority} | {status}"
        )


def main():
    owner = Owner(owner_id=1, name="Minh")

    pet1 = Pet(pet_id=1, name="Milo", species="Dog", age=3)
    pet2 = Pet(pet_id=2, name="Luna", species="Cat", age=5)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(
        task_id=1,
        pet=pet1,
        task_type="Morning Walk",
        duration=30,
        priority=3,
        due_date=date.today(),
        due_time="08:00",
        frequency="daily",
    )

    task2 = Task(
        task_id=2,
        pet=pet2,
        task_type="Feed Breakfast",
        duration=10,
        priority=5,
        due_date=date.today(),
        due_time="08:00",
        frequency="once",
    )

    task3 = Task(
        task_id=3,
        pet=pet1,
        task_type="Medication",
        duration=5,
        priority=4,
        due_date=date.today(),
        due_time="09:00",
        frequency="weekly",
    )

    owner.add_task(task1)
    owner.add_task(task2)
    owner.add_task(task3)

    scheduler = Scheduler(owner.get_all_tasks())
    daily_plan = scheduler.generate_daily_plan()

    print_schedule(daily_plan)

    print("\nSorted Tasks by Time")
    print("=" * 40)
    sorted_tasks = scheduler.sort_tasks_by_time()
    for task in sorted_tasks:
        print(f"{task.due_time} | {task.pet.name:<10} | {task.task_type}")

    print("\nFiltered Tasks for Pet: Milo")
    print("=" * 40)
    milo_tasks = scheduler.filter_tasks_by_pet("Milo")
    for task in milo_tasks:
        print(f"{task.due_time} | {task.pet.name:<10} | {task.task_type}")

    print("\nIncomplete Tasks")
    print("=" * 40)
    pending_tasks = scheduler.filter_tasks_by_status(False)
    for task in pending_tasks:
        print(f"{task.due_time} | {task.pet.name:<10} | {task.task_type}")

    print("\nConflict Warnings")
    print("=" * 40)

    conflict_warnings = scheduler.get_conflict_warnings()

    if conflict_warnings:
        for warning in conflict_warnings:
            print(warning)
    else:
        print("No conflicts detected.")

    print("\nRecurring Task Test")
    print("=" * 40)

    new_daily_task = scheduler.mark_task_complete(1)
    new_weekly_task = scheduler.mark_task_complete(3)

    print("Task 1 completed:", task1.completed)
    print("Task 3 completed:", task3.completed)

    if new_daily_task:
        print(
            f"New daily task created: {new_daily_task.task_type} | "
            f"{new_daily_task.due_date} | {new_daily_task.due_time}"
        )

    if new_weekly_task:
        print(
            f"New weekly task created: {new_weekly_task.task_type} | "
            f"{new_weekly_task.due_date} | {new_weekly_task.due_time}"
        )

if __name__ == "__main__":
    main()