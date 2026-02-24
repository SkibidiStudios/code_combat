# 🎮 Code Combat 6

This repository contains **Code Combat 6** developed by 4AINFO.
The class is divided into multiple teams, each working on a **dedicated feature branch**.

The project follows a **controlled Git workflow** to avoid conflicts and keep the code organized.

---

## 🔀 Branch Structure (IMPORTANT)

This repository uses **three levels of branches**:

### 🟢 `main`
- Stable and final version of the project
- Used only for delivery or evaluation
- ❌ Do NOT push directly

### 🟡 `dev`
- Integration branch
- Contains all **approved and merged features**
- ❌ Do NOT push directly
- ✅ Only Pull Requests are allowed

### 🔵 `feature/*`
- Work branches for each group
- Each group works **only on its assigned branch**
- Pull Requests must target `dev`

---

## 👥 Feature Branches and Responsibilities

Each group has **one predefined feature branch**.

| Branch | Group | Responsibility | Folder to edit |
|------|------|---------------|----------------|
| `feature/core-system` | G1 | Core classes, inventory, slots | `core/` |
| `feature/logic-combat-system` | G2 | Combat loop & logic | `engine/` |
| `feature/ui-render-engine` | G3 | UI rendering & menus | `ui/` |
| `feature/data-json-loader` | G4 | JSON loaders & validators | `data/` |
| `feature/game-design` | G5 | Game Design Documents | `design/` |
| `feature/species-system` | G6 | Species & enemies | `species/` |
| `feature/classes-abilities` | G7 | Player classes & abilities | `classes/` |
| `feature/items-melee-armor` | G8 | Melee weapons & armor | `items/melee/` |
| `feature/items-ranged-magic` | G9 | Ranged & magic items | `items/ranged/`, `items/magic/` |
| `feature/qa-testing` | G10 | Testing & debugging | `tests/` |
| `feature/ui-assets` | G11 | Sprites & UI assets | `assets/` |
| `feature/content-world-data` | G12 | Lore & world JSON data | `data/` |

📌 **You must only modify your assigned folder.**

---

## 🧑‍💻 How to Start Working

1. Clone the repository  
   ```bash
   git clone <repo-url>
   ```

2. Checkout your group branch  
   ```bash
   git checkout feature/your-branch-name
   ```

3. Work only inside your assigned folder

4. Commit your changes  
   ```bash
   git add .
   git commit -m "Short and clear message"
   ```

5. Push your branch  
   ```bash
   git push origin feature/your-branch-name
   ```

6. Open a **Pull Request → `dev`**

---

## 🔁 Pull Request Rules

- One Pull Request per feature
- Modify only your group folder
- No direct pushes to `main` or `dev`
- Fix errors if requested during review

Pull Requests that break the rules will be rejected.

---

## 🧪 Testing

- All tests are located in `tests/`
- QA group validates merges
- If tests fail, the PR will not be merged

