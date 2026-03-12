import streamlit as st
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
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=40, value=2)

# Keep Owner in session memory
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id=1, name=owner_name)
else:
    st.session_state.owner.name = owner_name

# Keep Pet in session memory
if "pet" not in st.session_state:
    st.session_state.pet = Pet(
        pet_id=1,
        name=pet_name,
        species=species,
        age=int(age),
    )
    st.session_state.owner.add_pet(st.session_state.pet)
else:
    st.session_state.pet.name = pet_name
    st.session_state.pet.species = species
    st.session_state.pet.age = int(age)

st.write("Owner object in session:", st.session_state.owner)
st.write("Pet object in session:", st.session_state.pet)

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
    task = Task(
        task_id=st.session_state.task_counter,
        pet=st.session_state.pet,
        task_type=task_title,
        duration=int(duration),
        priority=priority_map[priority_label],
        due_time=due_time,
        frequency=frequency,
    )
    st.session_state.owner.add_task(task)
    st.session_state.task_counter += 1
    st.success(f"Added task: {task_title}")
    st.rerun()

current_tasks = st.session_state.pet.get_tasks()

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
                st.session_state.pet.tasks.pop(index)
                st.session_state.schedule_rows = []
                st.session_state.plan_explanations = []
                st.session_state.conflict_rows = []
                st.rerun()

    if st.button("Clear all tasks"):
        st.session_state.pet.tasks = []
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
            st.table(st.session_state.schedule_rows)

            st.markdown("### Why this plan was chosen")
            for explanation in st.session_state.plan_explanations:
                st.write(explanation)

            if st.session_state.conflict_rows:
                st.markdown("### Scheduling Conflicts")
                st.warning("Some tasks share the same due time.")
                st.table(st.session_state.conflict_rows)
            else:
                st.info("No scheduling conflicts detected.")