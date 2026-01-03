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
    assert temp_storage.db_file.exists()


def test_add_entry(temp_storage):
    """Test adding an entry."""
    entry = temp_storage.add_entry(
        title="Test entry"
    )
    
    assert entry.title == "Test entry"
    assert entry.id is not None


def test_get_all_entries(temp_storage):
    """Test retrieving all entries."""
    temp_storage.add_entry("Entry 1")
    temp_storage.add_entry("Entry 2")
    
    entries = temp_storage.get_entries()
    assert len(entries) == 2


def test_create_active_entry(temp_storage):
    """Test creating an active entry (task)."""
    entry = temp_storage.add_entry(
        title="Test task",
        description="Test description",
        status="active"
    )
    
    assert entry.title == "Test task"
    assert entry.description == "Test description"
    assert entry.status == "active"


def test_get_entries_by_status(temp_storage):
    """Test filtering entries by status."""
    temp_storage.add_entry("Active task", status="active")
    temp_storage.add_entry("Completed task", status="done")
    
    active_entries = temp_storage.get_entries(status="active")
    completed_entries = temp_storage.get_entries(status="done")
    
    assert len(active_entries) == 1
    assert len(completed_entries) == 1


def test_add_progress(temp_storage):
    """Test adding progress to an entry."""
    entry = temp_storage.add_entry("Test task", status="active")
    
    updated_entry = temp_storage.add_progress(
        entry.id,
        50.0,
        "Halfway done"
    )
    
    assert updated_entry is not None
    assert updated_entry.current_progress == 50.0
    assert len(updated_entry.progress_logs) == 1


def test_complete_entry(temp_storage):
    """Test completing an entry."""
    entry = temp_storage.add_entry("Test task", status="active")
    temp_storage.add_progress(entry.id, 50.0)
    
    completed_entry = temp_storage.complete_entry(entry.id)
    
    assert completed_entry.status == "done"
    assert completed_entry.current_progress == 100.0


def test_cancel_entry(temp_storage):
    """Test cancelling an entry."""
    entry = temp_storage.add_entry("Test task", status="active")
    
    cancelled_entry = temp_storage.cancel_entry(entry.id)
    
    assert cancelled_entry.status == "cancelled"


def test_update_entry(temp_storage):
    """Test updating an entry."""
    entry = temp_storage.add_entry("Test task")
    entry.description = "Updated description"
    
    temp_storage.update_entry(entry)
    
    retrieved_entry = temp_storage.get_entry(entry.id)
    assert retrieved_entry.description == "Updated description"
