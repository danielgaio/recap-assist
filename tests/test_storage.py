"""Tests for storage layer."""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from recap_assist.storage import Storage


@pytest.fixture
def temp_storage():
    """Create a temporary storage for testing."""
    temp_dir = tempfile.mkdtemp()
    storage = Storage(temp_dir)
    yield storage
    shutil.rmtree(temp_dir)


def test_storage_initialization(temp_storage):
    """Test storage initialization creates necessary files."""
    assert temp_storage.activities_file.exists()
    assert temp_storage.tasks_file.exists()


def test_add_activity(temp_storage):
    """Test adding an activity."""
    activity = temp_storage.add_activity(
        description="Test activity",
        tags=["test", "work"]
    )
    
    assert activity.description == "Test activity"
    assert len(activity.tags) == 2
    assert activity.id is not None


def test_get_all_activities(temp_storage):
    """Test retrieving all activities."""
    temp_storage.add_activity("Activity 1")
    temp_storage.add_activity("Activity 2")
    
    activities = temp_storage.get_all_activities()
    assert len(activities) == 2


def test_get_activities_with_tags(temp_storage):
    """Test filtering activities by tags."""
    temp_storage.add_activity("Work task", tags=["work"])
    temp_storage.add_activity("Personal task", tags=["personal"])
    temp_storage.add_activity("Work meeting", tags=["work", "meeting"])
    
    work_activities = temp_storage.get_activities(tags=["work"])
    assert len(work_activities) == 2


def test_create_task(temp_storage):
    """Test creating a task."""
    task = temp_storage.create_task(
        title="Test task",
        description="Test description",
        tags=["test"]
    )
    
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.status == "active"


def test_get_tasks(temp_storage):
    """Test retrieving tasks."""
    temp_storage.create_task("Task 1")
    temp_storage.create_task("Task 2")
    
    tasks = temp_storage.get_tasks()
    assert len(tasks) == 2


def test_get_tasks_by_status(temp_storage):
    """Test filtering tasks by status."""
    task1 = temp_storage.create_task("Active task")
    task2 = temp_storage.create_task("To be completed")
    
    temp_storage.complete_task(task2.id)
    
    active_tasks = temp_storage.get_tasks(status="active")
    completed_tasks = temp_storage.get_tasks(status="completed")
    
    assert len(active_tasks) == 1
    assert len(completed_tasks) == 1


def test_add_task_progress(temp_storage):
    """Test adding progress to a task."""
    task = temp_storage.create_task("Test task")
    
    updated_task = temp_storage.add_task_progress(
        task.id,
        50.0,
        "Halfway done"
    )
    
    assert updated_task is not None
    assert updated_task.current_progress == 50.0
    assert len(updated_task.progress_logs) == 1


def test_complete_task(temp_storage):
    """Test completing a task."""
    task = temp_storage.create_task("Test task")
    temp_storage.add_task_progress(task.id, 50.0)
    
    completed_task = temp_storage.complete_task(task.id)
    
    assert completed_task.status == "completed"
    assert completed_task.current_progress == 100.0


def test_cancel_task(temp_storage):
    """Test cancelling a task."""
    task = temp_storage.create_task("Test task")
    
    cancelled_task = temp_storage.cancel_task(task.id)
    
    assert cancelled_task.status == "cancelled"


def test_update_task(temp_storage):
    """Test updating a task."""
    task = temp_storage.create_task("Test task")
    task.description = "Updated description"
    
    temp_storage.update_task(task)
    
    retrieved_task = temp_storage.get_task(task.id)
    assert retrieved_task.description == "Updated description"
