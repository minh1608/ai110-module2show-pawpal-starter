from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
    pet = Pet(pet_id=1, name="Milo", species="Dog", age=3)
    task = Task(
        task_id=1,
        pet=pet,
        task_type="Walk",
        duration=30,
        priority=3,
        due_time="08:00",
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
        due_time="07:30",
    )

    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1