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
        due_time="08:00",
    )

    task2 = Task(
        task_id=2,
        pet=pet2,
        task_type="Feed Breakfast",
        duration=10,
        priority=5,
        due_time="07:30",
    )

    task3 = Task(
        task_id=3,
        pet=pet1,
        task_type="Medication",
        duration=5,
        priority=4,
        due_time="09:00",
    )

    owner.add_task(task1)
    owner.add_task(task2)
    owner.add_task(task3)

    scheduler = Scheduler(owner.get_all_tasks())
    daily_plan = scheduler.generate_daily_plan()

    print_schedule(daily_plan)


if __name__ == "__main__":
    main()