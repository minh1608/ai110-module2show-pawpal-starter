# PawPal+ Project Reflection

## 1. System Design

The three main actions in PawPal+ are adding pet and owner information, creating pet care tasks, and generating a daily care plan. The user needs a way to store basic pet details so the system can organize care around the correct pet. The user also needs to add tasks like feeding, walking, medication, and grooming with enough detail for scheduling. Finally, the app should generate a daily plan that helps the owner decide what to do first and why.

**a. Initial design**

My initial UML design used four main classes: Owner, Pet, Task, and Scheduler. Owner is responsible for storing the owner’s identity and managing the pets in the system. Pet stores basic pet information such as name, species, and age, and keeps a list of care tasks for that pet. Task represents a single care activity, such as feeding, walking, or medication, and stores details like duration, priority, due time, and completion status. Scheduler is responsible for organizing tasks, sorting them by priority, generating a daily plan, and detecting scheduling conflicts.

**b. Design changes**

After reviewing the skeleton, I decided to keep the Owner class focused on managing pets rather than storing a separate master list of tasks. Instead, tasks belong directly to each Pet, and the owner can collect all tasks through the pets when needed. I also noticed that the Scheduler may eventually need additional inputs such as available time or owner preferences, but I chose not to add those yet because the Phase 1 goal was to keep the system skeleton simple and focused. This helped me avoid unnecessary complexity too early in the design process.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler currently considers three main constraints: task priority, due time, and completion status. Priority determines which tasks should appear earlier in the schedule, while due time helps organize tasks chronologically within the same priority level. The scheduler also tracks whether a task has already been completed so that only incomplete tasks are considered when generating a plan. I decided that priority and due time mattered most because pet care tasks often have different levels of urgency. For example, feeding or medication may be more urgent than enrichment activities, so higher-priority tasks should appear earlier in the schedule.

**b. Tradeoffs**

One tradeoff my scheduler makes is that conflict detection only checks for exact matching task times instead of overlapping durations. For example, it can detect two tasks scheduled at 08:00, but it would not detect a conflict between a task at 08:00 for 30 minutes and another task at 08:15 for 20 minutes. I decided this tradeoff was reasonable for this version of PawPal+ because it keeps the algorithm simple, readable, and easy to verify in a beginner-friendly project. If I had more time, I would improve it by comparing time ranges instead of exact matches only.

---

## 3. AI Collaboration

**a. How you used AI**

During this project, I used AI tools mainly for brainstorming design ideas, debugging errors, and reviewing my code structure. AI was helpful for suggesting improvements to the scheduling logic, identifying potential edge cases, and explaining why certain errors occurred. I also used AI to help generate test ideas and to review whether my implementation matched the intended system design.

The most helpful prompts were questions that focused on understanding the system behavior, such as asking why a scheduling result appeared incorrect or how to structure classes so that responsibilities were clearly separated. These kinds of prompts helped me reason about the system rather than just copying generated code.

**b. Judgment and verification**

One moment where I did not accept an AI suggestion as-is occurred when implementing multi-pet support in the Streamlit interface. An early suggestion reused a single pet object stored in session state, which caused tasks from different pets to overwrite each other and appear under the wrong pet in the schedule. Instead of using that approach, I redesigned the logic so that the Owner class stores a list of Pet objects, and the interface allows the user to select which pet a task belongs to.

To verify AI suggestions, I relied on testing the program directly. I ran the application, created multiple pets and tasks, and checked whether the schedule displayed the correct pet names and task order. If the system behavior did not match expectations, I adjusted the implementation until the output was correct.

---

## 4. Testing and Verification

**a. What you tested**

I wrote automated tests using pytest to verify several important behaviors of the system. These tests checked that tasks are stored correctly, that tasks are sorted chronologically, that recurring tasks are created properly when a task is completed, and that the scheduler can detect conflicts when two tasks share the same due time. I also tested filtering functions that return tasks for a specific pet.

These tests were important because the scheduler logic is the core of the application. If sorting, recurrence, or conflict detection fails, the generated schedule would be unreliable for the user.

**b. Confidence**

Based on the test results and manual testing in the Streamlit interface, I am reasonably confident that the scheduler works correctly for the main use cases of the application. The automated tests confirm that the key algorithms behave as expected.

If I had more time, I would add additional tests for edge cases such as pets with no tasks, tasks with identical priorities and times, and scenarios involving overlapping task durations. I would also test more complex recurrence patterns to ensure they behave consistently over time.

---

## 5. Reflection

**a. What went well**

The part of this project I am most satisfied with is the separation between the scheduling logic and the user interface. By placing all scheduling algorithms inside the Scheduler class, the system remains organized and easier to test. This structure also made it easier to connect the logic to the Streamlit interface later without rewriting the core logic.

**b. What you would improve**

If I were to continue developing this project, I would improve the scheduling algorithm to detect overlapping time ranges instead of only identical timestamps. I would also expand the UI so users could edit or reschedule tasks directly from the interface. Another improvement would be allowing the scheduler to consider the owner’s available time and automatically distribute tasks more intelligently throughout the day.

**c. Key takeaway**

One important lesson from this project is that AI tools are most effective when used as assistants rather than decision-makers. AI can help generate ideas and suggest solutions, but the developer still needs to evaluate those suggestions carefully and ensure they fit the system design. Acting as the system architect and verifying results through testing is essential when collaborating with AI tools in software development.