"""Tests for data models."""

import pytest
from datetime import datetime
from recap_assist.models import Entry, ProgressLog


def test_entry_creation():
    """Test creating an entry."""
    entry = Entry(
        id="test-1",
        title="Test entry",
        description="Test description",
        timestamp=datetime.utcnow().isoformat(),
        status="active",
        tags=["work", "test"],
        metadata={"key": "value"}
    )
    
    assert entry.id == "test-1"
    assert entry.title == "Test entry"
    assert entry.description == "Test description"
    assert entry.status == "active"
    assert len(entry.tags) == 2
    assert entry.metadata["key"] == "value"


def test_entry_serialization():
    """Test entry to_dict and from_dict."""
    entry = Entry(
        id="test-1",
        title="Test entry",
        timestamp=datetime.utcnow().isoformat(),
        tags=["test"]
    )
    
    # Convert to dict and back
    entry_dict = entry.to_dict()
    restored = Entry.from_dict(entry_dict)
    
    assert restored.id == entry.id
    assert restored.title == entry.title
    assert restored.tags == entry.tags


def test_progress_log_creation():
    """Test creating a progress log."""
    log = ProgressLog(
        timestamp=datetime.utcnow().isoformat(),
        percentage=50.0,
        note="Halfway done"
    )
    
    assert log.percentage == 50.0
    assert log.note == "Halfway done"


def test_entry_add_progress():
    """Test adding progress to an entry."""
    entry = Entry(
        id="task-1",
        title="Test task",
        timestamp=datetime.utcnow().isoformat(),
        status="active"
    )
    
    entry.add_progress(25.0, "First update")
    entry.add_progress(75.0, "Second update")
    
    assert len(entry.progress_logs) == 2
    assert entry.current_progress == 75.0
    assert entry.progress_logs[0].percentage == 25.0
    assert entry.progress_logs[1].percentage == 75.0


def test_entry_serialization_with_progress():
    """Test entry to_dict and from_dict with progress logs."""
    entry = Entry(
        id="task-1",
        title="Test task",
        timestamp=datetime.utcnow().isoformat(),
        description="Test description"
    )
    entry.add_progress(50.0, "Halfway")
    
    # Convert to dict and back
    entry_dict = entry.to_dict()
    restored = Entry.from_dict(entry_dict)
    
    assert restored.id == entry.id
    assert restored.title == entry.title
    assert len(restored.progress_logs) == 1
    assert restored.current_progress == 50.0
