import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, inspect
from datetime import datetime, timedelta
import numpy as np
import json

# Page configuration
st.set_page_config(
    page_title="DevStride Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional styling with dark mode support
st.markdown("""
<style>
    /* ============= LIGHT MODE (Default) ============= */

    /* Tab styling - Light mode */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-radius: 10px;
        padding: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        border-radius: 8px;
        font-weight: 500;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600;
    }

    /* Metric cards */
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
    }

    /* Data tables */
    .dataframe thead tr th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.85rem;
        padding: 12px !important;
        border: none !important;
    }

    /* Section headers */
    h1, h2, h3 {
        font-weight: 700;
    }

    h2 {
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }

    /* Buttons */
    .stDownloadButton button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }

    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 2rem;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }

    /* Info/Alert boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }

    /* ============= DARK MODE OVERRIDES ============= */

    /* Dark mode detection for Streamlit */
    [data-testid="stAppViewContainer"][data-theme="dark"] .main,
    [data-testid="stApp"][class*="dark"] .main {
        background-color: #0e1117 !important;
    }

    /* Tab styling - Dark mode */
    [data-testid="stApp"][class*="dark"] .stTabs [data-baseweb="tab-list"],
    [data-theme="dark"] .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(38, 39, 48, 0.5);
    }

    [data-testid="stApp"][class*="dark"] .stTabs [data-baseweb="tab"],
    [data-theme="dark"] .stTabs [data-baseweb="tab"] {
        background-color: rgba(38, 39, 48, 0.8);
        color: #a0a0a0;
    }

    /* Sidebar - Dark mode */
    [data-testid="stApp"][class*="dark"] [data-testid="stSidebar"],
    [data-theme="dark"] [data-testid="stSidebar"] {
        background-color: #0e1117;
        border-right: 1px solid #262730;
    }

    /* Data tables - Dark mode */
    [data-testid="stApp"][class*="dark"] .dataframe tbody tr:nth-child(even),
    [data-theme="dark"] .dataframe tbody tr:nth-child(even) {
        background-color: rgba(38, 39, 48, 0.3);
    }

    [data-testid="stApp"][class*="dark"] .dataframe tbody tr:hover,
    [data-theme="dark"] .dataframe tbody tr:hover {
        background-color: rgba(102, 126, 234, 0.15);
    }

    [data-testid="stApp"][class*="dark"] .dataframe,
    [data-theme="dark"] .dataframe {
        color: #fafafa;
    }

    [data-testid="stApp"][class*="dark"] .dataframe tbody,
    [data-theme="dark"] .dataframe tbody {
        background-color: rgba(38, 39, 48, 0.5);
    }

    /* Expanders - Dark mode */
    [data-testid="stApp"][class*="dark"] div[data-testid="stExpander"],
    [data-theme="dark"] div[data-testid="stExpander"] {
        background-color: rgba(38, 39, 48, 0.5);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }

    /* Metric cards - Dark mode text */
    [data-testid="stApp"][class*="dark"] [data-testid="stMetricValue"],
    [data-theme="dark"] [data-testid="stMetricValue"] {
        color: #fafafa;
    }

    [data-testid="stApp"][class*="dark"] [data-testid="stMetricLabel"],
    [data-theme="dark"] [data-testid="stMetricLabel"] {
        color: #a0a0a0;
    }

    /* Universal dark mode fallback */
    @media (prefers-color-scheme: dark) {
        .stTabs [data-baseweb="tab"]:not([aria-selected="true"]) {
            background-color: rgba(38, 39, 48, 0.8) !important;
            color: #a0a0a0 !important;
        }

        .dataframe tbody tr:nth-child(even) {
            background-color: rgba(38, 39, 48, 0.3) !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_database_connection():
    connection_url = "postgresql://ds_ro_tenger_ways_bb3ecf37e53c6b6d:a7ZI3%24E%26Y01OUOBjwsH%23%24Zsaxb9iIBXJ@ep-mute-firefly-74914637-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    return create_engine(connection_url)

engine = get_database_connection()

# Helper function to format JSON fields
def format_json_field(json_text):
    """Format JSON text for readable display"""
    if pd.isna(json_text) or json_text is None or json_text == '':
        return '—'
    try:
        # Try to parse and pretty print JSON
        json_obj = json.loads(json_text) if isinstance(json_text, str) else json_text
        if isinstance(json_obj, dict):
            # For dict, show key-value pairs
            items = [f"{k}: {v}" for k, v in json_obj.items()]
            return ' | '.join(items) if items else '—'
        elif isinstance(json_obj, list):
            # For list, show items
            return ', '.join(str(item) for item in json_obj) if json_obj else '—'
        else:
            return str(json_obj)
    except (json.JSONDecodeError, TypeError, AttributeError):
        # If parsing fails, return as string (might already be formatted)
        return str(json_text) if json_text else '—'

# Load data with caching
@st.cache_data(ttl=300)
def load_workitems():
    # Try query with JSON fields first
    try:
        query = """
        SELECT
            w.id,
            w.number,
            w.title,
            w.assignee_username,
            w.author_username,
            w.completed_at,
            w.date_added,
            w.date_updated,
            w.start_date,
            w.due_date,
            w.time_spent_seconds,
            w.archived,
            w.work_type_id,
            w.lane_id,
            w.board_id,
            w.priority_id,
            w.optimistic_estimate,
            w.likely_estimate,
            w.pessimistic_estimate,
            w.point_effort,
            w.parent_number,
            w.root_folder_number,
            CASE
                WHEN w.custom_fields IS NOT NULL THEN w.custom_fields::text
                ELSE NULL
            END as custom_fields_text,
            CASE
                WHEN w.description IS NOT NULL THEN w.description::text
                ELSE NULL
            END as description_text,
            CASE
                WHEN w.tags IS NOT NULL THEN w.tags::text
                ELSE NULL
            END as tags_text
        FROM workitems w
        WHERE w.organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'
        """
        df = pd.read_sql(query, engine)
    except Exception as e:
        # Fall back to query without JSON fields if they don't exist
        st.warning(f"Note: Some JSON fields may not be available. Loading basic fields only.")
        query = """
        SELECT
            w.id,
            w.number,
            w.title,
            w.assignee_username,
            w.author_username,
            w.completed_at,
            w.date_added,
            w.date_updated,
            w.start_date,
            w.due_date,
            w.time_spent_seconds,
            w.archived,
            w.work_type_id,
            w.lane_id,
            w.board_id,
            w.priority_id,
            w.optimistic_estimate,
            w.likely_estimate,
            w.pessimistic_estimate,
            w.point_effort,
            w.parent_number,
            w.root_folder_number
        FROM workitems w
        WHERE w.organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'
        """
        df = pd.read_sql(query, engine)

    df['date_added'] = pd.to_datetime(df['date_added'])
    df['date_updated'] = pd.to_datetime(df['date_updated'])
    df['completed_at'] = pd.to_datetime(df['completed_at'])
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['due_date'] = pd.to_datetime(df['due_date'])
    return df

@st.cache_data(ttl=300)
def load_time_entries():
    query = """
    SELECT
        te.id,
        te.author_username,
        te.item_number,
        te.description,
        te.start_date,
        te.end_date,
        te.length_seconds,
        te.completed,
        te.manual,
        te.date_added
    FROM time_entries te
    WHERE te.organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'
    """
    df = pd.read_sql(query, engine)
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df['date_added'] = pd.to_datetime(df['date_added'])
    return df

@st.cache_data(ttl=600)
def load_users():
    query = "SELECT username, first_name, last_name, email FROM users"
    return pd.read_sql(query, engine)

@st.cache_data(ttl=600)
def load_work_types():
    query = "SELECT id, name, color FROM work_types WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
    return pd.read_sql(query, engine)

@st.cache_data(ttl=600)
def load_priorities():
    query = "SELECT id, name, color FROM priorities WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
    return pd.read_sql(query, engine)

@st.cache_data(ttl=600)
def load_boards():
    query = "SELECT id, label FROM boards WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
    return pd.read_sql(query, engine)

@st.cache_data(ttl=600)
def load_lanes():
    query = "SELECT id, name, color FROM lanes WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
    return pd.read_sql(query, engine)

@st.cache_data(ttl=600)
def load_folders():
    # Try query with JSON fields first
    try:
        query = """
        SELECT
            id,
            number,
            title,
            parent_number,
            item_count,
            date_added,
            date_updated,
            CASE
                WHEN hierarchy IS NOT NULL THEN hierarchy::text
                ELSE NULL
            END as hierarchy_text,
            CASE
                WHEN hierarchy_path IS NOT NULL THEN hierarchy_path::text
                ELSE NULL
            END as hierarchy_path_text
        FROM folders
        WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'
        AND archived = false
        """
        return pd.read_sql(query, engine)
    except Exception:
        # Fall back to query without JSON fields if they don't exist
        query = """
        SELECT
            id,
            number,
            title,
            parent_number,
            item_count,
            date_added,
            date_updated
        FROM folders
        WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'
        AND archived = false
        """
        return pd.read_sql(query, engine)

@st.cache_data(ttl=3600)
def get_database_schema():
    """Get schema information for all tables"""
    inspector = inspect(engine)
    schema_info = {}

    tables = ['workitems', 'time_entries', 'users', 'work_types', 'priorities',
              'boards', 'lanes', 'folders', 'teams']

    for table in tables:
        try:
            columns = inspector.get_columns(table)
            schema_info[table] = {
                'columns': [
                    {
                        'name': col['name'],
                        'type': str(col['type']),
                        'nullable': col.get('nullable', 'unknown')
                    }
                    for col in columns
                ]
            }
            # Get row count
            try:
                count_query = f"SELECT COUNT(*) as count FROM {table}"
                if table not in ['users', 'teams']:
                    count_query += " WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
                result = pd.read_sql(count_query, engine)
                schema_info[table]['row_count'] = result['count'].iloc[0]
            except:
                schema_info[table]['row_count'] = 'N/A'
        except Exception as e:
            schema_info[table] = {'error': str(e)}

    return schema_info

# Helper functions
def format_seconds(seconds):
    """Convert seconds to human readable format"""
    if pd.isna(seconds) or seconds == 0:
        return "0h"
    hours = seconds / 3600
    if hours < 1:
        return f"{int(seconds/60)}m"
    return f"{hours:.1f}h"

def format_time_detailed(seconds):
    """Convert seconds to detailed time format"""
    if pd.isna(seconds) or seconds == 0:
        return "0h 0m"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours}h {minutes}m"

def calculate_variance(actual, estimated):
    """Calculate variance percentage"""
    if pd.isna(estimated) or estimated == 0:
        return 0
    if pd.isna(actual):
        actual = 0
    variance = ((actual - estimated) / estimated) * 100
    return variance

def format_variance(variance):
    """Format variance with color indicator"""
    if variance > 0:
        return f"+{variance:.1f}%"
    return f"{variance:.1f}%"

def format_datetime(dt):
    """Format datetime for display"""
    if pd.isna(dt):
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# Professional chart theme
def get_chart_theme():
    """Return professional chart theme colors"""
    return {
        'primary': ['#667eea', '#764ba2', '#f093fb', '#4facfe'],
        'gradient': ['#667eea', '#7c6beb', '#9259ec', '#a746ed', '#bd33ee'],
        'success': ['#10b981', '#059669', '#047857'],
        'warning': ['#f59e0b', '#d97706', '#b45309'],
        'danger': ['#ef4444', '#dc2626', '#b91c1c'],
        'neutral': ['#64748b', '#475569', '#334155']
    }

def apply_chart_template(fig, title=""):
    """Apply professional template to plotly charts"""
    fig.update_layout(
        template='plotly_white',
        title={
            'text': title,
            'font': {'size': 20, 'color': '#1e293b', 'family': 'Arial, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        font={'family': 'Arial, sans-serif', 'size': 12, 'color': '#475569'},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, b=40, l=40, r=40),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial, sans-serif"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#e2e8f0',
            borderwidth=1
        )
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    return fig

def create_metric_card(label, value, icon="📊", delta=None, delta_color="normal"):
    """Create a professional metric card with HTML/CSS"""
    delta_html = ""
    if delta:
        color = "#10b981" if delta_color == "positive" else "#ef4444" if delta_color == "negative" else "#64748b"
        arrow = "↑" if delta_color == "positive" else "↓" if delta_color == "negative" else ""
        delta_html = f'<div style="color: {color}; font-size: 0.9rem; margin-top: 0.5rem;">{arrow} {delta}</div>'

    card_html = f"""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); border-left: 4px solid #667eea; height: 100%;">
        <div style="color: #64748b; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; margin-bottom: 0.5rem;">
            {icon} {label}
        </div>
        <div style="color: #1e293b; font-size: 2rem; font-weight: 700;">
            {value}
        </div>
        {delta_html}
    </div>
    """
    return card_html

def build_folder_hierarchy(folders_df):
    """Build hierarchical folder structure"""
    # Create a dictionary for quick lookup
    folder_dict = {}
    for _, folder in folders_df.iterrows():
        folder_dict[folder['number']] = {
            'title': folder['title'],
            'parent': folder['parent_number'],
            'item_count': folder['item_count'],
            'children': [],
            'level': 0
        }

    # Build parent-child relationships
    root_folders = []
    for number, folder_info in folder_dict.items():
        parent = folder_info['parent']
        if pd.isna(parent) or parent not in folder_dict:
            root_folders.append(number)
        else:
            folder_dict[parent]['children'].append(number)

    # Calculate levels
    def set_level(folder_num, level=0):
        folder_dict[folder_num]['level'] = level
        for child in folder_dict[folder_num]['children']:
            set_level(child, level + 1)

    for root in root_folders:
        set_level(root)

    return folder_dict, root_folders

def get_folder_path(folder_number, folder_dict):
    """Get the full path of a folder from root"""
    path = []
    current = folder_number
    while current and current in folder_dict:
        path.insert(0, folder_dict[current]['title'])
        parent = folder_dict[current]['parent']
        if pd.isna(parent):
            break
        current = parent
    return ' > '.join(path)

# Main app
def main():
    # Professional header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h1 style="color: white; font-size: 2.5rem; font-weight: 700; margin: 0; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);">📊 DevStride Analytics</h1>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.1rem; margin-top: 0.5rem; margin-bottom: 0;">Real-time Work Item & Budget Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    with st.spinner("Loading data..."):
        df_workitems = load_workitems()
        df_time_entries = load_time_entries()
        df_users = load_users()
        df_work_types = load_work_types()
        df_priorities = load_priorities()
        df_boards = load_boards()
        df_lanes = load_lanes()
        df_folders = load_folders()

    # Sidebar filters
    st.sidebar.header("🔍 Filters")

    # Date range filter
    st.sidebar.subheader("Date Range")
    min_date = df_workitems['date_added'].min().date()
    max_date = df_workitems['date_added'].max().date()

    # Calculate rolling Sunday to Sunday for last 2 weeks
    today = datetime.now().date()
    # Find the most recent Sunday (or today if it's Sunday)
    days_since_sunday = (today.weekday() + 1) % 7  # Monday=1, Sunday=0
    last_sunday = today - timedelta(days=days_since_sunday)
    two_weeks_ago_sunday = last_sunday - timedelta(days=14)

    # Ensure calculated dates are within data range
    default_end = min(last_sunday, max_date)
    default_start = max(two_weeks_ago_sunday, min_date)
    # If start would be after end, use last 14 days of available data
    if default_start > default_end:
        default_end = max_date
        default_start = max(max_date - timedelta(days=14), min_date)

    date_range = st.sidebar.date_input(
        "Select date range",
        value=(default_start, default_end),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

    # User filters
    st.sidebar.subheader("Users")
    all_assignees = sorted(df_workitems['assignee_username'].dropna().unique())
    selected_assignees = st.sidebar.multiselect(
        "Assignees",
        options=["All"] + all_assignees,
        default=["All"]
    )

    all_authors = sorted(df_workitems['author_username'].dropna().unique())
    selected_authors = st.sidebar.multiselect(
        "Authors",
        options=["All"] + all_authors,
        default=["All"]
    )

    # Work type filter
    work_type_names = df_work_types[['id', 'name']].set_index('id')['name'].to_dict()
    selected_work_types = st.sidebar.multiselect(
        "Work Types",
        options=["All"] + list(work_type_names.values()),
        default=["All"]
    )

    # Priority filter
    priority_names = df_priorities[['id', 'name']].set_index('id')['name'].to_dict()
    selected_priorities = st.sidebar.multiselect(
        "Priorities",
        options=["All"] + list(priority_names.values()),
        default=["All"]
    )

    # Board filter
    board_names = df_boards[['id', 'label']].set_index('id')['label'].to_dict()
    selected_boards = st.sidebar.multiselect(
        "Boards",
        options=["All"] + list(board_names.values()),
        default=["All"]
    )

    # Lane filter
    lane_names = df_lanes[['id', 'name']].set_index('id')['name'].to_dict()
    selected_lanes = st.sidebar.multiselect(
        "Lanes (Status)",
        options=["All"] + list(lane_names.values()),
        default=["All"]
    )

    # Completion status filter
    completion_filter = st.sidebar.radio(
        "Completion Status",
        options=["All", "Completed", "In Progress"],
        index=0
    )

    # Apply filters
    filtered_workitems = df_workitems.copy()

    # Exclude archived workitems
    filtered_workitems = filtered_workitems[filtered_workitems['archived'] != True]

    # Date filter
    filtered_workitems = filtered_workitems[
        (filtered_workitems['date_added'].dt.date >= start_date) &
        (filtered_workitems['date_added'].dt.date <= end_date)
    ]

    # User filters
    if "All" not in selected_assignees:
        filtered_workitems = filtered_workitems[filtered_workitems['assignee_username'].isin(selected_assignees)]

    if "All" not in selected_authors:
        filtered_workitems = filtered_workitems[filtered_workitems['author_username'].isin(selected_authors)]

    # Work type filter
    if "All" not in selected_work_types:
        work_type_ids = [k for k, v in work_type_names.items() if v in selected_work_types]
        filtered_workitems = filtered_workitems[filtered_workitems['work_type_id'].isin(work_type_ids)]

    # Priority filter
    if "All" not in selected_priorities:
        priority_ids = [k for k, v in priority_names.items() if v in selected_priorities]
        filtered_workitems = filtered_workitems[filtered_workitems['priority_id'].isin(priority_ids)]

    # Board filter
    if "All" not in selected_boards:
        board_ids = [k for k, v in board_names.items() if v in selected_boards]
        filtered_workitems = filtered_workitems[filtered_workitems['board_id'].isin(board_ids)]

    # Lane filter
    if "All" not in selected_lanes:
        lane_ids = [k for k, v in lane_names.items() if v in selected_lanes]
        filtered_workitems = filtered_workitems[filtered_workitems['lane_id'].isin(lane_ids)]

    # Completion filter
    if completion_filter == "Completed":
        filtered_workitems = filtered_workitems[filtered_workitems['completed_at'].notna()]
    elif completion_filter == "In Progress":
        filtered_workitems = filtered_workitems[filtered_workitems['completed_at'].isna()]

    # Filter time entries based on same date range
    filtered_time_entries = df_time_entries[
        (df_time_entries['start_date'].dt.date >= start_date) &
        (df_time_entries['start_date'].dt.date <= end_date)
    ]

    if "All" not in selected_assignees:
        filtered_time_entries = filtered_time_entries[filtered_time_entries['author_username'].isin(selected_assignees)]

    # Key Metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Work Items", len(filtered_workitems))

    with col2:
        completed_items = len(filtered_workitems[filtered_workitems['completed_at'].notna()])
        st.metric("Completed Items", completed_items)

    with col3:
        in_progress = len(filtered_workitems[filtered_workitems['completed_at'].isna()])
        st.metric("In Progress", in_progress)

    with col4:
        total_time = filtered_workitems['time_spent_seconds'].sum()
        st.metric("Total Time Tracked", format_time_detailed(total_time))

    with col5:
        unique_assignees = filtered_workitems['assignee_username'].nunique()
        st.metric("Active Users", unique_assignees)

    st.markdown("---")

    # Visualizations
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Overview",
        "⏱️ Time Tracking",
        "👥 Team Analysis",
        "💰 Budget vs Actuals",
        "⚠️ Stale Items",
        "📋 Data Table",
        "🔧 Debug/Schema"
    ])

    with tab1:
        st.header("Work Items Overview")

        col1, col2 = st.columns(2)

        with col1:
            # Work items by completion status
            st.subheader("Work Items by Status")
            status_data = pd.DataFrame({
                'Status': ['Completed', 'In Progress'],
                'Count': [
                    len(filtered_workitems[filtered_workitems['completed_at'].notna()]),
                    len(filtered_workitems[filtered_workitems['completed_at'].isna()])
                ]
            })
            fig = px.pie(status_data, values='Count', names='Status',
                        color='Status',
                        color_discrete_map={'Completed': '#10b981', 'In Progress': '#f59e0b'},
                        hole=0.4)
            fig = apply_chart_template(fig, "")
            fig.update_traces(textposition='inside', textinfo='percent+label',
                            marker=dict(line=dict(color='white', width=2)))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Work items by work type
            st.subheader("Work Items by Type")
            workitems_with_type = filtered_workitems.copy()
            workitems_with_type['work_type_name'] = workitems_with_type['work_type_id'].map(work_type_names)
            type_counts = workitems_with_type['work_type_name'].value_counts()
            if len(type_counts) > 0:
                colors = get_chart_theme()
                fig = px.bar(x=type_counts.index, y=type_counts.values,
                            labels={'x': 'Work Type', 'y': 'Count'})
                fig.update_traces(marker_color=colors['primary'][0],
                                marker_line_color='white',
                                marker_line_width=1.5)
                fig = apply_chart_template(fig, "")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No work type data available")

        # Work items timeline
        st.subheader("Work Items Created Over Time")
        timeline_data = filtered_workitems.copy()
        timeline_data['date'] = timeline_data['date_added'].dt.date
        daily_counts = timeline_data.groupby('date').size().reset_index(name='count')
        if len(daily_counts) > 0:
            fig = px.line(daily_counts, x='date', y='count',
                         labels={'date': 'Date', 'count': 'Work Items Created'},
                         markers=True)
            fig.update_traces(line_color='#636EFA')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No timeline data available")

        # Work items by priority
        st.subheader("Work Items by Priority")
        workitems_with_priority = filtered_workitems.copy()
        workitems_with_priority['priority_name'] = workitems_with_priority['priority_id'].map(priority_names)
        priority_counts = workitems_with_priority['priority_name'].value_counts()
        if len(priority_counts) > 0:
            fig = px.bar(x=priority_counts.index, y=priority_counts.values,
                        labels={'x': 'Priority', 'y': 'Count'},
                        color=priority_counts.values,
                        color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No priority data available")

    with tab2:
        st.header("Time Tracking Analysis")

        # Time by user
        st.subheader("Time Logged by User")
        if len(filtered_time_entries) > 0:
            time_by_user = filtered_time_entries.groupby('author_username')['length_seconds'].sum().sort_values(ascending=False)
            time_by_user_hours = time_by_user / 3600

            fig = px.bar(x=time_by_user_hours.index, y=time_by_user_hours.values,
                        labels={'x': 'User', 'y': 'Hours'},
                        color=time_by_user_hours.values,
                        color_continuous_scale='Viridis')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No time tracking data available for selected filters")

        col1, col2 = st.columns(2)

        with col1:
            # Time entries over time
            st.subheader("Time Entries Over Time")
            if len(filtered_time_entries) > 0:
                time_timeline = filtered_time_entries.copy()
                time_timeline['date'] = time_timeline['start_date'].dt.date
                daily_time = time_timeline.groupby('date')['length_seconds'].sum() / 3600
                fig = px.area(x=daily_time.index, y=daily_time.values,
                             labels={'x': 'Date', 'y': 'Hours Logged'})
                fig.update_traces(line_color='#00CC96', fillcolor='rgba(0, 204, 150, 0.3)')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No time entry data available")

        with col2:
            # Manual vs automatic time entries
            st.subheader("Time Entry Types")
            if len(filtered_time_entries) > 0:
                entry_types = filtered_time_entries['manual'].value_counts()
                entry_types.index = ['Manual' if x else 'Automatic' for x in entry_types.index]
                fig = px.pie(values=entry_types.values, names=entry_types.index,
                            color_discrete_sequence=['#AB63FA', '#19D3F3'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No time entry type data available")

        # Top items by time spent
        st.subheader("Top 10 Work Items by Time Spent")
        if len(filtered_workitems[filtered_workitems['time_spent_seconds'] > 0]) > 0:
            top_items = filtered_workitems.nlargest(10, 'time_spent_seconds')[['number', 'title', 'assignee_username', 'time_spent_seconds', 'date_updated']]
            top_items['time_spent'] = top_items['time_spent_seconds'].apply(format_time_detailed)
            top_items['last_updated'] = top_items['date_updated'].apply(format_datetime)
            top_items = top_items[['number', 'title', 'assignee_username', 'time_spent', 'last_updated']]
            st.dataframe(top_items, use_container_width=True, hide_index=True)
        else:
            st.info("No time spent data available")

    with tab3:
        st.header("Team Performance Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # Work items by assignee
            st.subheader("Work Items by Assignee")
            if len(filtered_workitems['assignee_username'].dropna()) > 0:
                assignee_counts = filtered_workitems['assignee_username'].value_counts().head(15)
                fig = px.bar(x=assignee_counts.values, y=assignee_counts.index,
                            labels={'x': 'Work Items', 'y': 'Assignee'},
                            orientation='h',
                            color=assignee_counts.values,
                            color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No assignee data available")

        with col2:
            # Completed items by assignee
            st.subheader("Completed Items by Assignee")
            completed = filtered_workitems[filtered_workitems['completed_at'].notna()]
            if len(completed['assignee_username'].dropna()) > 0:
                completed_counts = completed['assignee_username'].value_counts().head(15)
                fig = px.bar(x=completed_counts.values, y=completed_counts.index,
                            labels={'x': 'Completed Items', 'y': 'Assignee'},
                            orientation='h',
                            color=completed_counts.values,
                            color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No completed items data available")

        # User performance table
        st.subheader("User Performance Summary")
        if len(filtered_workitems['assignee_username'].dropna()) > 0:
            user_stats = []
            for user in filtered_workitems['assignee_username'].dropna().unique():
                user_items = filtered_workitems[filtered_workitems['assignee_username'] == user]
                completed = len(user_items[user_items['completed_at'].notna()])
                total = len(user_items)
                time_spent = user_items['time_spent_seconds'].sum()

                user_stats.append({
                    'User': user,
                    'Total Items': total,
                    'Completed': completed,
                    'In Progress': total - completed,
                    'Completion Rate': f"{(completed/total*100):.1f}%" if total > 0 else "0%",
                    'Total Time': format_time_detailed(time_spent)
                })

            user_stats_df = pd.DataFrame(user_stats).sort_values('Total Items', ascending=False)
            st.dataframe(user_stats_df, use_container_width=True, hide_index=True)
        else:
            st.info("No user performance data available")

    with tab4:
        st.header("💰 Budget vs Actuals Analysis")

        # Calculate budget metrics
        budget_data = filtered_workitems.copy()
        budget_data['board_name'] = budget_data['board_id'].map(board_names)
        budget_data['work_type_name'] = budget_data['work_type_id'].map(work_type_names)

        # Convert estimates from hours to seconds for comparison
        # Handle NULL values in likely_estimate
        budget_data['estimated_seconds'] = budget_data['likely_estimate'].fillna(0) * 3600
        budget_data['actual_seconds'] = budget_data['time_spent_seconds'].fillna(0)
        budget_data['variance_seconds'] = budget_data['actual_seconds'] - budget_data['estimated_seconds']
        budget_data['variance_pct'] = budget_data.apply(
            lambda row: calculate_variance(row['actual_seconds'], row['estimated_seconds']),
            axis=1
        )

        # Overall Budget Summary
        st.subheader("📊 Overall Budget Summary")
        col1, col2, col3, col4 = st.columns(4)

        total_estimated = budget_data['estimated_seconds'].sum()
        total_actual = budget_data['actual_seconds'].sum()
        total_variance = total_actual - total_estimated
        variance_pct = calculate_variance(total_actual, total_estimated)

        with col1:
            st.metric("Total Estimated", format_time_detailed(total_estimated))
        with col2:
            st.metric("Total Actual", format_time_detailed(total_actual))
        with col3:
            variance_color = "red" if total_variance > 0 else "green"
            st.metric("Variance", format_time_detailed(abs(total_variance)),
                     delta=format_variance(variance_pct),
                     delta_color="inverse")
        with col4:
            items_with_estimates = len(budget_data[budget_data['estimated_seconds'] > 0])
            st.metric("Items with Estimates", f"{items_with_estimates}/{len(budget_data)}")

        st.markdown("---")

        # Budget by Board - Interactive Table with Drill-Down
        st.subheader("📋 Budget Analysis by Board (Click to Drill Down)")

        board_budget = budget_data.groupby('board_name').agg({
            'id': 'count',
            'estimated_seconds': 'sum',
            'actual_seconds': 'sum',
            'variance_seconds': 'sum'
        }).reset_index()

        board_budget.columns = ['Board', 'Items', 'Estimated (sec)', 'Actual (sec)', 'Variance (sec)']
        board_budget['Estimated'] = board_budget['Estimated (sec)'].apply(format_time_detailed)
        board_budget['Actual'] = board_budget['Actual (sec)'].apply(format_time_detailed)
        board_budget['Variance'] = board_budget['Variance (sec)'].apply(format_time_detailed)
        board_budget['Variance %'] = board_budget.apply(
            lambda row: f"{calculate_variance(row['Actual (sec)'], row['Estimated (sec)']):.1f}%",
            axis=1
        )
        board_budget['Status'] = board_budget['Variance (sec)'].apply(
            lambda x: '🔴 Over Budget' if x > 0 else '🟢 Under Budget' if x < 0 else '⚪ On Target'
        )

        # Display interactive table
        display_board_budget = board_budget[['Board', 'Items', 'Estimated', 'Actual', 'Variance', 'Variance %', 'Status']]
        st.dataframe(
            display_board_budget,
            use_container_width=True,
            hide_index=True,
            height=400
        )

        # Visualization: Budget vs Actual by Board
        st.subheader("📊 Budget vs Actual Comparison by Board")
        if len(board_budget) > 0:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Estimated',
                x=board_budget['Board'],
                y=board_budget['Estimated (sec)'] / 3600,
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                name='Actual',
                x=board_budget['Board'],
                y=board_budget['Actual (sec)'] / 3600,
                marker_color='darkblue'
            ))
            fig.update_layout(
                barmode='group',
                xaxis_title='Board',
                yaxis_title='Hours',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # DRILL-DOWN SECTION
        st.subheader("🔍 Detailed Board Drill-Down")
        st.markdown("Select a board below to see all work items, organized by folders/workstreams")

        # Board selector for detailed view
        available_boards = sorted(budget_data['board_name'].dropna().unique())
        if len(available_boards) > 0:
            selected_board_detail = st.selectbox(
                "Select a board for detailed drill-down:",
                options=available_boards,
                key="board_drilldown_selector"
            )

            if selected_board_detail:
                board_detail_data = budget_data[budget_data['board_name'] == selected_board_detail].copy()

                # Add folder information
                board_detail_data['folder_number'] = board_detail_data['root_folder_number']

                # Get folder names
                folder_map = df_folders.set_index('number')['title'].to_dict()
                board_detail_data['folder_name'] = board_detail_data['folder_number'].map(folder_map)
                board_detail_data['folder_name'] = board_detail_data['folder_name'].fillna('No Folder')

                # Summary for selected board
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Items in Board", len(board_detail_data))
                with col2:
                    st.metric("Total Folders/Workstreams", board_detail_data['folder_name'].nunique())
                with col3:
                    completed_pct = (len(board_detail_data[board_detail_data['completed_at'].notna()]) / len(board_detail_data) * 100) if len(board_detail_data) > 0 else 0
                    st.metric("Completion Rate", f"{completed_pct:.1f}%")

                # Group by folder
                folders_in_board = board_detail_data['folder_name'].unique()

                st.markdown("### 📁 Work Items by Folder/Workstream")

                for folder in sorted(folders_in_board):
                    folder_items = board_detail_data[board_detail_data['folder_name'] == folder]

                    # Skip empty folders
                    if len(folder_items) == 0:
                        continue

                    # Calculate folder metrics
                    folder_est = folder_items['estimated_seconds'].sum()
                    folder_act = folder_items['actual_seconds'].sum()
                    folder_var = folder_act - folder_est
                    folder_completed = len(folder_items[folder_items['completed_at'].notna()])
                    folder_total = len(folder_items)

                    # Create expander for each folder
                    with st.expander(
                        f"📁 {folder} ({folder_total} items, {folder_completed} completed) - "
                        f"Est: {format_time_detailed(folder_est)}, Act: {format_time_detailed(folder_act)}, "
                        f"Var: {format_time_detailed(abs(folder_var))}"
                    ):
                        # Display all items in this folder
                        folder_display = folder_items[[
                            'number', 'title', 'work_type_name', 'assignee_username',
                            'estimated_seconds', 'actual_seconds', 'variance_seconds',
                            'completed_at', 'date_updated'
                        ]].copy()

                        folder_display['Estimated'] = folder_display['estimated_seconds'].apply(format_time_detailed)
                        folder_display['Actual'] = folder_display['actual_seconds'].apply(format_time_detailed)
                        folder_display['Variance'] = folder_display['variance_seconds'].apply(format_time_detailed)
                        folder_display['Status'] = folder_display['completed_at'].apply(
                            lambda x: '✅ Complete' if pd.notna(x) else '⏳ In Progress'
                        )
                        folder_display['Last Updated'] = folder_display['date_updated'].apply(format_datetime)

                        display_cols = folder_display[[
                            'number', 'title', 'work_type_name', 'assignee_username',
                            'Estimated', 'Actual', 'Variance', 'Status', 'Last Updated'
                        ]]
                        display_cols.columns = [
                            'Number', 'Title', 'Type', 'Assignee',
                            'Estimated', 'Actual', 'Variance', 'Status', 'Last Updated'
                        ]

                        st.dataframe(display_cols, use_container_width=True, hide_index=True, height=300)

                        # Folder-level summary stats
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Items", folder_total)
                        with col2:
                            st.metric("Estimated", format_time_detailed(folder_est))
                        with col3:
                            st.metric("Actual", format_time_detailed(folder_act))
                        with col4:
                            var_pct = calculate_variance(folder_act, folder_est)
                            st.metric("Variance", f"{var_pct:.1f}%")

                # Work type breakdown for this board
                st.markdown("---")
                st.subheader("📊 Work Type Breakdown for This Board")

                work_type_budget = board_detail_data.groupby('work_type_name').agg({
                    'id': 'count',
                    'estimated_seconds': 'sum',
                    'actual_seconds': 'sum',
                    'variance_seconds': 'sum'
                }).reset_index()

                work_type_budget.columns = ['Work Type', 'Items', 'Estimated (sec)', 'Actual (sec)', 'Variance (sec)']
                work_type_budget['Estimated'] = work_type_budget['Estimated (sec)'].apply(format_time_detailed)
                work_type_budget['Actual'] = work_type_budget['Actual (sec)'].apply(format_time_detailed)
                work_type_budget['Variance'] = work_type_budget['Variance (sec)'].apply(format_time_detailed)
                work_type_budget['Variance %'] = work_type_budget.apply(
                    lambda row: f"{calculate_variance(row['Actual (sec)'], row['Estimated (sec)']):.1f}%",
                    axis=1
                )

                display_work_type = work_type_budget[['Work Type', 'Items', 'Estimated', 'Actual', 'Variance', 'Variance %']]
                st.dataframe(display_work_type, use_container_width=True, hide_index=True)

                # Pie chart showing actual time distribution by work type
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Estimated Time Distribution")
                    if work_type_budget['Estimated (sec)'].sum() > 0:
                        fig = px.pie(
                            work_type_budget,
                            values='Estimated (sec)',
                            names='Work Type',
                            title=f'Estimated Hours by Work Type'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No estimated time data")

                with col2:
                    st.subheader("Actual Time Distribution")
                    if work_type_budget['Actual (sec)'].sum() > 0:
                        fig = px.pie(
                            work_type_budget,
                            values='Actual (sec)',
                            names='Work Type',
                            title=f'Actual Hours by Work Type'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No actual time data")

                # Individual items with biggest variance
                st.subheader("⚠️ Items with Largest Budget Variance in This Board")
                variance_items = board_detail_data[
                    (board_detail_data['estimated_seconds'] > 0) &
                    (board_detail_data['actual_seconds'] > 0)
                ].copy()

                if len(variance_items) > 0:
                    variance_items['variance_abs'] = variance_items['variance_seconds'].abs()
                    top_variance = variance_items.nlargest(10, 'variance_abs')[
                        ['number', 'title', 'work_type_name', 'assignee_username',
                         'estimated_seconds', 'actual_seconds', 'variance_seconds', 'variance_pct', 'date_updated']
                    ].copy()

                    top_variance['Estimated'] = top_variance['estimated_seconds'].apply(format_time_detailed)
                    top_variance['Actual'] = top_variance['actual_seconds'].apply(format_time_detailed)
                    top_variance['Variance'] = top_variance['variance_seconds'].apply(format_time_detailed)
                    top_variance['Variance %'] = top_variance['variance_pct'].apply(lambda x: f"{x:.1f}%")
                    top_variance['Last Updated'] = top_variance['date_updated'].apply(format_datetime)

                    display_variance = top_variance[[
                        'number', 'title', 'work_type_name', 'assignee_username',
                        'Estimated', 'Actual', 'Variance', 'Variance %', 'Last Updated'
                    ]]
                    display_variance.columns = [
                        'Number', 'Title', 'Type', 'Assignee',
                        'Estimated', 'Actual', 'Variance', 'Variance %', 'Last Updated'
                    ]

                    st.dataframe(display_variance, use_container_width=True, hide_index=True)
                else:
                    st.info("No items with both estimates and actuals")
        else:
            st.info("No board data available")

        st.markdown("---")

        # VALUE STREAM HIERARCHY SECTION
        st.subheader("🌳 Value Stream Hierarchy & Audit")
        st.markdown("Explore the complete folder/value stream hierarchy with all work items at every level")

        # Board selector for value stream view
        if len(available_boards) > 0:
            selected_board_vs = st.selectbox(
                "Select a board to view value stream hierarchy:",
                options=available_boards,
                key="board_valuestream_selector"
            )

            if selected_board_vs:
                board_vs_data = budget_data[budget_data['board_name'] == selected_board_vs].copy()

                # Build folder hierarchy
                board_folders = df_folders.copy()
                folder_hierarchy, root_folders = build_folder_hierarchy(board_folders)

                # Get all folders that have items in this board
                folders_with_items = board_vs_data['root_folder_number'].unique()

                st.info(f"💡 Click any value stream below to see all work items. Hierarchy shows parent → child relationships.")

                # Function to get all work items for a folder and its descendants
                def get_items_for_folder_tree(folder_number):
                    """Get all items that belong to this folder or any descendant folder"""
                    items_list = []

                    # Get items directly in this folder (where parent_number is this folder)
                    direct_items = board_vs_data[board_vs_data['parent_number'] == folder_number]
                    if len(direct_items) > 0:
                        items_list.append(direct_items)

                    # Also check root_folder_number for top-level folders
                    root_items = board_vs_data[
                        (board_vs_data['root_folder_number'] == folder_number) &
                        (board_vs_data['parent_number'].isna() | ~board_vs_data['parent_number'].str.startswith('F'))
                    ]
                    if len(root_items) > 0:
                        items_list.append(root_items)

                    # Recursively get items from child folders
                    if folder_number in folder_hierarchy:
                        for child in folder_hierarchy[folder_number]['children']:
                            child_items = get_items_for_folder_tree(child)
                            if len(child_items) > 0:
                                items_list.append(child_items)

                    if items_list:
                        return pd.concat(items_list).drop_duplicates(subset=['id'])
                    return pd.DataFrame()

                # Function to get items DIRECTLY in this folder (not descendants)
                def get_direct_items_for_folder(folder_number):
                    """Get only items directly in this folder, not in subfolders"""
                    # Items where parent_number is this folder
                    direct_items = board_vs_data[board_vs_data['parent_number'] == folder_number]

                    # For root folders, also get items where this is the root and no folder parent
                    if folder_number in folder_hierarchy and folder_hierarchy[folder_number]['level'] == 0:
                        root_items = board_vs_data[
                            (board_vs_data['root_folder_number'] == folder_number) &
                            (board_vs_data['parent_number'].isna() | ~board_vs_data['parent_number'].str.startswith('F'))
                        ]
                        if len(direct_items) > 0 and len(root_items) > 0:
                            return pd.concat([direct_items, root_items]).drop_duplicates(subset=['id'])
                        elif len(root_items) > 0:
                            return root_items

                    return direct_items

                # Function to display folder and its children recursively
                def display_folder_tree(folder_number, level=0):
                    if folder_number not in folder_hierarchy:
                        return

                    folder_info = folder_hierarchy[folder_number]
                    folder_title = folder_info['title']

                    # Get items for this folder and all descendants
                    folder_items = get_items_for_folder_tree(folder_number)

                    # Get items DIRECTLY in this folder (not in subfolders)
                    direct_items = get_direct_items_for_folder(folder_number)

                    if len(folder_items) == 0 and len(folder_info['children']) == 0:
                        return  # Skip folders with no items and no children

                    # Calculate metrics for ALL items (including descendants)
                    if len(folder_items) > 0:
                        folder_est = folder_items['estimated_seconds'].sum()
                        folder_act = folder_items['actual_seconds'].sum()
                        folder_var = folder_act - folder_est
                        folder_completed = len(folder_items[folder_items['completed_at'].notna()])
                        folder_total = len(folder_items)
                    else:
                        folder_est = 0
                        folder_act = 0
                        folder_var = 0
                        folder_completed = 0
                        folder_total = 0

                    # Create indentation based on level
                    indent = "　" * level  # Using full-width space for indentation

                    # Determine icon based on level
                    if level == 0:
                        icon = "📊"
                    elif level == 1:
                        icon = "📁"
                    else:
                        icon = "📂"

                    # Create expander title with metrics
                    expander_title = f"{indent}{icon} {folder_title}"
                    if folder_total > 0:
                        expander_title += f" ({folder_total} items, {folder_completed} completed) - Est: {format_time_detailed(folder_est)}, Act: {format_time_detailed(folder_act)}"

                    with st.expander(expander_title, expanded=False):
                        # Show folder path
                        folder_path = get_folder_path(folder_number, folder_hierarchy)
                        st.caption(f"📍 Path: {folder_path}")

                        # Show summary of total items (including descendants) vs direct items
                        direct_count = len(direct_items)
                        total_count = len(folder_items)
                        if total_count > direct_count:
                            st.info(f"📊 This folder contains {direct_count} direct items and {total_count - direct_count} items in subfolders (Total: {total_count})")
                        elif direct_count > 0:
                            st.info(f"📊 This folder contains {direct_count} direct items")

                        # Display DIRECT items if any
                        if len(direct_items) > 0:
                            st.markdown(f"**Work Items Directly in {folder_title}:**")
                            display_items = direct_items[[
                                'number', 'title', 'work_type_name', 'assignee_username',
                                'estimated_seconds', 'actual_seconds', 'variance_seconds',
                                'completed_at', 'date_updated', 'parent_number'
                            ]].copy()

                            display_items['Estimated'] = display_items['estimated_seconds'].apply(format_time_detailed)
                            display_items['Actual'] = display_items['actual_seconds'].apply(format_time_detailed)
                            display_items['Variance'] = display_items['variance_seconds'].apply(format_time_detailed)
                            display_items['Status'] = display_items['completed_at'].apply(
                                lambda x: '✅ Complete' if pd.notna(x) else '⏳ In Progress'
                            )
                            display_items['Last Updated'] = display_items['date_updated'].apply(format_datetime)
                            display_items['Parent Item'] = display_items['parent_number'].fillna('—')

                            cols_to_show = display_items[[
                                'number', 'title', 'work_type_name', 'assignee_username',
                                'Estimated', 'Actual', 'Variance', 'Status', 'Last Updated', 'Parent Item'
                            ]]
                            cols_to_show.columns = [
                                'Number', 'Title', 'Type', 'Assignee',
                                'Estimated', 'Actual', 'Variance', 'Status', 'Last Updated', 'Parent Item'
                            ]

                            st.dataframe(cols_to_show, use_container_width=True, hide_index=True, height=min(400, len(cols_to_show) * 35 + 38))

                            # Calculate direct item metrics
                            direct_est = direct_items['estimated_seconds'].sum()
                            direct_act = direct_items['actual_seconds'].sum()
                            direct_completed = len(direct_items[direct_items['completed_at'].notna()])

                            # Show summary metrics - Direct items
                            st.markdown("**Direct Items Metrics:**")
                            col1, col2, col3, col4, col5 = st.columns(5)
                            with col1:
                                st.metric("Direct Items", len(direct_items))
                            with col2:
                                st.metric("Completed", direct_completed)
                            with col3:
                                st.metric("Estimated", format_time_detailed(direct_est))
                            with col4:
                                st.metric("Actual", format_time_detailed(direct_act))
                            with col5:
                                var_pct = calculate_variance(direct_act, direct_est)
                                st.metric("Variance", f"{var_pct:.1f}%")

                            # Show total metrics including descendants if different
                            if folder_total > len(direct_items):
                                st.markdown("**Total (Including Subfolders):**")
                                col1, col2, col3, col4, col5 = st.columns(5)
                                with col1:
                                    st.metric("Total Items", folder_total)
                                with col2:
                                    st.metric("Completed", folder_completed)
                                with col3:
                                    st.metric("Estimated", format_time_detailed(folder_est))
                                with col4:
                                    st.metric("Actual", format_time_detailed(folder_act))
                                with col5:
                                    var_pct = calculate_variance(folder_act, folder_est)
                                    st.metric("Variance", f"{var_pct:.1f}%")
                        else:
                            st.info("No direct work items in this folder (items may exist in subfolders)")

                        # Show child folders info if any
                        if len(folder_info['children']) > 0:
                            st.markdown(f"**Sub-folders in {folder_title}:**")
                            child_names = [folder_hierarchy[child]['title'] for child in folder_info['children'] if child in folder_hierarchy]
                            st.write(", ".join(child_names))

                    # Recursively display children
                    for child_number in folder_info['children']:
                        display_folder_tree(child_number, level + 1)

                # Display the hierarchy starting from root folders
                st.markdown("### 🌳 Complete Hierarchy")

                # Get root folders that have items in this board
                relevant_roots = []
                for root in root_folders:
                    # Check if this root or any of its descendants have items
                    def has_items_in_tree(folder_num):
                        # Check direct items
                        direct = get_direct_items_for_folder(folder_num)
                        if len(direct) > 0:
                            return True
                        # Check descendants
                        if folder_num in folder_hierarchy:
                            for child in folder_hierarchy[folder_num]['children']:
                                if has_items_in_tree(child):
                                    return True
                        return False

                    if has_items_in_tree(root):
                        relevant_roots.append(root)

                if len(relevant_roots) > 0:
                    for root in relevant_roots:
                        display_folder_tree(root, level=0)
                else:
                    st.info("No items found in folder hierarchy for this board")

                # Quick search for specific value stream
                st.markdown("---")
                st.subheader("🔎 Search for Specific Value Stream")
                search_vs = st.text_input(
                    "Enter value stream name (e.g., 'Open Order Management'):",
                    key="valuestream_search"
                )

                if search_vs:
                    # Search for matching folders
                    matching_folders = []
                    for folder_num, folder_info in folder_hierarchy.items():
                        if search_vs.lower() in folder_info['title'].lower():
                            # Get all items for this folder and descendants
                            all_items = get_items_for_folder_tree(folder_num)
                            direct_items = get_direct_items_for_folder(folder_num)

                            if len(all_items) > 0:
                                matching_folders.append({
                                    'number': folder_num,
                                    'title': folder_info['title'],
                                    'path': get_folder_path(folder_num, folder_hierarchy),
                                    'items': all_items,
                                    'direct_items': direct_items,
                                    'level': folder_info['level']
                                })

                    if len(matching_folders) > 0:
                        st.success(f"Found {len(matching_folders)} matching value stream(s):")

                        for match in matching_folders:
                            # Determine icon based on level
                            if match['level'] == 0:
                                icon = "📊"
                            elif match['level'] == 1:
                                icon = "📁"
                            else:
                                icon = "📂"

                            st.markdown(f"#### {icon} {match['title']}")
                            st.caption(f"📍 Full path: {match['path']} | Level: {match['level']}")

                            items_df = match['items']
                            direct_df = match['direct_items']

                            # Calculate metrics for all items
                            if len(items_df) > 0:
                                folder_est = items_df['estimated_seconds'].sum()
                                folder_act = items_df['actual_seconds'].sum()
                                folder_completed = len(items_df[items_df['completed_at'].notna()])
                                folder_total = len(items_df)
                            else:
                                folder_est = 0
                                folder_act = 0
                                folder_completed = 0
                                folder_total = 0

                            # Calculate metrics for direct items
                            direct_est = direct_df['estimated_seconds'].sum() if len(direct_df) > 0 else 0
                            direct_act = direct_df['actual_seconds'].sum() if len(direct_df) > 0 else 0
                            direct_completed = len(direct_df[direct_df['completed_at'].notna()]) if len(direct_df) > 0 else 0
                            direct_total = len(direct_df)

                            # Show info about direct vs total
                            if folder_total > direct_total:
                                st.info(f"📊 Contains {direct_total} direct items and {folder_total - direct_total} items in subfolders (Total: {folder_total})")
                            else:
                                st.info(f"📊 Contains {direct_total} direct items")

                            # Show direct items metrics
                            st.markdown("**Direct Items Metrics:**")
                            col1, col2, col3, col4, col5 = st.columns(5)
                            with col1:
                                st.metric("Direct Items", direct_total)
                            with col2:
                                st.metric("Completed", f"{direct_completed}/{direct_total}")
                            with col3:
                                st.metric("Estimated", format_time_detailed(direct_est))
                            with col4:
                                st.metric("Actual", format_time_detailed(direct_act))
                            with col5:
                                var_pct = calculate_variance(direct_act, direct_est)
                                st.metric("Variance", f"{var_pct:.1f}%")

                            # Show total metrics if different
                            if folder_total > direct_total:
                                st.markdown("**Total (Including Subfolders):**")
                                col1, col2, col3, col4, col5 = st.columns(5)
                                with col1:
                                    st.metric("Total Items", folder_total)
                                with col2:
                                    st.metric("Completed", f"{folder_completed}/{folder_total}")
                                with col3:
                                    st.metric("Estimated", format_time_detailed(folder_est))
                                with col4:
                                    st.metric("Actual", format_time_detailed(folder_act))
                                with col5:
                                    var_pct = calculate_variance(folder_act, folder_est)
                                    st.metric("Variance", f"{var_pct:.1f}%")

                            # Show DIRECT items in table
                            if len(direct_df) > 0:
                                st.markdown("**Direct Work Items:**")
                                display_items = direct_df[[
                                'number', 'title', 'work_type_name', 'assignee_username',
                                'estimated_seconds', 'actual_seconds', 'variance_seconds',
                                'completed_at', 'date_updated', 'parent_number'
                            ]].copy()

                            display_items['Estimated'] = display_items['estimated_seconds'].apply(format_time_detailed)
                            display_items['Actual'] = display_items['actual_seconds'].apply(format_time_detailed)
                            display_items['Variance'] = display_items['variance_seconds'].apply(format_time_detailed)
                            display_items['Status'] = display_items['completed_at'].apply(
                                lambda x: '✅ Complete' if pd.notna(x) else '⏳ In Progress'
                            )
                            display_items['Last Updated'] = display_items['date_updated'].apply(format_datetime)
                            display_items['Parent Item'] = display_items['parent_number'].fillna('—')

                            cols_to_show = display_items[[
                                'number', 'title', 'work_type_name', 'assignee_username',
                                'Estimated', 'Actual', 'Variance', 'Status', 'Last Updated', 'Parent Item'
                            ]]
                            cols_to_show.columns = [
                                'Number', 'Title', 'Type', 'Assignee',
                                'Estimated', 'Actual', 'Variance', 'Status', 'Last Updated', 'Parent Item'
                            ]

                            st.dataframe(cols_to_show, use_container_width=True, hide_index=True)
                        else:
                            st.info("No direct items in this folder (all items are in subfolders)")

                        st.markdown("---")
                    else:
                        st.warning(f"No value streams found matching '{search_vs}' with items in board '{selected_board_vs}'")
        else:
            st.info("No boards available")

        # Download budget analysis
        st.markdown("---")
        st.subheader("📥 Export Budget Analysis")

        export_data = budget_data[[
            'number', 'title', 'board_name', 'work_type_name', 'assignee_username',
            'estimated_seconds', 'actual_seconds', 'variance_seconds', 'variance_pct', 'date_updated'
        ]].copy()

        export_data['Estimated'] = export_data['estimated_seconds'].apply(format_time_detailed)
        export_data['Actual'] = export_data['actual_seconds'].apply(format_time_detailed)
        export_data['Variance'] = export_data['variance_seconds'].apply(format_time_detailed)
        export_data['Variance %'] = export_data['variance_pct'].apply(lambda x: f"{x:.1f}%")
        export_data['Last Updated'] = export_data['date_updated'].apply(format_datetime)

        export_display = export_data[[
            'number', 'title', 'board_name', 'work_type_name', 'assignee_username',
            'Estimated', 'Actual', 'Variance', 'Variance %', 'Last Updated'
        ]]
        export_display.columns = [
            'Number', 'Title', 'Board', 'Type', 'Assignee',
            'Estimated', 'Actual', 'Variance', 'Variance %', 'Last Updated'
        ]

        csv = export_display.to_csv(index=False)
        st.download_button(
            label="📥 Download Budget Analysis as CSV",
            data=csv,
            file_name=f"budget_analysis_{start_date}_to_{end_date}.csv",
            mime="text/csv"
        )

    with tab5:
        st.header("⚠️ Stale Work Items")
        st.markdown("Work items with no activity (time logged or updates) in the last 3 days, excluding Done and Icebox items")

        # Calculate 3 days ago (timezone-aware to match pandas datetime columns)
        three_days_ago = pd.Timestamp.now(tz='UTC') - timedelta(days=3)

        # Get lane names for Done and Icebox
        done_icebox_lanes = []
        for lane_id, lane_name in lane_names.items():
            if 'done' in lane_name.lower() or 'icebox' in lane_name.lower():
                done_icebox_lanes.append(lane_id)

        # Filter out Done and Icebox items
        active_items = filtered_workitems[~filtered_workitems['lane_id'].isin(done_icebox_lanes)].copy()

        # Get recent time entries (last 3 days)
        recent_time_entries = df_time_entries[
            pd.to_datetime(df_time_entries['date_added']) >= three_days_ago
        ]['item_number'].unique()

        # Find stale items: no update in last 3 days AND no time logged in last 3 days
        stale_items = active_items[
            (active_items['date_updated'] < three_days_ago) &
            (~active_items['number'].isin(recent_time_entries))
        ].copy()

        # Add lane and type names
        stale_items['lane_name'] = stale_items['lane_id'].map(lane_names)
        stale_items['work_type_name'] = stale_items['work_type_id'].map(work_type_names)
        stale_items['board_name'] = stale_items['board_id'].map(board_names)

        # Display summary metrics
        st.subheader("📊 Stale Items Summary")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Stale Items", len(stale_items))

        with col2:
            if len(stale_items) > 0:
                avg_days_stale = (pd.Timestamp.now(tz='UTC') - stale_items['date_updated'].max()).days
                st.metric("Oldest Item (days)", avg_days_stale)
            else:
                st.metric("Oldest Item (days)", 0)

        with col3:
            unique_assignees = stale_items['assignee_username'].nunique()
            st.metric("Affected Assignees", unique_assignees)

        with col4:
            unique_boards = stale_items['board_name'].nunique()
            st.metric("Affected Boards", unique_boards)

        st.markdown("---")

        if len(stale_items) > 0:
            # Breakdown by board
            st.subheader("🗂️ Stale Items by Board")
            board_counts = stale_items['board_name'].value_counts()

            if len(board_counts) > 0:
                colors = get_chart_theme()
                fig = px.bar(
                    x=board_counts.values,
                    y=board_counts.index,
                    orientation='h',
                    labels={'x': 'Number of Stale Items', 'y': 'Board'}
                )
                fig.update_traces(
                    marker_color=colors['warning'][0],
                    marker_line_color='white',
                    marker_line_width=1.5
                )
                fig = apply_chart_template(fig, "")
                st.plotly_chart(fig, use_container_width=True)

            # Detailed table
            st.subheader("📋 Stale Items Details")

            # Calculate days since last update
            stale_items['days_since_update'] = (pd.Timestamp.now(tz='UTC') - stale_items['date_updated']).dt.days

            display_stale = stale_items[[
                'number', 'title', 'assignee_username', 'board_name',
                'lane_name', 'work_type_name', 'date_updated', 'days_since_update'
            ]].copy()

            display_stale['Last Updated'] = display_stale['date_updated'].apply(format_datetime)

            final_display = display_stale[[
                'number', 'title', 'assignee_username', 'board_name',
                'lane_name', 'work_type_name', 'Last Updated', 'days_since_update'
            ]]

            final_display.columns = [
                'Number', 'Title', 'Assignee', 'Board',
                'Lane', 'Type', 'Last Updated', 'Days Stale'
            ]

            # Sort by days stale (descending)
            final_display = final_display.sort_values('Days Stale', ascending=False)

            st.dataframe(final_display, use_container_width=True, hide_index=True, height=600)

            # Download option
            csv = final_display.to_csv(index=False)
            st.download_button(
                label="📥 Download stale items as CSV",
                data=csv,
                file_name=f"stale_items_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

        else:
            st.success("✅ No stale items found! All active work items have been updated in the last 3 days.")

    with tab6:
        st.header("📋 Data Table")
        st.markdown("Browse all filtered work items in a table format")

        if len(filtered_workitems) > 0:
            # Create display dataframe
            display_df = filtered_workitems.copy()
            display_df['board_name'] = display_df['board_id'].map(board_names)
            display_df['work_type_name'] = display_df['work_type_id'].map(work_type_names)
            display_df['lane_name'] = display_df['lane_id'].map(lane_names)
            display_df['priority_name'] = display_df['priority_id'].map(priority_names)

            # Format time
            display_df['time_spent_formatted'] = display_df['time_spent_seconds'].apply(format_time_detailed)

            # Select and rename columns
            table_df = display_df[[
                'number', 'title', 'assignee_username', 'board_name',
                'lane_name', 'work_type_name', 'priority_name',
                'time_spent_formatted', 'completed_at', 'date_added', 'date_updated'
            ]]

            table_df.columns = [
                'Number', 'Title', 'Assignee', 'Board',
                'Lane', 'Type', 'Priority',
                'Time Spent', 'Completed At', 'Date Added', 'Last Updated'
            ]

            st.dataframe(table_df, use_container_width=True, hide_index=True, height=600)

            # Download data
            csv = table_df.to_csv(index=False)
            st.download_button(
                label="📥 Download filtered data as CSV",
                data=csv,
                file_name=f"workitems_{start_date}_to_{end_date}.csv",
                mime="text/csv"
            )
        else:
            st.info("No work items match the current filters")

    with tab7:
        st.header("🔧 Debug & Schema Information")
        st.markdown("View database schemas and structure for debugging purposes")

        # Get schema information
        with st.spinner("Loading schema information..."):
            schema_info = get_database_schema()

        # Display schema for each table
        for table_name, table_info in schema_info.items():
            with st.expander(f"📊 {table_name.upper()} (Click to expand schema)"):
                if 'error' in table_info:
                    st.error(f"Error loading schema: {table_info['error']}")
                else:
                    # Show row count
                    st.metric("Row Count", f"{table_info.get('row_count', 'N/A'):,}")

                    # Show columns
                    st.subheader("Columns")
                    columns_df = pd.DataFrame(table_info['columns'])
                    st.dataframe(columns_df, use_container_width=True, hide_index=True)

                    # Show sample data
                    st.subheader("Sample Data (First 3 rows)")
                    try:
                        sample_query = f"SELECT * FROM {table_name}"
                        if table_name not in ['users', 'teams']:
                            sample_query += " WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
                        sample_query += " LIMIT 3"

                        sample_df = pd.read_sql(sample_query, engine)
                        st.dataframe(sample_df, use_container_width=True)
                    except Exception as e:
                        st.error(f"Could not load sample data: {str(e)}")

        # Export all schemas
        st.markdown("---")
        st.subheader("📥 Export Schema Information")

        # Convert schema info to readable format
        schema_text = json.dumps(schema_info, indent=2, default=str)
        st.download_button(
            label="📥 Download All Schemas as JSON",
            data=schema_text,
            file_name="database_schemas.json",
            mime="application/json"
        )

        # Connection info
        st.markdown("---")
        st.subheader("🔗 Database Connection Info")
        st.code("""
Database: neondb
Host: ep-mute-firefly-74914637-pooler.us-east-2.aws.neon.tech
Organization ID: 33b4e799-b8aa-46cc-9d4d-73c915601515
Connection: Read-only
SSL: Required
        """)

if __name__ == "__main__":
    main()
