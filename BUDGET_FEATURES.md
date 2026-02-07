# 💰 Budget vs Actuals Features

## Overview
The new Budget vs Actuals tab provides comprehensive budget tracking and variance analysis across your entire organization, with drill-down capabilities by board and work type.

## Key Features

### 1. 📊 Overall Budget Summary (Top Metrics)
Four key metrics displayed at the top:
- **Total Estimated**: Sum of all estimated hours (from `likely_estimate` field)
- **Total Actual**: Sum of all actual time tracked
- **Variance**: Difference between actual and estimated (with percentage)
  - Shows as positive (over budget) or negative (under budget)
- **Items with Estimates**: Count of items that have time estimates

### 2. 📋 Budget Analysis by Board (Interactive Table)
Comprehensive table showing budget performance for each board:

**Columns:**
- Board Name
- Item Count
- Estimated Time
- Actual Time
- Variance (absolute)
- Variance % (percentage)
- Status (🔴 Over Budget / 🟢 Under Budget / ⚪ On Target)

**Features:**
- Sortable columns
- Scrollable for many boards
- Color-coded status indicators
- Human-readable time format (hours and minutes)

### 3. 📊 Visual Budget Comparison (Chart)
Side-by-side grouped bar chart showing:
- Estimated hours (light blue bars)
- Actual hours (dark blue bars)
- Easy visual comparison across all boards
- Hover for exact values

### 4. 🔍 Detailed Breakdown by Work Type
**Board Selector:**
- Dropdown to select any board for detailed analysis
- Analyzes work types within the selected board

**Work Type Budget Table:**
Shows for each work type:
- Item count
- Estimated time
- Actual time
- Variance (time and percentage)

**Distribution Pie Charts:**
Two side-by-side pie charts:
- **Left**: Estimated time distribution by work type
- **Right**: Actual time distribution by work type
- Compare how time was planned vs. how it was actually spent

### 5. ⚠️ Items with Largest Budget Variance
**Top 10 Items** with biggest differences between estimate and actual:

**Columns:**
- Item Number
- Title
- Work Type
- Assignee
- Estimated Time
- Actual Time
- Variance (absolute)
- Variance % (percentage)

**Use Cases:**
- Identify items that took much longer than expected
- Spot items that were completed faster than estimated
- Improve future estimates based on historical variance
- Find patterns in over/under estimation

### 6. 📥 Export Budget Analysis
**CSV Download** with complete budget data:
- All work items with estimates and actuals
- Variance calculations included
- Ready for further analysis in Excel/Google Sheets
- Filtered by your current dashboard filters

## How Budget is Calculated

### Estimated Time
Uses the `likely_estimate` field from work items:
- Stored in hours in the database
- Converted to seconds for comparison
- Middle estimate (between optimistic and pessimistic)

### Actual Time
Uses the `time_spent_seconds` field:
- Total time tracked on each work item
- Includes all time entries
- Automatically aggregated

### Variance
- **Formula**: Actual - Estimated
- **Positive variance**: Over budget (spent more time than estimated)
- **Negative variance**: Under budget (spent less time than estimated)
- **Percentage**: (Actual - Estimated) / Estimated × 100

## Use Cases

### 1. Project Health Monitoring
- Quickly identify which boards/projects are over or under budget
- See overall budget status at a glance
- Track variance trends over time

### 2. Resource Planning
- Understand where time is being spent
- Identify work types that consistently take longer than estimated
- Adjust future estimates based on historical data

### 3. Team Performance Review
- See which assignees have items with large variances
- Identify estimation accuracy by person or team
- Improve estimation skills through feedback

### 4. Sprint/Cycle Review
- Review budget performance for completed work
- Compare estimated vs actual for sprint planning
- Adjust velocity calculations

### 5. Client Reporting
- Export budget analysis for client reporting
- Show actual time vs estimates
- Justify budget overruns with detailed variance data

### 6. Continuous Improvement
- Identify patterns in estimation errors
- Find specific work types that are consistently mis-estimated
- Adjust estimation processes based on data

## Interactive Features

### Filters Apply Everywhere
All sidebar filters affect the Budget tab:
- **Date Range**: Only show items in selected period
- **Assignees**: See budget for specific people
- **Work Types**: Focus on specific types of work
- **Boards**: Pre-filter before viewing detailed analysis
- **Completion Status**: Compare completed vs in-progress

### Drill-Down Analysis
1. Start with Overall Summary (all boards)
2. View Budget by Board table (identify problem areas)
3. Select a specific board for detailed analysis
4. Examine work type distribution
5. Investigate individual items with largest variance

### Real-Time Updates
- All metrics update when filters change
- No page refresh needed
- Instant feedback on filter selections

## Color Coding

### Status Indicators
- 🔴 **Over Budget**: Red - Actual > Estimated
- 🟢 **Under Budget**: Green - Actual < Estimated
- ⚪ **On Target**: White - Actual ≈ Estimated (within small margin)

### Charts
- **Light Blue**: Estimated values (what was planned)
- **Dark Blue**: Actual values (what actually happened)
- Consistent color scheme across all visualizations

## Tips for Best Results

### 1. Ensure Estimates are Entered
- Budget analysis requires work items to have estimates
- The `likely_estimate` field should be populated
- Items without estimates won't show meaningful variance

### 2. Track Time Consistently
- Actual time comes from time entries
- Encourage team to track time on all work items
- More complete time tracking = more accurate variance

### 3. Use Appropriate Date Ranges
- Compare similar time periods (e.g., last sprint)
- Don't mix very old and very new data
- Use filters to focus on relevant timeframes

### 4. Review by Board
- Different boards may have different estimation accuracy
- Some projects may be more predictable than others
- Use board-level analysis to identify improvement areas

### 5. Export for Deeper Analysis
- Download CSV for pivot tables and advanced analysis
- Combine with other data sources
- Create custom reports in Excel/Sheets

## Limitations

### Items Without Estimates
- Items with no `likely_estimate` will show 0 hours estimated
- Variance will be 100% if actual time is tracked
- Filter to "Items with Estimates" for more meaningful analysis

### Work in Progress
- In-progress items may have partial time tracked
- Final variance will be different when completed
- Use "Completed" filter for final budget analysis

### Multiple Estimates
- Currently uses `likely_estimate` only
- `optimistic_estimate` and `pessimistic_estimate` not shown
- Could be added in future versions for PERT analysis

## Future Enhancements

Potential future additions:
- Trend analysis over time (variance trends by month)
- Forecast remaining work based on current variance
- Team/assignee comparison of estimation accuracy
- Budget alerts and thresholds
- PERT analysis using all three estimates
- Burndown charts with budget overlay
