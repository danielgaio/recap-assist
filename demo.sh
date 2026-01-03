#!/bin/bash
# Demo script showing recap-assist CLI features

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Recap-Assist CLI Demo                              ║"
echo "║    Local, Offline-First Activity & Task Tracker            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Clear existing data for a fresh demo
rm -rf ~/.recap

echo "📝 ACTIVITIES - Tracking what you've done"
echo "─────────────────────────────────────────────────────"
recap activity add "Completed project documentation" --tags work --tags documentation
recap activity add "Fixed bug in authentication flow" --tags work --tags bugfix
recap activity add "Team planning session" --tags meeting --tags planning
echo ""

echo "📋 Listing activities:"
recap activity list --limit 3
echo ""

echo "🎯 TASKS - Managing long-running work"
echo "─────────────────────────────────────────────────────"
recap task create "API Migration" --description "Migrate REST API to GraphQL" --tags backend --tags migration
TASK_ID=$(recap task list | grep -A1 "API Migration" | grep "ID:" | awk '{print $2}')
echo ""

echo "📈 Tracking progress on task:"
recap task progress "$TASK_ID" 25 --note "Created GraphQL schema"
recap task progress "$TASK_ID" 50 --note "Implemented resolvers"
recap task progress "$TASK_ID" 85 --note "Added tests and documentation"
echo ""

echo "📊 Viewing task with progress timeline:"
recap task show "$TASK_ID"
echo ""

echo "🔍 TIME-BASED QUERIES"
echo "─────────────────────────────────────────────────────"
echo "Activities from last week:"
recap activity list --filter last-week
echo ""

echo "✅ All active tasks:"
recap task list --status active
echo ""

echo "════════════════════════════════════════════════════════════"
echo "Demo complete! Try these commands yourself:"
echo "  recap activity add \"Your activity\" --tags tag1"
echo "  recap task create \"Your task\" --description \"Details\""
echo "  recap task progress <task-id> 50 --note \"Progress note\""
echo "  recap activity list --filter last-week"
echo "════════════════════════════════════════════════════════════"
