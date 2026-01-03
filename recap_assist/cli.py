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


# Activity commands

@main.group()
def activity():
    """Manage activities - timestamped records of things done."""
    pass


@activity.command(name="add")
@click.argument("description")
@click.option("--tags", "-t", multiple=True, help="Tags for the activity")
def activity_add(description: str, tags: tuple):
    """Add a new activity."""
    storage = Storage()
    activity = storage.add_activity(
        description=description,
        tags=list(tags)
    )
    click.echo(f"✓ Activity added: {activity.description}")
    click.echo(f"  ID: {activity.id}")
    click.echo(f"  Time: {format_datetime(datetime.fromisoformat(activity.timestamp))}")


@activity.command(name="list")
@click.option("--filter", "-f", help="Time filter (last-week, last-month, last-quarter)")
@click.option("--tags", "-t", multiple=True, help="Filter by tags")
@click.option("--limit", "-n", type=int, help="Limit number of results")
def activity_list(filter: Optional[str], tags: tuple, limit: Optional[int]):
    """List activities with optional filtering."""
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
    
    # Get activities
    activities = storage.get_activities(
        start_date=start_date,
        end_date=end_date,
        tags=list(tags) if tags else None
    )
    
    # Sort by timestamp (newest first)
    activities.sort(key=lambda a: a.timestamp, reverse=True)
    
    # Apply limit
    if limit:
        activities = activities[:limit]
    
    if not activities:
        click.echo("No activities found.")
        return
    
    # Display
    click.echo(f"\n📋 Found {len(activities)} activities:\n")
    for act in activities:
        click.echo(f"• {act.description}")
        click.echo(f"  {format_datetime(datetime.fromisoformat(act.timestamp))}")
        if act.tags:
            click.echo(f"  Tags: {', '.join(act.tags)}")
        click.echo()


# Task commands

@main.group()
def task():
    """Manage tasks - long-running actions with progress tracking."""
    pass


@task.command(name="create")
@click.argument("title")
@click.option("--description", "-d", help="Task description")
@click.option("--tags", "-t", multiple=True, help="Tags for the task")
def task_create(title: str, description: Optional[str], tags: tuple):
    """Create a new task."""
    storage = Storage()
    task = storage.create_task(
        title=title,
        description=description,
        tags=list(tags)
    )
    click.echo(f"✓ Task created: {task.title}")
    click.echo(f"  ID: {task.id}")
    click.echo(f"  Status: {task.status}")


@task.command(name="list")
@click.option("--status", "-s", type=click.Choice(["active", "completed", "cancelled"]), 
              help="Filter by status")
@click.option("--tags", "-t", multiple=True, help="Filter by tags")
def task_list(status: Optional[str], tags: tuple):
    """List tasks with optional filtering."""
    storage = Storage()
    
    tasks = storage.get_tasks(
        status=status,
        tags=list(tags) if tags else None
    )
    
    if not tasks:
        click.echo("No tasks found.")
        return
    
    # Sort by created date (newest first)
    tasks.sort(key=lambda t: t.created_at, reverse=True)
    
    click.echo(f"\n📝 Found {len(tasks)} tasks:\n")
    for t in tasks:
        status_icon = "✓" if t.status == "completed" else "⏳" if t.status == "active" else "✗"
        click.echo(f"{status_icon} {t.title} [{t.current_progress:.0f}%]")
        click.echo(f"  ID: {t.id}")
        click.echo(f"  Status: {t.status}")
        click.echo(f"  Created: {format_date(datetime.fromisoformat(t.created_at))}")
        if t.description:
            click.echo(f"  Description: {t.description}")
        if t.tags:
            click.echo(f"  Tags: {', '.join(t.tags)}")
        click.echo()


@task.command(name="progress")
@click.argument("task_id")
@click.argument("percentage", type=float)
@click.option("--note", "-n", help="Optional note for this progress update")
def task_progress(task_id: str, percentage: float, note: Optional[str]):
    """Add progress update to a task."""
    if percentage < 0 or percentage > 100:
        click.echo("Error: Percentage must be between 0 and 100", err=True)
        return
    
    storage = Storage()
    task = storage.add_task_progress(task_id, percentage, note)
    
    if not task:
        click.echo(f"Error: Task not found: {task_id}", err=True)
        return
    
    click.echo(f"✓ Progress updated for: {task.title}")
    click.echo(f"  Progress: {percentage:.0f}%")
    if note:
        click.echo(f"  Note: {note}")


@task.command(name="complete")
@click.argument("task_id")
def task_complete(task_id: str):
    """Mark a task as completed."""
    storage = Storage()
    task = storage.complete_task(task_id)
    
    if not task:
        click.echo(f"Error: Task not found: {task_id}", err=True)
        return
    
    click.echo(f"✓ Task completed: {task.title}")


@task.command(name="cancel")
@click.argument("task_id")
def task_cancel(task_id: str):
    """Mark a task as cancelled."""
    storage = Storage()
    task = storage.cancel_task(task_id)
    
    if not task:
        click.echo(f"Error: Task not found: {task_id}", err=True)
        return
    
    click.echo(f"✗ Task cancelled: {task.title}")


@task.command(name="show")
@click.argument("task_id")
def task_show(task_id: str):
    """Show detailed information about a task including progress timeline."""
    storage = Storage()
    task = storage.get_task(task_id)
    
    if not task:
        click.echo(f"Error: Task not found: {task_id}", err=True)
        return
    
    # Display task details
    status_icon = "✓" if task.status == "completed" else "⏳" if task.status == "active" else "✗"
    click.echo(f"\n{status_icon} {task.title}")
    click.echo(f"\nID: {task.id}")
    click.echo(f"Status: {task.status}")
    click.echo(f"Created: {format_datetime(datetime.fromisoformat(task.created_at))}")
    click.echo(f"Current Progress: {task.current_progress:.0f}%")
    
    if task.description:
        click.echo(f"\nDescription: {task.description}")
    
    if task.tags:
        click.echo(f"Tags: {', '.join(task.tags)}")
    
    # Display progress timeline
    if task.progress_logs:
        click.echo(f"\n📊 Progress Timeline ({len(task.progress_logs)} updates):\n")
        for log in task.progress_logs:
            click.echo(f"  {format_datetime(datetime.fromisoformat(log.timestamp))} - {log.percentage:.0f}%")
            if log.note:
                click.echo(f"    Note: {log.note}")
    else:
        click.echo("\nNo progress updates yet.")


if __name__ == "__main__":
    main()
