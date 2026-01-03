"""
Local storage layer for unified entries.
Uses JSON files for offline-first, local storage.
"""

import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import Entry, ProgressLog
import uuid


class Storage:
    """Manages local storage of entries."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize storage with a data directory."""
        if data_dir is None:
            data_dir = os.path.join(os.path.expanduser("~"), ".recap")
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.entries_file = self.data_dir / "entries.json"
        
        # Initialize file if it doesn't exist
        self._ensure_files_exist()
    
    def _ensure_files_exist(self) -> None:
        """Ensure storage files exist."""
        if not self.entries_file.exists():
            self._write_json(self.entries_file, [])
    
    def _read_json(self, filepath: Path) -> Any:
        """Read and parse JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def _write_json(self, filepath: Path, data: Any) -> None:
        """Write data to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Entry methods
    
    def add_entry(self, title: str, description: Optional[str] = None,
                 status: str = "done",
                 metadata: Optional[Dict[str, Any]] = None) -> Entry:
        """Add a new entry."""
        entry = Entry(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            timestamp=datetime.utcnow().isoformat(),
            status=status,
            metadata=metadata or {}
        )
        
        entries = self.get_all_entries_data()
        entries.append(entry.to_dict())
        self._write_json(self.entries_file, entries)
        
        return entry
    
    def get_all_entries_data(self) -> List[Dict[str, Any]]:
        """Get all entries as dictionaries."""
        return self._read_json(self.entries_file)
    
    def get_entries(self, start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   status: Optional[str] = None) -> List[Entry]:
        """Get entries with optional filtering."""
        entries_data = self.get_all_entries_data()
        entries = [Entry.from_dict(data) for data in entries_data]
        
        # Filter by date range
        if start_date:
            entries = [e for e in entries 
                      if datetime.fromisoformat(e.timestamp) >= start_date]
        if end_date:
            entries = [e for e in entries 
                      if datetime.fromisoformat(e.timestamp) <= end_date]
        
        # Filter by status
        if status:
            entries = [e for e in entries if e.status == status]
        
        return entries
    
    def get_entry(self, entry_id: str) -> Optional[Entry]:
        """Get an entry by ID."""
        entries = self.get_entries()
        for entry in entries:
            if entry.id == entry_id:
                return entry
        return None
    
    def update_entry(self, entry: Entry) -> None:
        """Update an entry."""
        entries_data = self.get_all_entries_data()
        
        # Find and replace the entry
        for i, entry_data in enumerate(entries_data):
            if entry_data['id'] == entry.id:
                entries_data[i] = entry.to_dict()
                break
        
        self._write_json(self.entries_file, entries_data)
    
    def add_progress(self, entry_id: str, percentage: float,
                    note: Optional[str] = None) -> Optional[Entry]:
        """Add progress to an entry."""
        entry = self.get_entry(entry_id)
        if entry:
            entry.add_progress(percentage, note)
            self.update_entry(entry)
            return entry
        return None
    
    def complete_entry(self, entry_id: str) -> Optional[Entry]:
        """Mark an entry as completed."""
        entry = self.get_entry(entry_id)
        if entry:
            entry.status = "done"
            # Add 100% progress if not already there
            if entry.current_progress < 100:
                entry.add_progress(100.0, "Completed")
            self.update_entry(entry)
            return entry
        return None
    
    def cancel_entry(self, entry_id: str) -> Optional[Entry]:
        """Mark an entry as cancelled."""
        entry = self.get_entry(entry_id)
        if entry:
            entry.status = "cancelled"
            self.update_entry(entry)
            return entry
        return None
