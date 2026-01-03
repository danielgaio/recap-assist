"""
Local storage layer for unified entries.
Uses SQLite for offline-first, local storage.
"""

import sqlite3
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import Entry, ProgressLog
import uuid


class Storage:
    """Manages local storage of entries using SQLite."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize storage with a data directory."""
        if data_dir is None:
            data_dir = os.path.join(os.path.expanduser("~"), ".recap")
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_file = self.data_dir / "recap.db"
        
        self._init_db()
    
    def _get_connection(self):
        """Get a database connection."""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                timestamp TEXT NOT NULL,
                status TEXT NOT NULL,
                metadata TEXT
            )
        """)
        
        # Create progress_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress_logs (
                entry_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                percentage REAL NOT NULL,
                note TEXT,
                FOREIGN KEY (entry_id) REFERENCES entries (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
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
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO entries (id, title, description, timestamp, status, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry.id,
            entry.title,
            entry.description,
            entry.timestamp,
            entry.status,
            json.dumps(entry.metadata)
        ))
        
        conn.commit()
        conn.close()
        
        return entry
    
    def _row_to_entry(self, row: sqlite3.Row, logs: List[sqlite3.Row]) -> Entry:
        """Convert DB rows to Entry object."""
        entry = Entry(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            timestamp=row['timestamp'],
            status=row['status'],
            metadata=json.loads(row['metadata']) if row['metadata'] else {}
        )
        
        entry.progress_logs = [
            ProgressLog(
                timestamp=log['timestamp'],
                percentage=log['percentage'],
                note=log['note']
            )
            for log in logs
        ]
        
        return entry

    def get_entries(self, start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   status: Optional[str] = None) -> List[Entry]:
        """Get entries with optional filtering."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM entries WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.isoformat())
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.isoformat())
        if status:
            query += " AND status = ?"
            params.append(status)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        entries = []
        for row in rows:
            # Fetch logs for each entry
            cursor.execute("SELECT * FROM progress_logs WHERE entry_id = ? ORDER BY timestamp", (row['id'],))
            log_rows = cursor.fetchall()
            entries.append(self._row_to_entry(row, log_rows))
            
        conn.close()
        return entries
    
    def get_entry(self, entry_id: str) -> Optional[Entry]:
        """Get an entry by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM entries WHERE id = ?", (entry_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
            
        cursor.execute("SELECT * FROM progress_logs WHERE entry_id = ? ORDER BY timestamp", (entry_id,))
        log_rows = cursor.fetchall()
        
        conn.close()
        return self._row_to_entry(row, log_rows)
    
    def update_entry(self, entry: Entry) -> None:
        """Update an entry's main fields."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE entries 
            SET title = ?, description = ?, status = ?, metadata = ?
            WHERE id = ?
        """, (
            entry.title,
            entry.description,
            entry.status,
            json.dumps(entry.metadata),
            entry.id
        ))
        
        conn.commit()
        conn.close()
    
    def add_progress(self, entry_id: str, percentage: float,
                    note: Optional[str] = None) -> Optional[Entry]:
        """Add progress to an entry."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Check if entry exists
        cursor.execute("SELECT id FROM entries WHERE id = ?", (entry_id,))
        if not cursor.fetchone():
            conn.close()
            return None
            
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO progress_logs (entry_id, timestamp, percentage, note)
            VALUES (?, ?, ?, ?)
        """, (
            entry_id,
            timestamp,
            percentage,
            note
        ))
        
        conn.commit()
        conn.close()
        
        return self.get_entry(entry_id)
    
    def complete_entry(self, entry_id: str) -> Optional[Entry]:
        """Mark an entry as completed."""
        entry = self.get_entry(entry_id)
        if not entry:
            return None
            
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Update status
        cursor.execute("UPDATE entries SET status = 'done' WHERE id = ?", (entry_id,))
        
        # Add 100% progress if needed
        if entry.current_progress < 100:
            timestamp = datetime.utcnow().isoformat()
            cursor.execute("""
                INSERT INTO progress_logs (entry_id, timestamp, percentage, note)
                VALUES (?, ?, ?, ?)
            """, (
                entry_id,
                timestamp,
                100.0,
                "Completed"
            ))
            
        conn.commit()
        conn.close()
        
        return self.get_entry(entry_id)
    
    def cancel_entry(self, entry_id: str) -> Optional[Entry]:
        """Mark an entry as cancelled."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE entries SET status = 'cancelled' WHERE id = ?", (entry_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return None
            
        conn.commit()
        conn.close()
        
        return self.get_entry(entry_id)
