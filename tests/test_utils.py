"""Tests for utility functions."""

import pytest
from datetime import datetime, timedelta
from recap_assist.utils import (
    get_week_range,
    get_month_range,
    get_quarter_range,
    get_last_n_days,
    parse_time_filter,
    format_datetime,
    format_date
)


def test_get_last_n_days():
    """Test getting last N days range."""
    start, end = get_last_n_days(7)
    
    # Should be approximately 7 days apart
    delta = end - start
    assert delta.days >= 6 and delta.days <= 7


def test_get_week_range():
    """Test getting week range."""
    start, end = get_week_range(0)
    
    # Start should be a Monday
    assert start.weekday() == 0
    
    # Should span about 7 days
    delta = end - start
    assert delta.days >= 6 and delta.days <= 7


def test_get_month_range():
    """Test getting month range."""
    start, end = get_month_range(0)
    
    # Start should be first day of month
    assert start.day == 1
    
    # Should span at least 28 days
    delta = end - start
    assert delta.days >= 27


def test_get_quarter_range():
    """Test getting quarter range."""
    start, end = get_quarter_range(0)
    
    # Start should be first day of quarter month
    assert start.day == 1
    assert start.month in [1, 4, 7, 10]
    
    # Should span about 90 days
    delta = end - start
    assert delta.days >= 89 and delta.days <= 92


def test_parse_time_filter_week():
    """Test parsing week filter."""
    start, end = parse_time_filter("last-week")
    delta = end - start
    assert delta.days >= 6 and delta.days <= 7


def test_parse_time_filter_month():
    """Test parsing month filter."""
    start, end = parse_time_filter("last-month")
    delta = end - start
    assert delta.days == 30


def test_parse_time_filter_quarter():
    """Test parsing quarter filter."""
    start, end = parse_time_filter("last-quarter")
    delta = end - start
    assert delta.days == 90


def test_parse_time_filter_invalid():
    """Test parsing invalid filter raises error."""
    with pytest.raises(ValueError):
        parse_time_filter("invalid-filter")


def test_format_datetime():
    """Test datetime formatting."""
    dt = datetime(2026, 1, 3, 14, 30, 45)
    formatted = format_datetime(dt)
    assert formatted == "2026-01-03 14:30:45"


def test_format_date():
    """Test date formatting."""
    dt = datetime(2026, 1, 3, 14, 30, 45)
    formatted = format_date(dt)
    assert formatted == "2026-01-03"
