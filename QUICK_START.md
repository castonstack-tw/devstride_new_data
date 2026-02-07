# Quick Start Guide

## Before You Start: Test the Connection

**Recommended:** Run the test script first to verify everything works:
```bash
python test_connection.py
```

This will check:
- Database connection
- All required tables are accessible
- Data can be loaded correctly

If all tests pass, you're ready to run the dashboard!

## Running the Dashboard

### Option 1: Using the Run Script (Recommended)
```bash
./run_dashboard.sh
```

### Option 2: Using Streamlit Directly
```bash
streamlit run streamlit_dashboard.py
```

## What to Expect

1. **Startup**: The dashboard will start and open in your default web browser at `http://localhost:8501`

2. **Loading**: Initial data load may take 5-10 seconds

3. **Main View**: You'll see:
   - 5 key metric cards at the top
   - Sidebar with filters on the left
   - 4 tabs with different visualizations

## Quick Tour

### Step 1: Key Metrics (Top of Page)
- **Total Work Items**: All items in the selected date range
- **Completed Items**: Successfully finished work
- **In Progress**: Current active work
- **Total Time Tracked**: All time logged on work items
- **Active Users**: Number of unique assignees

### Step 2: Filters (Left Sidebar)
Start with these common filters:
1. **Date Range**: Default is last 90 days
   - Click to change date range

2. **Users** → **Assignees**:
   - Select specific team members to see their work
   - Keep "All" selected to see everyone

3. **Completion Status**:
   - "All": See everything
   - "Completed": Only finished items
   - "In Progress": Only active items

### Step 3: Explore the Tabs

#### 📊 Overview Tab
- See work distribution by status (pie chart)
- View work types breakdown
- Track items created over time
- Analyze priority distribution

#### ⏱️ Time Tracking Tab
- See who logged the most time
- View time trends over days
- Check manual vs automatic entries
- Find top time-consuming items

#### 👥 Team Analysis Tab
- Compare team member workloads
- View completion rates by person
- See detailed performance metrics

#### 📋 Data Table Tab
- Browse all filtered work items
- Search for specific items
- Download data as CSV

## Common Use Cases

### 1. View Your Own Work
1. Go to sidebar → Assignees
2. Deselect "All"
3. Select your username
4. See your assigned work items

### 2. Weekly Team Review
1. Set date range to last 7 days
2. Go to Team Analysis tab
3. Review completion rates
4. Check time logged per person

### 3. Export Monthly Report
1. Set date range to last month
2. Apply any needed filters
3. Go to Data Table tab
4. Click "Download filtered data as CSV"

### 4. Track Project Progress
1. Select specific Board from filters
2. Go to Overview tab
3. View status pie chart
4. Check items created timeline

### 5. Find Specific Work Item
1. Go to Data Table tab
2. Use search box at top
3. Type item number, title, or any keyword
4. View filtered results

## Tips for Best Results

✅ **DO:**
- Start with broader filters, then narrow down
- Use the Overview tab first to get a general picture
- Export data for offline analysis
- Refresh page (F5) if data seems outdated

❌ **DON'T:**
- Apply too many filters at once initially
- Forget to check the date range
- Ignore the key metrics at the top

## Performance Notes

- Data is cached for 5 minutes for faster loading
- Larger date ranges may take longer to load
- All visualizations are interactive (hover for details)

## Need Help?

1. Check the full [README.md](README.md) for detailed information
2. Verify your filters aren't too restrictive
3. Try resetting all filters to "All"
4. Refresh the page to reload data

## Stopping the Dashboard

Press `Ctrl+C` in the terminal where it's running to stop the server.

---

**Ready to start?** Run `./run_dashboard.sh` and open http://localhost:8501 in your browser!
