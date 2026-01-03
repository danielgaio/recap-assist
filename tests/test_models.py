"""Tests for data models."""

import pytest
from datetime import datetime
from recap_assist.models import Activity, Task, ProgressLog


def test_activity_creation():
    """Test creating an activity."""
    activity = Activity(
        id="test-1",
        description="Test activity",
        timestamp=datetime.utcnow().isoformat(),
        tags=["work", "test"],
        metadata={"key": "value"}
    )
    
    assert activity.id == "test-1"
    assert activity.description == "Test activity"
    assert len(activity.tags) == 2
    assert activity.metadata["key"] == "value"


def test_activity_serialization():
    """Test activity to_dict and from_dict."""
    activity = Activity(
        id="test-1",
        description="Test activity",
        timestamp=datetime.utcnow().isoformat(),
        tags=["test"]
    )
    
    # Convert to dict and back
    activity_dict = activity.to_dict()
    restored = Activity.from_dict(activity_dict)
    
    assert restored.id == activity.id
    assert restored.description == activity.description
    assert restored.tags == activity.tags


def test_progress_log_creation():
    """Test creating a progress log."""
    log = ProgressLog(
        timestamp=datetime.utcnow().isoformat(),
        percentage=50.0,
        note="Halfway done"
    )
    
    assert log.percentage == 50.0
    assert log.note == "Halfway done"


def test_task_creation():
    """Test creating a task."""
    task = Task(
        id="task-1",
        title="Test task",
        description="A test task",
        tags=["work"]
    )
    
    assert task.id == "task-1"
    assert task.title == "Test task"
    assert task.status == "active"
    assert task.current_progress == 0.0


def test_task_add_progress():
    """Test adding progress to a task."""
    task = Task(
        id="task-1",
        title="Test task"
    )
    
    task.add_progress(25.0, "First update")
    task.add_progress(75.0, "Second update")
    
    assert len(task.progress_logs) == 2
    assert task.current_progress == 75.0
    assert task.progress_logs[0].percentage == 25.0
    assert task.progress_logs[1].percentage == 75.0


def test_task_serialization():
    """Test task to_dict and from_dict with progress logs."""
    task = Task(
        id="task-1",
        title="Test task",
        description="Test description"
    )
    task.add_progress(50.0, "Halfway")
    
    # Convert to dict and back
    task_dict = task.to_dict()
    restored = Task.from_dict(task_dict)
    
    assert restored.id == task.id
    assert restored.title == task.title
    assert len(restored.progress_logs) == 1
    assert restored.current_progress == 50.0
