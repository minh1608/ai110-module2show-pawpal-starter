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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
