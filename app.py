import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+.

This version connects the Streamlit UI to your backend logic so you can create pets,
add care tasks, and generate a daily schedule.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

with st.expander("What this demo does", expanded=True):
    st.markdown(
        """
This demo lets you:
- Enter basic owner and pet information
- Add pet care tasks with duration, priority, due time, and frequency
- Generate a daily schedule using your backend classes
"""
    )

st.divider()

st.subheader("Owner and Pet Info")
owner_name = st.text_input("Owner name", value="Minh")

st.markdown("### Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=40, value=2)

# Keep Owner in session memory
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id=1, name=owner_name)
else:
    st.session_state.owner.name = owner_name

if "pet_counter" not in st.session_state:
    st.session_state.pet_counter = 1

if st.button("Add pet"):
    existing_names = [pet.name for pet in st.session_state.owner.pets]
    if not pet_name.strip():
        st.error("Please enter a pet name.")
    elif pet_name in existing_names:
        st.warning("A pet with this name already exists.")
    else:
        new_pet = Pet(
            pet_id=st.session_state.pet_counter,
            name=pet_name,
            species=species,
            age=int(age),
        )
        st.session_state.owner.add_pet(new_pet)
        st.session_state.pet_counter += 1
        st.success(f"Added pet: {pet_name}")
        st.rerun()

if st.session_state.owner.pets:
    pet_names = [pet.name for pet in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Select pet for tasks", pet_names)

    selected_pet = next(
        pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name
    )

    st.caption(
        f"Selected pet: {selected_pet.name} ({selected_pet.species}, age {selected_pet.age})"
    )
else:
    selected_pet = None
    st.info("No pets added yet. Add a pet first.")

# Keep Owner in session memory
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id=1, name=owner_name)
else:
    st.session_state.owner.name = owner_name

st.write("Owner object in session:", st.session_state.owner)

if "schedule_rows" not in st.session_state:
    st.session_state.schedule_rows = []

if "plan_explanations" not in st.session_state:
    st.session_state.plan_explanations = []

if "conflict_rows" not in st.session_state:
    st.session_state.conflict_rows = []

st.markdown("### Tasks")
st.caption("Add a few tasks, then generate a daily schedule.")

col1, col2 = st.columns(2)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)

col3, col4 = st.columns(2)
with col3:
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    due_time = st.text_input("Due time (HH:MM)", value="08:00")

frequency = st.selectbox("Frequency", ["daily", "weekly", "once"], index=0)

priority_map = {
    "low": 1,
    "medium": 2,
    "high": 3,
}

if "task_counter" not in st.session_state:
    st.session_state.task_counter = 1

if st.button("Add task"):
    if selected_pet is None:
        st.error("Please add a pet before adding tasks.")
    else:
        task = Task(
            task_id=st.session_state.task_counter,
            pet=selected_pet,
            task_type=task_title,
            duration=int(duration),
            priority=priority_map[priority_label],
            due_date=date.today(),
            due_time=due_time,
            frequency=frequency,
        )
        st.session_state.owner.add_task(task)
        st.session_state.task_counter += 1
        st.success(f"Added task: {task_title} for {selected_pet.name}")
        st.rerun()

current_tasks = st.session_state.owner.get_all_tasks()

if current_tasks:
    st.write("Current tasks:")

    for index, task in enumerate(current_tasks):
        col1, col2 = st.columns([8, 1])

        with col1:
            st.write(
                f"{task.task_type} | {task.duration} min | "
                f"Priority {task.priority} | {task.due_time} | {task.frequency}"
            )

        with col2:
            if st.button("❌", key=f"delete_{task.task_id}"):
                task.pet.tasks = [pet_task for pet_task in task.pet.tasks if pet_task.task_id != task.task_id]
                st.session_state.schedule_rows = []
                st.session_state.plan_explanations = []
                st.session_state.conflict_rows = []
                st.rerun()

    if st.button("Clear all tasks"):
        for pet in st.session_state.owner.pets:
            pet.tasks = []
        st.session_state.schedule_rows = []
        st.session_state.plan_explanations = []
        st.session_state.conflict_rows = []
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule using your backend PawPal system.")

if st.button("Generate schedule"):
    all_tasks = st.session_state.owner.get_all_tasks()

    if not owner_name.strip() or not pet_name.strip():
        st.error("Please enter both owner and pet information.")
    elif not all_tasks:
        st.error("Please add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(all_tasks)
        daily_plan = scheduler.generate_daily_plan()
        conflicts = scheduler.detect_conflicts()

        schedule_rows = []
        plan_explanations = []

        for position, task in enumerate(daily_plan, start=1):
            schedule_rows.append(
                {
                    "Time": task.due_time,
                    "Pet": task.pet.name,
                    "Task": task.task_type,
                    "Duration": f"{task.duration} min",
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Status": "Done" if task.completed else "Pending",
                }
            )

            plan_explanations.append(
                f"{position}. {task.task_type} for {task.pet.name} is scheduled at "
                f"{task.due_time} because it has priority {task.priority}."
            )

        conflict_rows = []
        for task in conflicts:
            conflict_rows.append(
                {
                    "Time": task.due_time,
                    "Pet": task.pet.name,
                    "Task": task.task_type,
                }
            )

        st.session_state.schedule_rows = schedule_rows
        st.session_state.plan_explanations = plan_explanations
        st.session_state.conflict_rows = conflict_rows

        st.success("Schedule generated successfully.")
        if st.session_state.schedule_rows:
            st.markdown("### Today's Schedule")
            st.caption("Tasks are automatically sorted by priority and due time.")
            st.table(st.session_state.schedule_rows)

            st.markdown("### Why this plan was chosen")
            for explanation in st.session_state.plan_explanations:
                st.write(explanation)

            if st.session_state.conflict_rows:
                st.markdown("### Scheduling Conflicts")
                st.warning("⚠️ Scheduling conflict detected. Multiple tasks are scheduled at the same time.")
                st.table(st.session_state.conflict_rows)
            else:
                st.info("No scheduling conflicts detected.")