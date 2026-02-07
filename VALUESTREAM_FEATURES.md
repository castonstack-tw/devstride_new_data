# 🌳 Value Stream Hierarchy & Audit Features

## Overview
The dashboard now includes complete hierarchical navigation of value streams (folders) with the ability to drill down to the lowest level work items and audit specific value streams.

## New Features

### 1. 🌳 Complete Hierarchy View

**Location:** Budget vs Actuals tab → "Value Stream Hierarchy & Audit" section

**What it shows:**
- Full hierarchical folder structure from root to lowest level
- Parent → Child relationships visualized with indentation
- All work items at every level of the hierarchy
- Budget metrics (estimated, actual, variance) for each level

**Visual Hierarchy:**
```
📊 Parent Value Stream (10 items) - Est: 50h, Act: 55h
　📁 Child Value Stream 1 (5 items) - Est: 25h, Act: 28h
　　📂 Grandchild Value Stream (2 items) - Est: 10h, Act: 12h
　📁 Child Value Stream 2 (5 items) - Est: 25h, Act: 27h
```

**Icons by level:**
- 📊 Level 0 (Root/Parent)
- 📁 Level 1 (Child)
- 📂 Level 2+ (Grandchild and deeper)

### 2. 📍 Full Path Display

Each expanded value stream shows:
- **Path breadcrumb**: Shows complete path from root to current folder
- Example: `Arden Insurance > Open Order Management > Order Processing`

### 3. 🔍 Quick Search for Specific Value Streams

**How to use:**
1. Enter value stream name (e.g., "Open Order Management")
2. Dashboard finds all matching value streams
3. Shows complete results with:
   - Full path to each match
   - All work items in that value stream
   - Budget metrics
   - Last updated timestamps
   - Parent item relationships

**Perfect for auditing!**

### 4. 📋 Work Item Details at Every Level

For each value stream (at any level), you see:
- **Number** - Work item ID
- **Title** - Item description
- **Type** - Work type (Bug, Epic, etc.)
- **Assignee** - Who's responsible
- **Estimated** - Planned time
- **Actual** - Time spent
- **Variance** - Over/under budget
- **Status** - ✅ Complete or ⏳ In Progress
- **Last Updated** - When last modified
- **Parent Item** - Parent work item (if any)

### 5. 📊 Metrics at Each Level

Each value stream expander shows:
- **Total Items** - Count of work items
- **Completed** - Number finished
- **Estimated** - Total estimated time
- **Actual** - Total actual time
- **Variance %** - Budget variance percentage

### 6. 📂 Sub-folder Indicators

When a folder has children, it shows:
- List of immediate sub-folders
- Helps navigate the hierarchy
- Understand structure at a glance

## How to Audit "Open Order Management"

### Method 1: Using Search (Recommended)
1. Go to **Budget vs Actuals** tab
2. Scroll to **"Value Stream Hierarchy & Audit"**
3. Select your board from dropdown
4. Scroll to **"Search for Specific Value Stream"**
5. Type: `Open Order Management`
6. View results:
   - See full path
   - View all work items
   - Check budget metrics
   - Review last updated dates
   - Export if needed

### Method 2: Using Hierarchy Tree
1. Go to **Budget vs Actuals** tab
2. Scroll to **"Value Stream Hierarchy & Audit"**
3. Select your board
4. Browse **"Complete Hierarchy"** section
5. Click through parent folders to find "Open Order Management"
6. Expand to see all items

### Method 3: Using Original Drill-Down
1. Go to **Budget vs Actuals** tab
2. Use **"Detailed Board Drill-Down"** section
3. Select board
4. Find folder in list and expand

## Example Use Cases

### Use Case 1: Audit Specific Value Stream
**Goal:** Check status of "Open Order Management"

**Steps:**
1. Select board
2. Search for "Open Order Management"
3. Review metrics:
   - Are we over/under budget?
   - How many items completed?
   - When were items last updated?
4. Check individual items for blockers
5. Export data for reporting

### Use Case 2: Understand Full Hierarchy
**Goal:** See complete structure of work organization

**Steps:**
1. Select board
2. View "Complete Hierarchy"
3. Expand each level to understand:
   - How work is organized
   - Which value streams have most items
   - Where time is being spent
