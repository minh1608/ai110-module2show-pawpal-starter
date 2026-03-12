# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## 📸 Demo

Below is an example of the PawPal+ scheduling interface.

![PawPal Demo](pawpal_demo.png)

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ now includes several simple algorithms to help organize pet care tasks:

- **Task Sorting:** Tasks can be sorted by due time to create a clear daily order.
- **Filtering:** Tasks can be filtered by pet name or completion status.
- **Recurring Tasks:** When a daily or weekly task is completed, a new task instance is automatically scheduled for the next occurrence.
- **Conflict Detection:** The scheduler detects tasks scheduled at the same time and returns a warning message.

These features help the system produce a more useful and intelligent daily care plan for the pet owner.

## AI Task Suggestions

PawPal+ now includes a simple AI-inspired task suggestion feature.

When a user selects a pet, the system automatically recommends common care tasks based on the pet’s species. For example:

- Dogs may receive suggestions such as **Morning Walk**, **Feed Breakfast**, or **Play Time**.
- Cats may receive suggestions like **Clean Litter Box**, **Feed Meal**, or **Play Session**.

These suggestions help the owner quickly add typical care activities without manually entering every task. Suggested tasks can be added with a single click and are immediately integrated into the scheduling system.

## Features

PawPal+ includes several intelligent scheduling features designed to help pet owners manage daily care tasks effectively:

- **Task Sorting by Time**  
  Tasks can be automatically sorted by due date and time to create a clear chronological schedule.

- **Priority-Based Planning**  
  Higher priority tasks appear earlier in the generated daily plan.

- **Task Filtering**  
  Tasks can be filtered by pet name or completion status to focus on specific care responsibilities.

- **Recurring Tasks**  
  When a task with a frequency of "daily" or "weekly" is completed, the system automatically creates the next occurrence.

- **Conflict Detection**  
  The scheduler detects tasks scheduled at the same date and time and provides warning messages.

These features make the PawPal+ system more intelligent and helpful for organizing pet care routines.

## Data Persistence

PawPal+ now saves pets and tasks between runs using a JSON file.

All owner, pet, and task data are automatically stored in `data.json`.  
When the app starts, it loads this file so previously added pets and tasks remain available.

This persistence layer allows the system to behave more like a real application rather than a temporary demo session.

## Testing PawPal+

You can run the automated tests with:

```bash
python -m pytest
```

The current test suite verifies core behaviors in the PawPal+ system, including:
	•	task completion
	•	task addition
	•	chronological sorting
	•	recurring task creation
	•	conflict detection

**Confidence Level:** ★★★★☆ (4/5)

I am confident that the core scheduling logic works correctly for the main happy paths and key edge cases covered by the tests. If I had more time, I would add more tests for empty schedules, overlapping durations, and weekly recurrence edge cases.