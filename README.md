# DevStride Analytics Dashboard

A comprehensive Streamlit-based analytics dashboard for visualizing and analyzing DevStride project management data from PostgreSQL.

## Features

### 📊 Interactive Visualizations
- **Work Items Overview**: View distribution of work items by status, type, and priority
- **Time Tracking Analysis**: Analyze time logged by users and work items
- **Team Performance**: Monitor team productivity and completion rates
- **Interactive Data Table**: Browse, search, and filter all work items

### 🔍 Advanced Filters
The dashboard includes comprehensive filtering options:
- **Date Range**: Filter data by custom date ranges
- **Users**: Filter by assignees and authors
- **Work Types**: Filter by Bug, Epic, Capability, etc.
- **Priorities**: Filter by priority levels
- **Boards**: Filter by project boards
- **Lanes**: Filter by workflow status (To Do, In Progress, Done, etc.)
- **Completion Status**: View all items, completed only, or in-progress only

### 📈 Key Metrics
Real-time metrics displayed at the top:
- Total work items in selected range
- Completed items count
- In-progress items count
- Total time tracked
- Number of active users

### 📋 Data Export
- Download filtered data as CSV for further analysis
- Search functionality in data table

## Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database access (connection string provided)

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the dashboard**:
```bash
# Option 1: Using the provided script
chmod +x run_dashboard.sh
./run_dashboard.sh

# Option 2: Direct streamlit command
streamlit run streamlit_dashboard.py
```

3. **Access the dashboard**:
Open your web browser and navigate to:
```
http://localhost:8501
```

## Dashboard Tabs

### 1. 📊 Overview
- Work items by completion status (pie chart)
- Work items by type (bar chart)
- Work items created over time (line chart)
- Work items by priority (bar chart)

### 2. ⏱️ Time Tracking
- Time logged by user (bar chart)
- Time entries over time (area chart)
- Manual vs automatic time entries (pie chart)
- Top 10 work items by time spent (table)

### 3. 👥 Team Analysis
- Work items by assignee (horizontal bar chart)
- Completed items by assignee (horizontal bar chart)
- User performance summary table with:
  - Total items assigned
  - Completed items
  - In-progress items
  - Completion rate percentage
  - Total time spent

### 4. 📋 Data Table
- Full filterable and searchable data table
- All work items with details:
  - Number, Title, Assignee, Author
  - Type, Priority, Board, Lane, Status
  - Time spent, Created date, Completed date
- CSV export functionality

## Database Connection

The dashboard connects to a PostgreSQL database hosted on Neon.tech:
- Database: neondb
- Connection: Read-only access
- SSL: Required

The connection string is securely embedded in the application.

## Usage Tips

1. **Performance**: Data is cached for 5 minutes to improve performance. Refresh the page to reload data.

2. **Filtering**: Use the sidebar to apply multiple filters simultaneously. Select "All" to remove a filter.

3. **Date Range**: Default view shows the last 90 days. Adjust as needed for your analysis period.

4. **Export**: After applying filters, use the download button in the Data Table tab to export filtered results.

5. **Search**: Use the search box in the Data Table tab to find specific work items by any field.

## Technical Details

### Data Sources
- **workitems**: Main work items table (7,167 records)
- **time_entries**: Time tracking entries (5,744 records)
- **users**: User information (74 users)
- **work_types**: Types of work items (9 types)
- **priorities**: Priority levels
- **boards**: Project boards
- **lanes**: Workflow lanes/statuses

### Time Format
Time is displayed in hours and minutes format:
- Short format: "5.5h"
- Detailed format: "5h 30m"

### Color Schemes
- Status: Green (Completed), Orange (In Progress)
- Charts: Professional color schemes for better readability
- Work types: Blues palette
- Priorities: Reds palette
- Time tracking: Viridis and green scales

## Troubleshooting

### Dashboard won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### No data showing
- Verify database connection
- Check filter settings (reset all to "All")
- Ensure date range includes data

### Slow performance
- Reduce date range for faster queries
- Clear browser cache
- Restart the Streamlit server

## Support

For issues or questions about:
- **Data**: Contact your DevStride administrator
- **Dashboard**: Review this README or check Streamlit documentation
- **Database**: Verify connection credentials with your database admin

## Version

- Dashboard Version: 1.0.0
- Created: February 2026
- Last Updated: February 2026

## License

This dashboard is created for internal use with DevStride project management data.
