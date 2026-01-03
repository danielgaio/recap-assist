# recap-assist

A local, offline-first CLI agent to track activities and task progress.

## Features

- **Activities**: Timestamped records of things you've done
- **Tasks**: Long-running actions with progress tracking
- **Progress Logs**: Dated updates with completion percentages
- **Time-based Queries**: Filter activities by last week/month/quarter
- **Task Progress Timelines**: View progress updates over time
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

### Activities

Track timestamped records of things you've done:

```bash
# Add an activity
recap activity add "Finished project documentation" --tags work --tags documentation

# List all activities
recap activity list

# List activities from the last week
recap activity list --filter last-week

# List activities with specific tags
recap activity list --tags work

# Limit results
recap activity list --limit 10
```

### Tasks

Manage long-running tasks with progress tracking:

```bash
# Create a new task
recap task create "Write API documentation" --description "Document all REST endpoints" --tags work

# List all tasks
recap task list

# List only active tasks
recap task list --status active

# Add progress update (0-100%)
recap task progress <task-id> 25 --note "Completed authentication endpoints"

# Show task details and progress timeline
recap task show <task-id>

# Mark task as complete
recap task complete <task-id>

# Cancel a task
recap task cancel <task-id>
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

- **Models** (`models.py`): Data structures for Activities, Tasks, and Progress Logs
- **Storage** (`storage.py`): Local JSON-based persistence layer
- **Utils** (`utils.py`): Time-based query utilities
- **CLI** (`cli.py`): Command-line interface using Click

All data is stored locally in JSON files at `~/.recap/`:
- `activities.json`: All activity records
- `tasks.json`: All task records with progress logs

## Examples

### Daily Workflow

```bash
# Morning: Log what you did yesterday
recap activity add "Fixed bug in user authentication" --tags work --tags bugfix
recap activity add "Team standup meeting" --tags meeting

# During the day: Update task progress
recap task progress abc-123 50 --note "Halfway through implementation"

# End of day: Review your activities
recap activity list --filter this-week

# Weekly review: Check task progress
recap task list --status active
recap task show abc-123
```

### Monthly Recap

```bash
# See all activities from last month
recap activity list --filter last-month

# Review completed tasks
recap task list --status completed
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
