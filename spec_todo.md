# Local Activity & Progress Agent — Specification

This document tracks the simplified MVP specification and implementation status.

---

## 1. Minimal MVP (Deliver First) 🎯

### Storage Layer
- [x] **SQLite Database**
  - Story: As a system, I store data in a local SQLite file for reliability.
  - Acceptance: `recap.db` created in `~/.recap/` with `entries` and `progress_logs` tables.
  - Test: `tests/test_storage.py::test_storage_initialization`
- [x] **JSON Migration**
  - Story: As a user, my existing JSON data is preserved when upgrading.
  - Acceptance: `_migrate_from_json` runs on init, imports data, renames old file to `.bak`.
  - Test: `tests/test_storage.py` (implicit in verification script)

### Domain Model
- [x] **Unified Entry Model**
  - Story: As a developer, I use a single model for both activities and tasks.
  - Acceptance: `Entry` class supports `id`, `title`, `status`, `progress_logs`.
  - Test: `tests/test_models.py`

### Core CLI Commands
- [x] **Log Activity**
  - Story: As a user, I can log a completed activity.
  - Acceptance: `recap log "Title"` creates a `done` entry.
  - CLI: `recap log <title>`
- [x] **Create Task**
  - Story: As a user, I can create a task to track later.
  - Acceptance: `recap todo "Title"` creates an `active` entry.
  - CLI: `recap todo <title>`
- [x] **List Entries**
  - Story: As a user, I can see my entries filtered by status or time.
  - Acceptance: `recap list` shows entries; supports `--status` and `--filter`.
  - CLI: `recap list [--status] [--filter]`
- [x] **Update Progress**
  - Story: As a user, I can update progress on a task.
  - Acceptance: `recap progress <id> <pct>` adds a log entry and updates current progress.
  - CLI: `recap progress <id> <pct>`
- [x] **Complete Entry**
  - Story: As a user, I can mark a task as done.
  - Acceptance: `recap complete <id>` sets status to `done` and progress to 100%.
  - CLI: `recap complete <id>`
- [x] **Cancel Entry**
  - Story: As a user, I can cancel a task I won't finish.
  - Acceptance: `recap cancel <id>` sets status to `cancelled`.
  - CLI: `recap cancel <id>`
- [x] **Show Details**
  - Story: As a user, I can see the full history of an entry.
  - Acceptance: `recap show <id>` displays metadata and progress timeline.
  - CLI: `recap show <id>`

### Time Filters
- [x] **Date Range Logic**
  - Story: As a user, I can filter lists by common time ranges.
  - Acceptance: `this-week`, `last-week`, `this-month` correctly calculate ranges.
  - Test: `tests/test_utils.py`

---

## 2. Backlog / Nice-to-Have ⏳

### Enhanced CLI / TUI
- [ ] **Interactive TUI**
  - Story: As a user, I can navigate my data without memorizing commands.
  - Acceptance: Textual-based UI with list/detail views.
- [ ] **Edit Command**
  - Story: As a user, I can fix typos in titles or descriptions.
  - Acceptance: `recap edit <id>` allows modifying fields.

### Advanced Features
- [ ] **Visualizations**
  - Story: As a user, I can see my progress over time visually.
  - Acceptance: ASCII charts or export to plotting tools.
- [ ] **Stagnation Detection**
  - Story: As a user, I am alerted to tasks that haven't moved in X days.
- [ ] **AI Summarization**
  - Story: As a user, I can get a summary of my week using a local LLM.

### Explicit Non-Goals
- Multi-user support
- Cloud sync
- Real-time collaboration
- Heavy graphical UI frameworks