4. Identify areas needing attention

### Use Case 3: Find All Sub-Value Streams
**Goal:** See what's under a parent value stream

**Steps:**
1. Browse hierarchy tree
2. Expand parent folder
3. See list of sub-folders
4. Click each to see work items
5. Compare budget across sub-streams

### Use Case 4: Track Work Item Dependencies
**Goal:** See parent-child relationships between items

**Steps:**
1. Search for value stream
2. View "Parent Item" column
3. Identify which items depend on others
4. Check if parent items are completed
5. Unblock dependent work

## Data Shown

### Folder/Value Stream Information
- **Title** - Value stream name
- **Path** - Full hierarchical path
- **Level** - Depth in hierarchy (0 = root, 1 = child, etc.)
- **Item Count** - Direct work items
- **Child Folders** - Sub-value streams

### Work Item Information
- All standard work item fields
- Plus: Parent item reference
- Plus: Last updated timestamp
- Plus: Budget variance
- Plus: Completion status

## Tips for Best Results

### 1. Start with Search
If you know the value stream name, use search first:
- Faster than browsing hierarchy
- Shows exact matches
- Includes full context

### 2. Use Path Breadcrumbs
The path helps you understand:
- Where the value stream sits in organization
- Parent-child relationships
- Full context of the work

### 3. Check Last Updated
Use timestamps to find:
- Stale items (not updated recently)
- Active items (recently updated)
- Items needing attention

### 4. Review Parent Items
Parent item column shows:
- Dependencies between items
- Work breakdown structure
- Blocking relationships

### 5. Export for Deeper Analysis
After finding value stream:
- Review in dashboard
- Export to CSV
- Analyze in Excel
- Share with stakeholders

## Integration with Other Features

### Works with All Filters
- Date range filters apply
- User filters apply
- Work type filters apply
- Board filters apply

### Combined with Budget Analysis
- See budget metrics at each level
- Compare across value streams
- Identify over-budget areas
- Track variance by hierarchy level

### Enhanced by Debug Tab
- View folder schema
- Understand data structure
- Debug hierarchy issues
- Verify parent-child links

## Example Hierarchy

```
📊 Arden Insurance (Root)
　📁 Open Order Management (Level 1)
　　📂 Order Entry (Level 2)
　　　- I1234: Implement order form
　　　- I1235: Add validation
　　📂 Order Processing (Level 2)
　　　- I1236: Process orders
　　　- I1237: Send confirmations
　　📂 Order Fulfillment (Level 2)
　　　- I1238: Ship orders
　　　- I1239: Track shipments
　📁 Customer Service (Level 1)
　　📂 Support Tickets (Level 2)
　　　- I1240: Handle inquiries
　　　- I1241: Resolve issues
```

## Performance Notes

- Hierarchy is cached for 10 minutes
- Search is instant (client-side)
- Large hierarchies may take a moment to render
- Use search for deep hierarchies (5+ levels)

## Troubleshooting

### "No items found in folder hierarchy"
- Check board selection
- Verify date range includes work items
- Try removing filters

### "No value streams found matching"
- Check spelling
- Try partial name
- Browse hierarchy instead
- Check if items exist in selected board

### Hierarchy looks incomplete
- Some folders may be empty (hidden)
- Check if folders are archived
- Verify date filters

## Next Steps

After auditing a value stream:
1. **Identify issues** - Over budget, stale items, blockers
2. **Take action** - Reassign, update estimates, unblock
3. **Document findings** - Export data, share reports
4. **Follow up** - Re-audit periodically
5. **Improve estimates** - Learn from variances

## Quick Reference

**To audit "Open Order Management":**
```
1. Budget vs Actuals tab
2. Value Stream Hierarchy & Audit section
3. Select board
4. Search: "Open Order Management"
5. Review all items and metrics
6. Export if needed
```

**To explore full hierarchy:**
```
1. Budget vs Actuals tab
2. Value Stream Hierarchy & Audit section
3. Select board
4. Browse "Complete Hierarchy"
5. Click to expand each level
```

**To find specific item:**
```
1. Use search in value stream section
2. Or use main Data Table tab search
3. See which value stream it belongs to
4. Check its parent item
```
