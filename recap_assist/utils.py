"""
Utilities for time-based queries and date handling.
"""

from datetime import datetime, timedelta
from typing import Tuple


def get_week_range(weeks_ago: int = 0) -> Tuple[datetime, datetime]:
    """Get the date range for a week (Monday to Sunday)."""
    now = datetime.utcnow()
    
    # Get the start of the current week (Monday)
    days_since_monday = now.weekday()
    start_of_current_week = now - timedelta(days=days_since_monday)
    start_of_current_week = start_of_current_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Calculate the target week
    start = start_of_current_week - timedelta(weeks=weeks_ago)
    end = start + timedelta(days=7) - timedelta(microseconds=1)
    
    return start, end


def get_month_range(months_ago: int = 0) -> Tuple[datetime, datetime]:
    """Get the date range for a month."""
    now = datetime.utcnow()
    
    # Calculate target month and year
    target_month = now.month - months_ago
    target_year = now.year
    
    while target_month <= 0:
        target_month += 12
        target_year -= 1
    
    # Start of the month
    start = datetime(target_year, target_month, 1, 0, 0, 0, 0)
    
    # End of the month
    if target_month == 12:
        end = datetime(target_year + 1, 1, 1, 0, 0, 0, 0) - timedelta(microseconds=1)
    else:
        end = datetime(target_year, target_month + 1, 1, 0, 0, 0, 0) - timedelta(microseconds=1)
    
    return start, end


def get_quarter_range(quarters_ago: int = 0) -> Tuple[datetime, datetime]:
    """Get the date range for a quarter (3 months)."""
    now = datetime.utcnow()
    
    # Determine current quarter (1-4)
    current_quarter = (now.month - 1) // 3 + 1
    
    # Calculate target quarter
    target_quarter = current_quarter - quarters_ago
    target_year = now.year
    
    while target_quarter <= 0:
        target_quarter += 4
        target_year -= 1
    
    # Start month of the quarter
    start_month = (target_quarter - 1) * 3 + 1
    start = datetime(target_year, start_month, 1, 0, 0, 0, 0)
    
    # End of the quarter
    end_month = start_month + 3
    if end_month > 12:
        end = datetime(target_year + 1, end_month - 12, 1, 0, 0, 0, 0) - timedelta(microseconds=1)
    else:
        end = datetime(target_year, end_month, 1, 0, 0, 0, 0) - timedelta(microseconds=1)
    
    return start, end


def get_last_n_days(days: int) -> Tuple[datetime, datetime]:
    """Get the date range for the last N days."""
    now = datetime.utcnow()
    start = now - timedelta(days=days)
    return start, now


def parse_time_filter(filter_str: str) -> Tuple[datetime, datetime]:
    """
    Parse a time filter string and return date range.
    
    Supported formats:
    - 'last-week' or 'week': Last 7 days from today
    - 'last-month' or 'month': Last 30 days from today
    - 'last-quarter' or 'quarter': Last 90 days from today
    - 'this-week': Current week (Monday to today)
    - 'this-month': Current month (1st to today)
    - 'this-quarter': Current quarter (start to today)
    """
    filter_str = filter_str.lower()
    
    if filter_str in ['last-week', 'week']:
        return get_last_n_days(7)
    elif filter_str in ['last-month', 'month']:
        return get_last_n_days(30)
    elif filter_str in ['last-quarter', 'quarter']:
        return get_last_n_days(90)
    elif filter_str == 'this-week':
        start, _ = get_week_range(0)
        return start, datetime.utcnow()
    elif filter_str == 'this-month':
        start, _ = get_month_range(0)
        return start, datetime.utcnow()
    elif filter_str == 'this-quarter':
        start, _ = get_quarter_range(0)
        return start, datetime.utcnow()
    else:
        raise ValueError(f"Unknown time filter: {filter_str}")


def format_datetime(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_date(dt: datetime) -> str:
    """Format date only for display."""
    return dt.strftime("%Y-%m-%d")
