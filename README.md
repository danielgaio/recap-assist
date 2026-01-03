# recap-assist

A local, offline-first CLI agent to track activities and task progress.

## Features

- **Unified Entries**: Track both completed activities and active tasks
- **Progress Logs**: Dated updates with completion percentages
- **Time-based Queries**: Filter entries by last week/month/quarter
- **Progress Timelines**: View progress updates over time
- **Fully Local**: All data stored locally in `~/.recap/`
- **Offline-first**: No internet connection required
- **Clean CLI**: Simple, intuitive command-line interface

## Installation

```bash
# Clone the repository
git clone https://github.com/danielgaio/recap-assist.git
cd recap-assist

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Usage

### Logging Activities

Log things you've already done:

```bash
# Log a completed activity
recap log "Finished project documentation" --tags work --tags documentation
```

### Managing Tasks

Create and manage active tasks:

```bash
# Create a new active task
recap todo "Write API documentation" --description "Document all REST endpoints" --tags work

# List all entries (tasks and activities)
recap list

# List only active tasks
recap list --status active

# Add progress update (0-100%)
recap progress <entry-id> 25 --note "Completed authentication endpoints"

# Show entry details and progress timeline
recap show <entry-id>

# Mark entry as complete
recap complete <entry-id>

# Cancel an entry
recap cancel <entry-id>
```

### Time Filters

Supported time filter options:
- `last-week` or `week`: Last 7 days
- `last-month` or `month`: Last 30 days
- `last-quarter` or `quarter`: Last 90 days
- `this-week`: Current week (Monday to today)
- `this-month`: Current month (1st to today)
- `this-quarter`: Current quarter (start to today)

## Architecture

The project follows a clean, extensible architecture:

- **Models** (`models.py`): Data structures for unified Entries and Progress Logs
- **Storage** (`storage.py`): Local JSON-based persistence layer
- **Utils** (`utils.py`): Time-based query utilities
- **CLI** (`cli.py`): Command-line interface using Click

All data is stored locally in JSON files at `~/.recap/`:
- `entries.json`: All activity and task records

## Examples

### Daily Workflow

```bash
# Morning: Log what you did yesterday
recap log "Fixed bug in user authentication" --tags work --tags bugfix
recap log "Team standup meeting" --tags meeting

# During the day: Update task progress
recap progress abc-123 50 --note "Halfway through implementation"

# End of day: Review your entries
recap list --filter this-week

# Weekly review: Check active tasks
recap list --status active
recap show abc-123
```

### Monthly Recap

```bash
# See all entries from last month
recap list --filter last-month

# Review completed entries
recap list --status done
```

## Development

The project uses Python 3.8+ and has minimal dependencies (only `click` for CLI).

```bash
# Install in development mode
pip install -e .

# Run the CLI
recap --help
```

## License

MIT License
