"""
Data models for activities, tasks, and progress logs.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
import json


@dataclass
class Activity:
    """Timestamped record of things done."""
    id: str
    description: str
    timestamp: str  # ISO format
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Activity':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ProgressLog:
    """Dated update with completion percentage."""
    timestamp: str  # ISO format
    percentage: float  # 0-100
    note: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProgressLog':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Task:
    """Long-running action with progress tracking."""
    id: str
    title: str
    description: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    status: str = "active"  # active, completed, cancelled
    progress_logs: List[ProgressLog] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def current_progress(self) -> float:
        """Get the most recent progress percentage."""
        if not self.progress_logs:
            return 0.0
        return self.progress_logs[-1].percentage
    
    def add_progress(self, percentage: float, note: Optional[str] = None) -> None:
        """Add a progress update."""
        progress = ProgressLog(
            timestamp=datetime.utcnow().isoformat(),
            percentage=percentage,
            note=note
        )
        self.progress_logs.append(progress)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['progress_logs'] = [log.to_dict() for log in self.progress_logs]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create from dictionary."""
        progress_logs_data = data.pop('progress_logs', [])
        task = cls(**data)
        task.progress_logs = [ProgressLog.from_dict(log) for log in progress_logs_data]
        return task
