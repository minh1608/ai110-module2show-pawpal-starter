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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
