"""
Local storage layer for activities and tasks.
Uses JSON files for offline-first, local storage.
"""

import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from .models import Activity, Task, ProgressLog
import uuid


class Storage:
    """Manages local storage of activities and tasks."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize storage with a data directory."""
        if data_dir is None:
            data_dir = os.path.join(os.path.expanduser("~"), ".recap")
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.activities_file = self.data_dir / "activities.json"
        self.tasks_file = self.data_dir / "tasks.json"
        
        # Initialize files if they don't exist
        self._ensure_files_exist()
    
    def _ensure_files_exist(self) -> None:
        """Ensure storage files exist."""
        if not self.activities_file.exists():
            self._write_json(self.activities_file, [])
        if not self.tasks_file.exists():
            self._write_json(self.tasks_file, [])
    
    def _read_json(self, filepath: Path) -> Any:
        """Read and parse JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def _write_json(self, filepath: Path, data: Any) -> None:
        """Write data to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Activity methods
    
    def add_activity(self, description: str, tags: Optional[List[str]] = None,
                    metadata: Optional[Dict[str, Any]] = None) -> Activity:
        """Add a new activity."""
        activity = Activity(
            id=str(uuid.uuid4()),
            description=description,
            timestamp=datetime.utcnow().isoformat(),
            tags=tags or [],
            metadata=metadata or {}
        )
        
        activities = self.get_all_activities()
        activities.append(activity.to_dict())
        self._write_json(self.activities_file, activities)
        
        return activity
    
    def get_all_activities(self) -> List[Dict[str, Any]]:
        """Get all activities as dictionaries."""
        return self._read_json(self.activities_file)
    
    def get_activities(self, start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None,
                      tags: Optional[List[str]] = None) -> List[Activity]:
        """Get activities with optional filtering."""
        activities_data = self.get_all_activities()
        activities = [Activity.from_dict(data) for data in activities_data]
        
        # Filter by date range
        if start_date:
            activities = [a for a in activities 
                         if datetime.fromisoformat(a.timestamp) >= start_date]
        if end_date:
            activities = [a for a in activities 
                         if datetime.fromisoformat(a.timestamp) <= end_date]
        
        # Filter by tags
        if tags:
            activities = [a for a in activities 
                         if any(tag in a.tags for tag in tags)]
        
        return activities
    
    # Task methods
    
    def create_task(self, title: str, description: Optional[str] = None,
                   tags: Optional[List[str]] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> Task:
        """Create a new task."""
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            created_at=datetime.utcnow().isoformat(),
            tags=tags or [],
            metadata=metadata or {}
        )
        
        tasks = self.get_all_tasks()
        tasks.append(task.to_dict())
        self._write_json(self.tasks_file, tasks)
        
        return task
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks as dictionaries."""
        return self._read_json(self.tasks_file)
    
    def get_tasks(self, status: Optional[str] = None,
                 tags: Optional[List[str]] = None) -> List[Task]:
        """Get tasks with optional filtering."""
        tasks_data = self.get_all_tasks()
        tasks = [Task.from_dict(data) for data in tasks_data]
        
        # Filter by status
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        # Filter by tags
        if tags:
            tasks = [t for t in tasks if any(tag in t.tags for tag in tags)]
        
        return tasks
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        tasks = self.get_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task: Task) -> None:
        """Update a task."""
        tasks_data = self.get_all_tasks()
        
        # Find and replace the task
        for i, task_data in enumerate(tasks_data):
            if task_data['id'] == task.id:
                tasks_data[i] = task.to_dict()
                break
        
        self._write_json(self.tasks_file, tasks_data)
    
    def add_task_progress(self, task_id: str, percentage: float,
                         note: Optional[str] = None) -> Optional[Task]:
        """Add progress to a task."""
        task = self.get_task(task_id)
        if task:
            task.add_progress(percentage, note)
            self.update_task(task)
            return task
        return None
    
    def complete_task(self, task_id: str) -> Optional[Task]:
        """Mark a task as completed."""
        task = self.get_task(task_id)
        if task:
            task.status = "completed"
            # Add 100% progress if not already there
            if task.current_progress < 100:
                task.add_progress(100.0, "Task completed")
            self.update_task(task)
            return task
        return None
    
    def cancel_task(self, task_id: str) -> Optional[Task]:
        """Mark a task as cancelled."""
        task = self.get_task(task_id)
        if task:
            task.status = "cancelled"
            self.update_task(task)
            return task
        return None
