# Local Activity & Progress Agent — Specification TODO

This document tracks what the specification is and witch parts are implemented.

---

## Core Principles
- [ ] Offline-first, fully local execution
- [ ] Single-user system
- [ ] Historical accuracy (append-only by default)
- [ ] Modular, extensible architecture (AI-ready)

---

## Interface (TUI)
- [ ] Text-based User Interface (TUI) as main interface
- [ ] Keyboard navigation (no command-heavy CLI)
- [ ] Panels for activities, tasks, and progress
- [ ] Forms for creating/editing records
- [ ] Timeline-style views

---

## Activity Logging
- [ ] Create activity
  - [ ] Timestamp (default: now)
  - [ ] Text description
  - [ ] Optional task association
- [ ] Edit activity (configurable)
- [ ] Delete activity (configurable)
- [ ] Store activities locally (SQLite or equivalent)

---

## Time-Based Queries
- [ ] Query activities by predefined intervals
  - [ ] Last week
  - [ ] Last month
  - [ ] Last quarter
- [ ] Custom date range queries
- [ ] Aggregated summaries
  - [ ] Activity count
  - [ ] Grouping by tasks

---

## Tasks (Actions)
- [ ] Create task
  - [ ] Title
  - [ ] Description
  - [ ] Start date
  - [ ] Optional target date
  - [ ] Status (planned / in progress / paused / completed)
- [ ] Edit task
- [ ] Associate activities with tasks

---

## Progress Tracking
- [ ] Create progress log entry
  - [ ] Date
  - [ ] Completion percentage (0–100)
  - [ ] Activity description
  - [ ] Optional notes
- [ ] Append-only progress history
- [ ] Prevent regressions by default (configurable)

---

## Progress Analysis & Visualization
- [ ] Task progress timeline
- [ ] Completion percentage over time (time series)
- [ ] Export data for plotting
- [ ] Detect stagnation periods (future)

---

## Persistence Layer
- [ ] Local database (SQLite)
- [ ] Clear schema for:
  - [ ] Activities
  - [ ] Tasks
  - [ ] Progress logs

---

## Architecture
- [ ] Domain layer (business logic)
- [ ] Persistence layer
- [ ] TUI interface layer
- [ ] Clear separation of concerns

---

## AI / Agent Readiness (Future)
- [ ] Activity summarization hooks
- [ ] Pattern detection hooks
- [ ] Productivity insights hooks

---

## Explicit Non-Goals (for now)
- [ ] Multi-user support
- [ ] Cloud sync
- [ ] Real-time collaboration
- [ ] Heavy graphical UI frameworks
