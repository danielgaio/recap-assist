"""
Data models for activities, tasks, and progress logs.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict


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
class Entry:
    """Unified record for activities and tasks."""
    id: str
    title: str
    timestamp: str  # ISO format (creation time)
    description: Optional[str] = None
    status: str = "done"  # done, active, cancelled
    progress_logs: List[ProgressLog] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def current_progress(self) -> float:
        """Get the most recent progress percentage."""
        if not self.progress_logs:
            return 100.0 if self.status == "done" else 0.0
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
    def from_dict(cls, data: Dict[str, Any]) -> 'Entry':
        """Create from dictionary."""
        progress_logs_data = data.pop('progress_logs', [])
        entry = cls(**data)
        entry.progress_logs = [ProgressLog.from_dict(log) for log in progress_logs_data]
        return entry
