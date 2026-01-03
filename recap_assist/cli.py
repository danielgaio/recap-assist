"""
CLI interface for recap-assist.
"""

import click
from datetime import datetime
from typing import Optional
from .storage import Storage
from .utils import parse_time_filter, format_datetime, format_date


@click.group()
@click.version_option(version="0.1.0")
def main():
    """
    Recap-Assist: A local, offline-first CLI agent to track activities and task progress.
    
    Track your daily activities, manage long-running tasks, and view progress over time.
    All data is stored locally on your machine.
    """
    pass


@main.command(name="log")
@click.argument("title")
@click.option("--description", "-d", help="Optional description")
@click.option("--tags", "-t", multiple=True, help="Tags for the entry")
def log(title: str, description: Optional[str], tags: tuple):
    """Log a completed activity."""
    storage = Storage()
    entry = storage.add_entry(
        title=title,
        description=description,
        status="done",
        tags=list(tags)
    )
    click.echo(f"✓ Logged: {entry.title}")
    click.echo(f"  ID: {entry.id}")
    click.echo(f"  Time: {format_datetime(datetime.fromisoformat(entry.timestamp))}")


@main.command(name="todo")
@click.argument("title")
@click.option("--description", "-d", help="Optional description")
@click.option("--tags", "-t", multiple=True, help="Tags for the entry")
def todo(title: str, description: Optional[str], tags: tuple):
    """Create a new active task."""
    storage = Storage()
    entry = storage.add_entry(
        title=title,
        description=description,
        status="active",
        tags=list(tags)
    )
    click.echo(f"✓ Added to TODO: {entry.title}")
    click.echo(f"  ID: {entry.id}")
    click.echo(f"  Status: {entry.status}")


@main.command(name="list")
@click.option("--filter", "-f", help="Time filter (last-week, last-month, etc.)")
@click.option("--status", "-s", type=click.Choice(["active", "done", "cancelled"]), help="Filter by status")
@click.option("--tags", "-t", multiple=True, help="Filter by tags")
@click.option("--limit", "-n", type=int, help="Limit number of results")
def list_entries(filter: Optional[str], status: Optional[str], tags: tuple, limit: Optional[int]):
    """List entries with optional filtering."""
    storage = Storage()
    
    # Parse time filter
    start_date = None
    end_date = None
    if filter:
        try:
            start_date, end_date = parse_time_filter(filter)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            return
    
    # Get entries
    entries = storage.get_entries(
        start_date=start_date,
        end_date=end_date,
        status=status,
        tags=list(tags) if tags else None
    )
    
    # Sort by timestamp (newest first)
    entries.sort(key=lambda e: e.timestamp, reverse=True)
    
    # Apply limit
    if limit:
        entries = entries[:limit]
    
    if not entries:
        click.echo("No entries found.")
        return
    
    # Display
    click.echo(f"\n📋 Found {len(entries)} entries:\n")
    for entry in entries:
        status_icon = "✓" if entry.status == "done" else "⏳" if entry.status == "active" else "✗"
        click.echo(f"{status_icon} {entry.title} [{entry.current_progress:.0f}%]")
        click.echo(f"  ID: {entry.id}")
        click.echo(f"  Status: {entry.status}")
        click.echo(f"  Time: {format_datetime(datetime.fromisoformat(entry.timestamp))}")
        if entry.tags:
            click.echo(f"  Tags: {', '.join(entry.tags)}")
        click.echo()


@main.command(name="progress")
@click.argument("entry_id")
@click.argument("percentage", type=float)
@click.option("--note", "-n", help="Optional note for this progress update")
def progress(entry_id: str, percentage: float, note: Optional[str]):
    """Add progress update to an entry."""
    if percentage < 0 or percentage > 100:
        click.echo("Error: Percentage must be between 0 and 100", err=True)
        return
    
    storage = Storage()
    entry = storage.add_progress(entry_id, percentage, note)
    
    if not entry:
        click.echo(f"Error: Entry not found: {entry_id}", err=True)
        return
    
    click.echo(f"✓ Progress updated for: {entry.title}")
    click.echo(f"  Progress: {percentage:.0f}%")
    if note:
        click.echo(f"  Note: {note}")


@main.command(name="complete")
@click.argument("entry_id")
def complete(entry_id: str):
    """Mark an entry as completed."""
    storage = Storage()
    entry = storage.complete_entry(entry_id)
    
    if not entry:
        click.echo(f"Error: Entry not found: {entry_id}", err=True)
        return
    
    click.echo(f"✓ Completed: {entry.title}")


@main.command(name="cancel")
@click.argument("entry_id")
def cancel(entry_id: str):
    """Mark an entry as cancelled."""
    storage = Storage()
    entry = storage.cancel_entry(entry_id)
    
    if not entry:
        click.echo(f"Error: Entry not found: {entry_id}", err=True)
        return
    
    click.echo(f"✗ Cancelled: {entry.title}")


@main.command(name="show")
@click.argument("entry_id")
def show(entry_id: str):
    """Show detailed information about an entry."""
    storage = Storage()
    entry = storage.get_entry(entry_id)
    
    if not entry:
        click.echo(f"Error: Entry not found: {entry_id}", err=True)
        return
    
    # Display details
    status_icon = "✓" if entry.status == "done" else "⏳" if entry.status == "active" else "✗"
    click.echo(f"\n{status_icon} {entry.title}")
    click.echo(f"\nID: {entry.id}")
    click.echo(f"Status: {entry.status}")
    click.echo(f"Created: {format_datetime(datetime.fromisoformat(entry.timestamp))}")
    click.echo(f"Current Progress: {entry.current_progress:.0f}%")
    
    if entry.description:
        click.echo(f"\nDescription: {entry.description}")
    
    if entry.tags:
        click.echo(f"Tags: {', '.join(entry.tags)}")
    
    # Display progress timeline
    if entry.progress_logs:
        click.echo(f"\n📊 Progress Timeline ({len(entry.progress_logs)} updates):\n")
        for log in entry.progress_logs:
            click.echo(f"  {format_datetime(datetime.fromisoformat(log.timestamp))} - {log.percentage:.0f}%")
            if log.note:
                click.echo(f"    Note: {log.note}")
    else:
        click.echo("\nNo progress updates yet.")


if __name__ == "__main__":
    main()
