import dash
from dash import dcc, html, Input, Output, State, callback, no_update
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import hashlib
import random
import re

print("=" * 70)
print("AI-SOLUTIONS ANALYTICS DASHBOARD")
print("Metrics: Jobs | Demos/Events | AI Assistant | Country Analysis")
print("=" * 70)

# ============================================
# GENERATE COMPREHENSIVE WEB SERVER LOG DATA
# ============================================
print("Generating web server log data...")

np.random.seed(42)
n = 20000

# Countries data with coordinates for globe
countries_data = {
    'South Africa': {'lat': -30.5595, 'lon': 22.9375, 'region': 'Southern Africa'},
    'Botswana': {'lat': -22.3285, 'lon': 24.6849, 'region': 'Southern Africa'},
    'Namibia': {'lat': -22.9576, 'lon': 18.4904, 'region': 'Southern Africa'},
    'Zimbabwe': {'lat': -19.0154, 'lon': 29.1549, 'region': 'Southern Africa'},
    'Zambia': {'lat': -13.1339, 'lon': 27.8493, 'region': 'Southern Africa'},
    'Mozambique': {'lat': -18.6657, 'lon': 35.5296, 'region': 'Southern Africa'},
    'Kenya': {'lat': -1.2864, 'lon': 36.8172, 'region': 'East Africa'},
    'Nigeria': {'lat': 9.0820, 'lon': 8.6753, 'region': 'West Africa'},
    'Egypt': {'lat': 26.8206, 'lon': 30.8025, 'region': 'North Africa'},
    'Ghana': {'lat': 7.9465, 'lon': -1.0232, 'region': 'West Africa'},
    'Morocco': {'lat': 31.7917, 'lon': -7.0926, 'region': 'North Africa'},
    'Tanzania': {'lat': -6.3690, 'lon': 34.8888, 'region': 'East Africa'},
}

countries_list = list(countries_data.keys())

# Job types (for types of jobs requested)
job_types_list = [
    'Software Developer', 'Data Analyst', 'AI Engineer', 'Cloud Architect',
    'DevOps Engineer', 'Project Manager', 'Sales Representative', 'IT Support',
    'Cybersecurity Analyst', 'Business Intelligence Analyst', 'Data Scientist',
    'UX Designer', 'Product Manager', 'Network Engineer', 'Database Administrator',
    'Frontend Developer', 'Backend Developer', 'Full Stack Developer', 'QA Engineer'
]

# Departments
departments = ['HR', 'IT', 'Sales', 'Operations', 'Marketing', 'Finance', 'Executive']

# Event types (schedule demos or promotional events)
event_types = ['Schedule Demo', 'Promotional Event', 'Webinar', 'Conference', 'Workshop', 'Product Launch']

# AI query types (for AI-powered virtual assistant)
ai_query_types = ['Job Search', 'Company Info', 'Tech Support', 'Demo Booking', 'Pricing', 'Product Features', 
                  'Salary Inquiry', 'Career Advice', 'Training Request', 'Documentation']

# Generate dates (2025-2026)
start_date = datetime(2025, 1, 1)
dates = [start_date + timedelta(days=random.randint(0, 500)) for _ in range(n)]

# Create comprehensive dataframe with ALL required metrics
df = pd.DataFrame({
    'log_id': range(1, n + 1),
    'timestamp': dates,
    'date': [d.strftime('%Y-%m-%d') for d in dates],
    'year': [d.year for d in dates],
    'month': [d.strftime('%Y-%m') for d in dates],
    'month_num': [d.month for d in dates],
    'week': [d.isocalendar()[1] for d in dates],
    'week_start': [(d - timedelta(days=d.weekday())).strftime('%Y-%m-%d') for d in dates],
    'quarter': [f'Q{(d.month-1)//3+1} {d.year}' for d in dates],
    'day_name': [d.strftime('%A') for d in dates],
    
    # ========== LOCATION METRICS ==========
    'country': np.random.choice(countries_list, n),
    'city': np.random.choice(['Gaborone', 'Johannesburg', 'Cape Town', 'Nairobi', 'Lagos', 'Cairo', 'Accra', 'Dar es Salaam', 'Lusaka', 'Harare'], n),
    'office_location': np.random.choice(['Head Office', 'Regional Hub', 'Satellite Office', 'Remote Office'], n),
    'region': [countries_data[c]['region'] for c in np.random.choice(countries_list, n)],
    
    # ========== METRIC 1: NUMBER OF JOBS PLACED ==========
    'jobs_placed': np.random.poisson(lam=12, size=n),
    
    # ========== METRIC 2: TYPES OF JOBS REQUESTED ==========
    'job_title': np.random.choice(job_types_list, n),
    'job_department': np.random.choice(departments, n),
    'job_salary_band': np.random.choice(['Entry (<$50k)', 'Mid ($50-80k)', 'Senior ($80-120k)', 'Lead ($120k+)'], n, p=[0.2, 0.35, 0.3, 0.15]),
    'job_experience_level': np.random.choice(['Entry', 'Junior', 'Mid', 'Senior', 'Lead'], n, p=[0.1, 0.2, 0.35, 0.25, 0.1]),
    'job_remote_allowed': np.random.choice([True, False], n, p=[0.6, 0.4]),
    
    # ========== METRIC 3: REQUESTS FOR SCHEDULE DEMOS OR PROMOTIONAL EVENTS ==========
    'event_type': np.random.choice(event_types, n, p=[0.35, 0.25, 0.15, 0.1, 0.1, 0.05]),
    'event_requested': np.random.choice([True, False], n, p=[0.4, 0.6]),
    'event_attended': np.random.choice([True, False], n, p=[0.25, 0.75]),
    'event_follow_up': np.random.choice([True, False], n, p=[0.5, 0.5]),
    
    # ========== METRIC 4: REQUESTS FOR AI-POWERED VIRTUAL ASSISTANT ==========
    'ai_assistant_requested': np.random.choice([True, False], n, p=[0.5, 0.5]),
    'ai_query_type': np.random.choice(ai_query_types, n),
    'ai_response_time_sec': np.random.exponential(scale=1.5, size=n),
    'ai_helpful': np.random.choice([True, False], n, p=[0.88, 0.12]),
    'ai_satisfaction': np.random.choice([1, 2, 3, 4, 5], n, p=[0.03, 0.05, 0.12, 0.35, 0.45]),
    
    # ========== ADDITIONAL METRICS ==========
    'ai_assist_requests': np.random.poisson(lam=10, size=n),
    'rescheduled_meetings': np.random.poisson(lam=4, size=n),
    'total_meetings': np.random.poisson(lam=25, size=n),
    'resolution_time_minutes': np.random.exponential(scale=40, size=n),
    'satisfaction_score': np.random.choice([1, 2, 3, 4, 5], n, p=[0.03, 0.07, 0.2, 0.35, 0.35]),
    'ai_usage_rate': np.random.uniform(25, 98, n),
    'escalation_rate': np.random.uniform(5, 45, n),
    'user_id': np.random.randint(1000, 9999, n),
    'session_duration_min': np.random.exponential(scale=10, size=n),
    'pages_visited': np.random.poisson(lam=12, size=n),
    'returning_user': np.random.choice([True, False], n, p=[0.45, 0.55]),
})

# Add coordinates for each country
df['lat'] = df['country'].map(lambda c: countries_data.get(c, {}).get('lat', 0))
df['lon'] = df['country'].map(lambda c: countries_data.get(c, {}).get('lon', 0))

print(f"Generated {len(df):,} web server log records")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Countries: {df['country'].nunique()}")
print(f"Job Types: {df['job_title'].nunique()}")

# ============================================
# GRAPH LIBRARY FOR SEARCH (with tab and section info)
# ============================================
GRAPH_LIBRARY = {
    "overview-kpis": {"name": "Overview KPIs", "tab": "tab-overview", "keywords": ["kpi", "overview", "summary", "dashboard", "total", "metrics"]},
    "jobs-by-country": {"name": "Jobs Placed by Country", "tab": "tab-overview", "keywords": ["job", "jobs", "country", "placed", "employment"]},
    "events-by-country": {"name": "Event Requests by Country", "tab": "tab-overview", "keywords": ["event", "demo", "promotional", "country", "request"]},
    "ai-by-country": {"name": "AI Requests by Country", "tab": "tab-overview", "keywords": ["ai", "assistant", "virtual", "country", "request"]},
    "satisfaction-score": {"name": "Satisfaction Score by Region", "tab": "tab-overview", "keywords": ["satisfaction", "happy", "score", "rating"]},
    "ai-usage-rate": {"name": "AI Usage Rate by Region", "tab": "tab-overview", "keywords": ["usage", "adoption", "ai rate", "utilization"]},
    "escalation-rate": {"name": "Escalation Rate by Region", "tab": "tab-overview", "keywords": ["escalation", "human", "transfer", "handoff"]},
    "resolution-time": {"name": "Resolution Time by Office", "tab": "tab-overview", "keywords": ["resolution", "time", "speed", "response"]},
    "world-map-globe": {"name": "3D Rotating Globe Map", "tab": "tab-country", "keywords": ["map", "world", "globe", "rotate", "3d", "geographic", "country", "atlas", "earth"]},
    "country-comparison": {"name": "Country Comparison Chart", "tab": "tab-country", "keywords": ["compare", "comparison", "country", "bar"]},
    "jobs-country": {"name": "Jobs Placed by Country (Jobs Tab)", "tab": "tab-jobs", "keywords": ["job", "jobs", "country", "placed"]},
    "jobs-department": {"name": "Jobs by Department", "tab": "tab-jobs", "keywords": ["department", "jobs", "dept", "team"]},
    "jobs-salary": {"name": "Jobs by Salary Band", "tab": "tab-jobs", "keywords": ["salary", "pay", "income", "band", "jobs"]},
    "jobs-trend": {"name": "Jobs Trend Over Time", "tab": "tab-jobs", "keywords": ["trend", "time", "monthly", "timeline", "history"]},
    "top-job-titles": {"name": "Top Job Titles Requested", "tab": "tab-job-types", "keywords": ["title", "position", "role", "top", "job"]},
    "job-department-treemap": {"name": "Job Types by Department", "tab": "tab-job-types", "keywords": ["treemap", "department", "distribution", "job type"]},
    "experience-level": {"name": "Job Demand by Experience", "tab": "tab-job-types", "keywords": ["experience", "level", "senior", "junior", "entry"]},
    "remote-jobs": {"name": "Remote vs On-Site Jobs", "tab": "tab-job-types", "keywords": ["remote", "work from home", "onsite", "hybrid"]},
    "event-types": {"name": "Event Types Distribution", "tab": "tab-events", "keywords": ["event type", "demo", "webinar", "conference"]},
    "event-attendance": {"name": "Event Attendance Rate", "tab": "tab-events", "keywords": ["attendance", "attend", "event", "showed up"]},
    "event-trend": {"name": "Event Requests Trend", "tab": "tab-events", "keywords": ["event trend", "event history", "monthly events"]},
    "ai-query-types": {"name": "AI Query Types", "tab": "tab-ai", "keywords": ["ai query", "question", "assistant query", "chat"]},
    "ai-helpfulness": {"name": "AI Helpfulness Rating", "tab": "tab-ai", "keywords": ["helpful", "ai rating", "assistant rating"]},
    "ai-satisfaction": {"name": "AI Satisfaction Score", "tab": "tab-ai", "keywords": ["satisfaction", "ai score", "rating"]},
    "all-metrics-table": {"name": "All Metrics by Country Table", "tab": "tab-all-metrics", "keywords": ["table", "all metrics", "comprehensive", "data"]},
}

# ============================================
# AUTHENTICATION (Single Login)
# ============================================
USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "user": hashlib.sha256("user123".encode()).hexdigest(),
}

# ============================================
# INITIALIZE DASH APP
# ============================================
app = dash.Dash(__name__, title="AI-Solutions | Analytics Dashboard",
                external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'],
                suppress_callback_exceptions=True)
server = app.server

# Add custom CSS for highlighting and background image
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .highlight-graph {
                animation: highlight-pulse 2s ease-in-out;
                background-color: #fff3cd !important;
                border: 3px solid #ffc107 !important;
                border-radius: 10px !important;
                padding: 10px !important;
                transition: all 0.3s ease;
            }
            @keyframes highlight-pulse {
                0% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.7); }
                70% { box-shadow: 0 0 0 20px rgba(255, 193, 7, 0); }
                100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0); }
            }
            .graph-section {
                transition: all 0.3s ease;
                scroll-margin-top: 100px;
            }
            /* Globe container styling */
            .globe-container {
                background: linear-gradient(135deg, #0a0a2a, #1a1a3a);
                border-radius: 20px;
                padding: 10px;
            }
            /* Globe title styling */
            .globe-title {
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                margin-bottom: 20px;
                color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            .globe-title h2 {
                margin: 0;
                font-size: 28px;
                font-weight: bold;
            }
            .globe-title p {
                margin: 10px 0 0 0;
                opacity: 0.9;
                font-size: 14px;
            }
            /* Login page with background image */
            .login-background {
                background-image: url('https://images.unsplash.com/photo-1531297484001-80022131f5a1?q=80&w=2020&auto=format&fit=crop');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                position: relative;
                min-height: 100vh;
            }
            .login-background::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.65);
                z-index: 1;
            }
            .login-background > div {
                position: relative;
                z-index: 2;
            }
            /* Time granularity selector styling */
            .time-granularity-group {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 5px;
                margin-left: 15px;
            }
            .granularity-btn {
                margin: 0 2px;
                transition: all 0.2s;
            }
            .granularity-btn-active {
                background-color: #007bff !important;
                color: white !important;
                border-color: #007bff !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script>
            // Function to scroll to element and highlight
            window.scrollToGraph = function(elementId) {
                const element = document.getElementById(elementId);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    element.classList.add('highlight-graph');
                    setTimeout(() => {
                        element.classList.remove('highlight-graph');
                    }, 2000);
                }
            }
        </script>
    </body>
</html>
'''

# ============================================
# FUNCTION TO CREATE ROTATING GLOBE MAP WITH ENHANCED TITLE
# ============================================
def create_rotating_globe(data_df, title="🌍 Global Activity Map - Rotating Globe"):
    """Create an interactive 3D globe that users can rotate and drag"""
    
    # Aggregate data by country
    map_data = data_df.groupby('country').agg({
        'jobs_placed': 'sum',
        'event_requested': 'sum',
        'ai_assistant_requested': 'sum',
        'satisfaction_score': 'mean',
        'lat': 'first',
        'lon': 'first'
    }).reset_index()
    
    map_data['total_activity'] = map_data['jobs_placed'] + map_data['event_requested'] + map_data['ai_assistant_requested']
    
    # Create scattergeo map on a rotating globe (orthographic projection)
    fig = go.Figure()
    
    # Add scatter traces for each country (bubble size = total activity)
    fig.add_trace(go.Scattergeo(
        lon=map_data['lon'],
        lat=map_data['lat'],
        text=map_data['country'],
        mode='markers+text',
        textposition="top center",
        textfont=dict(size=10, color='white'),
        marker=dict(
            size=map_data['total_activity'] / map_data['total_activity'].max() * 40 + 10,
            color=map_data['total_activity'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Total Activity", x=0, y=0.5),
            line=dict(width=1, color='white'),
            sizemode='area',
            sizeref=2.*max(map_data['total_activity'])/(40**2),
            sizemin=4
        ),
        hoverinfo='text',
        hovertext=map_data.apply(lambda row: f"<b>{row['country']}</b><br>"
                                            f"📊 Jobs Placed: {row['jobs_placed']:,}<br>"
                                            f"🎉 Events: {row['event_requested']:,}<br>"
                                            f"🤖 AI Requests: {row['ai_assistant_requested']:,}<br>"
                                            f"⭐ Satisfaction: {row['satisfaction_score']:.1f}/5", axis=1),
        name='Countries'
    ))
    
    # Update layout for orthographic (globe) projection
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=20, color='white'),
            y=0.95
        ),
        geo=dict(
            projection=dict(
                type='orthographic',  # This creates the globe effect
                rotation=dict(lon=20, lat=0, roll=0),  # Initial rotation centered on Africa
                scale=1.2
            ),
            showland=True,
            landcolor='#2a5f3a',
            oceancolor='#1a5276',
            coastlinecolor='#ffffff',
            coastlinewidth=0.8,
            showcountries=True,
            countrycolor='#dddddd',
            countrywidth=0.8,
            showocean=True,
            showlakes=True,
            lakecolor='#2e86c1',
            showrivers=True,
            rivercolor='#3498db',
            showframe=False,
            bgcolor='rgba(0,0,0,0)',
            lataxis=dict(showgrid=False),
            lonaxis=dict(showgrid=False)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    
    # Add instructions for users
    fig.add_annotation(
        text="💡 Drag to rotate | Scroll to zoom",
        xref="paper", yref="paper",
        x=0.5, y=-0.05,
        showarrow=False,
        font=dict(size=12, color="#888"),
        bgcolor="rgba(0,0,0,0.5)"
    )
    
    return fig

# ============================================
# FUNCTION TO AGGREGATE DATA BY TIME GRANULARITY
# ============================================
def aggregate_by_time(df, granularity, metric_col, agg_func='sum'):
    """Aggregate data by daily, weekly, monthly, quarterly, or yearly granularity"""
    
    if granularity == 'daily':
        time_col = 'date'
        df_agg = df.groupby(time_col)[metric_col].agg(agg_func).reset_index()
        df_agg = df_agg.sort_values(time_col)
        df_agg['x_label'] = df_agg[time_col]
        
    elif granularity == 'weekly':
        df_copy = df.copy()
        df_copy['week_num'] = df_copy['timestamp'].dt.isocalendar().week
        df_copy['year_week'] = df_copy['timestamp'].dt.strftime('%Y-W%W')
        df_agg = df_copy.groupby(['year_week', 'week_start'])[metric_col].agg(agg_func).reset_index()
        df_agg = df_agg.sort_values('week_start')
        df_agg['x_label'] = df_agg['year_week']
        
    elif granularity == 'monthly':
        df_agg = df.groupby('month')[metric_col].agg(agg_func).reset_index()
        df_agg = df_agg.sort_values('month')
        df_agg['x_label'] = df_agg['month']
        
    elif granularity == 'quarterly':
        df_copy = df.copy()
        df_copy['quarter_period'] = df_copy['quarter']
        df_agg = df_copy.groupby('quarter_period')[metric_col].agg(agg_func).reset_index()
        df_agg = df_agg.sort_values('quarter_period')
        df_agg['x_label'] = df_agg['quarter_period']
        
    else:  # yearly
        df_agg = df.groupby('year')[metric_col].agg(agg_func).reset_index()
        df_agg = df_agg.sort_values('year')
        df_agg['x_label'] = df_agg['year'].astype(str)
    
    return df_agg

# ============================================
# LOGIN PAGE LAYOUT (WITH BACKGROUND IMAGE)
# ============================================
login_layout = html.Div(
    className="login-background",
    children=[
        html.Div([
            html.Div([
                html.Div([
                    html.Img(src="https://cdn-icons-png.flaticon.com/512/6681/6681206.png",
                            style={"width": "80px", "margin": "0 auto 20px", "display": "block"}),
                    html.H2("AI-Solutions", className="text-center", style={"color": "white", "fontWeight": "bold"}),
                    html.H5("Analytics Dashboard", className="text-center", style={"color": "rgba(255,255,255,0.8)"}),
                    html.Hr(style={"backgroundColor": "rgba(255,255,255,0.3)"}),
                    dcc.Input(id="login-username", type="text", placeholder="Username", 
                             className="form-control mb-3", style={"padding": "12px"}),
                    dcc.Input(id="login-password", type="password", placeholder="Password", 
                             className="form-control mb-3", style={"padding": "12px"}),
                    html.Button("🔐 Sign In", id="login-button", className="btn btn-primary w-100", 
                               style={"padding": "12px", "fontWeight": "bold"}),
                    html.Div(id="login-message", className="text-center mt-3", style={"color": "#ff6b6b"}),
                    html.Hr(style={"backgroundColor": "rgba(255,255,255,0.3)"}),
                    html.P("Demo Accounts:", className="text-center text-muted small mb-1"),
                    html.P("📧 admin / admin123", className="text-center text-muted small mb-0"),
                    html.P("📧 user / user123", className="text-center text-muted small")
                ], className="card-body p-4")
            ], className="card", style={
                "backgroundColor": "rgba(25,25,45,0.92)", 
                "borderRadius": "20px", 
                "boxShadow": "0 20px 40px rgba(0,0,0,0.4)",
                "backdropFilter": "blur(3px)"
            })
        ], className="col-md-4 mx-auto", style={"marginTop": "15vh"})
    ],
    style={"minHeight": "100vh"}
)

# ============================================
# DASHBOARD LAYOUT (AFTER LOGIN)
# ============================================
def get_dashboard_layout(username):
    return html.Div([
        # Header with logout button and search
        html.Div([
            html.Div([
                html.H1("🤖 AI-Solutions Analytics Dashboard", className="mb-0", style={"color": "white"}),
                html.P("Jobs Placed | Job Types | Events & Demos | AI Virtual Assistant | Country Analysis", 
                       className="text-muted mb-0", style={"color": "rgba(255,255,255,0.7)"}),
            ], className="col-md-6"),
            html.Div([
                html.Span(f"👤 {username}", className="badge bg-success me-2 p-2", style={"fontSize": "14px"}),
                html.Button("🚪 Logout", id="logout-btn", className="btn btn-danger btn-sm", style={"padding": "8px 16px"}),
            ], className="col-md-3 text-end"),
        ], className="row p-3", style={"background": "linear-gradient(135deg, #1a1a2e, #16213e)", "borderRadius": "10px", "marginBottom": "20px"}),
        
        # SEARCH BAR SECTION
        html.Div([
            html.Div([
                html.I("🔍", style={"fontSize": "24px", "marginRight": "10px"}),
                html.H5("Search for any graph", className="mb-0 me-3", style={"color": "#333"}),
            ], className="d-flex align-items-center"),
            html.Div([
                dcc.Input(id="graph-search-input", type="text", 
                         placeholder="Type keywords like 'jobs', 'country', 'ai', 'events', 'satisfaction', 'map', 'trend', 'globe'...", 
                         className="form-control", style={"width": "400px", "borderRadius": "25px", "padding": "10px 20px"}),
            ], className="flex-grow-1 mx-3"),
            html.Div([
                html.Button("🔎 Search", id="search-btn", className="btn btn-primary", style={"borderRadius": "25px", "padding": "8px 25px"}),
                html.Button("🗑️ Clear", id="clear-search-btn", className="btn btn-secondary ms-2", style={"borderRadius": "25px"}),
            ], className="d-flex"),
        ], className="d-flex align-items-center p-3 bg-white rounded shadow-sm mb-3", style={"borderLeft": "4px solid #007bff"}),
        
        # Search Results Summary
        html.Div(id="search-results-summary", className="mb-2 text-muted small"),
        
        # Navigation Tabs
        dcc.Tabs(id="dashboard-tabs", value="tab-overview", children=[
            dcc.Tab(label="📊 Overview & KPIs", value="tab-overview", style={"fontWeight": "bold"}),
            dcc.Tab(label="🌍 Country Analysis (Rotating Globe)", value="tab-country", style={"fontWeight": "bold"}),
            dcc.Tab(label="💼 Jobs Placed", value="tab-jobs", style={"fontWeight": "bold"}),
            dcc.Tab(label="🛠️ Types of Jobs Requested", value="tab-job-types", style={"fontWeight": "bold"}),
            dcc.Tab(label="🎉 Demos & Events", value="tab-events", style={"fontWeight": "bold"}),
            dcc.Tab(label="🤖 AI Virtual Assistant", value="tab-ai", style={"fontWeight": "bold"}),
            dcc.Tab(label="📈 All Metrics by Country", value="tab-all-metrics", style={"fontWeight": "bold"}),
        ], style={"marginBottom": "20px"}),
        
        # Global Filters
        html.Div([
            html.Div([
                html.Label("📅 Date Range:", className="fw-bold me-2"),
                dcc.DatePickerRange(id="date-range", start_date=df['date'].min(), end_date=df['date'].max(), 
                                    display_format="YYYY-MM-DD", className="me-3"),
            ], className="d-flex align-items-center me-4"),
            html.Div([
                html.Label("🌍 Country:", className="fw-bold me-2"),
                dcc.Dropdown(id="country-filter", options=[{"label": "All Countries", "value": "ALL"}] + 
                            [{"label": c, "value": c} for c in sorted(df['country'].unique())], 
                            value="ALL", style={"width": "220px"}, className="me-3"),
            ], className="d-flex align-items-center"),
            html.Div([
                html.Label("🎯 Jump to:", className="fw-bold me-2"),
                dcc.Dropdown(id="graph-jump-dropdown", placeholder="Select a graph to jump to...",
                            options=[{"label": g["name"], "value": graph_id} for graph_id, g in GRAPH_LIBRARY.items()],
                            style={"width": "250px"}),
            ], className="d-flex align-items-center"),
        ], className="d-flex flex-wrap p-3 bg-light rounded mb-3", style={"alignItems": "center"}),
        
        # Content Div where graphs will be displayed
        html.Div(id="tab-content", className="container-fluid"),
        
        # Hidden div for client-side callback to trigger scroll
        html.Div(id="scroll-trigger", style={"display": "none"}),
        
        # Stores
        dcc.Store(id="filtered-data-store"),
        dcc.Store(id="search-result-store", data={}),
        
        # Stores for granularity states
        dcc.Store(id="jobs-granularity", data="monthly"),
        dcc.Store(id="events-granularity", data="monthly"),
        dcc.Store(id="ai-granularity", data="monthly"),
    ])

# ============================================
# MAIN APP LAYOUT (Conditional)
# ============================================
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="session-store", data={"logged_in": False, "username": ""}),
    html.Div(id="page-content", children=login_layout)
])

# ============================================
# AUTHENTICATION CALLBACK (Login Only)
# ============================================
@app.callback(
    [Output("page-content", "children"), Output("login-message", "children"), 
     Output("session-store", "data")],
    [Input("login-button", "n_clicks")],
    [State("login-username", "value"), State("login-password", "value"), 
     State("session-store", "data")]
)
def handle_login(login_clicks, username, password, session_data):
    if login_clicks and login_clicks > 0:
        if username and password:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            if username in USERS and USERS[username] == hashed:
                dashboard = get_dashboard_layout(username)
                return dashboard, "", {"logged_in": True, "username": username}
            return login_layout, "❌ Invalid username or password", {"logged_in": False, "username": ""}
        return login_layout, "❌ Please enter username and password", {"logged_in": False, "username": ""}
    return login_layout, "", {"logged_in": False, "username": ""}

# ============================================
# LOGOUT CALLBACK
# ============================================
@app.callback(
    Output("page-content", "children", allow_duplicate=True),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_logout(logout_clicks):
    if logout_clicks and logout_clicks > 0:
        return login_layout
    return dash.no_update

# ============================================
# SEARCH FUNCTION - Find graphs matching search term
# ============================================
def search_graphs(search_term):
    if not search_term or search_term.strip() == "":
        return []
    
    search_term_lower = search_term.lower()
    matches = []
    
    for graph_id, graph_info in GRAPH_LIBRARY.items():
        # Check name
        if search_term_lower in graph_info["name"].lower():
            matches.append({"id": graph_id, "name": graph_info["name"], "tab": graph_info["tab"], "score": 2})
            continue
        
        # Check keywords
        for keyword in graph_info["keywords"]:
            if search_term_lower in keyword or keyword in search_term_lower:
                matches.append({"id": graph_id, "name": graph_info["name"], "tab": graph_info["tab"], "score": 1})
                break
    
    # Remove duplicates and sort by score
    unique_matches = []
    seen = set()
    for match in matches:
        if match["id"] not in seen:
            seen.add(match["id"])
            unique_matches.append(match)
    
    return sorted(unique_matches, key=lambda x: -x["score"])

# ============================================
# SEARCH CALLBACK - Update search results and auto-navigate
# ============================================
@app.callback(
    [Output("search-results-summary", "children"),
     Output("dashboard-tabs", "value"),
     Output("graph-jump-dropdown", "value"),
     Output("scroll-trigger", "children")],
    [Input("search-btn", "n_clicks"), Input("clear-search-btn", "n_clicks"), Input("graph-jump-dropdown", "value")],
    [State("graph-search-input", "value"), State("dashboard-tabs", "value")]
)
def handle_search(search_clicks, clear_clicks, jump_value, search_term, current_tab):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "", no_update, no_update, ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Handle Clear button
    if trigger_id == "clear-search-btn":
        return "", no_update, None, ""
    
    # Handle Jump dropdown selection
    if trigger_id == "graph-jump-dropdown" and jump_value:
        graph_info = GRAPH_LIBRARY.get(jump_value)
        if graph_info:
            target_tab = graph_info["tab"]
            return f"🔍 Jumping to: {graph_info['name']}", target_tab, no_update, f"scroll-to-{jump_value}"
        return no_update, no_update, no_update, ""
    
    # Handle Search button
    if trigger_id == "search-btn" and search_term:
        matches = search_graphs(search_term)
        if matches:
            first_match = matches[0]
            target_tab = first_match["tab"]
            result_text = f"🔍 Found {len(matches)} graph(s) matching '{search_term}'. Jumping to: {first_match['name']}"
            return result_text, target_tab, matches[0]["id"], f"scroll-to-{matches[0]['id']}"
        else:
            return f"🔍 No graphs found matching '{search_term}'. Try: jobs, country, ai, events, map, globe, trend, satisfaction", no_update, None, ""
    
    return "", no_update, no_update, ""

# ============================================
# CALLBACK TO FILTER DATA
# ============================================
@app.callback(
    Output("filtered-data-store", "data"),
    [Input("date-range", "start_date"), Input("date-range", "end_date"), 
     Input("country-filter", "value")],
    prevent_initial_call=True
)
def filter_data(start_date, end_date, country):
    filtered = df.copy()
    
    if start_date and end_date:
        filtered = filtered[(filtered['date'] >= start_date) & (filtered['date'] <= end_date)]
    
    if country and country != "ALL":
        filtered = filtered[filtered['country'] == country]
    
    return filtered.to_json(date_format='iso', orient='split')

# ============================================
# CLIENT-SIDE CALLBACK FOR SCROLLING
# ============================================
app.clientside_callback(
    """
    function(trigger_value) {
        if (trigger_value && trigger_value.startsWith('scroll-to-')) {
            var elementId = trigger_value.replace('scroll-to-', '');
            var element = document.getElementById(elementId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                element.classList.add('highlight-graph');
                setTimeout(function() {
                    if (element) {
                        element.classList.remove('highlight-graph');
                    }
                }, 2000);
            }
        }
        return '';
    }
    """,
    Output("scroll-trigger", "children", allow_duplicate=True),
    Input("scroll-trigger", "children"),
    prevent_initial_call=True)

# ============================================
# JOBS GRANULARITY CALLBACKS
# ============================================
@app.callback(
    [Output("jobs-granularity", "data"),
     Output("jobs-granularity-daily", "className"),
     Output("jobs-granularity-weekly", "className"),
     Output("jobs-granularity-monthly", "className"),
     Output("jobs-granularity-quarterly", "className"),
     Output("jobs-granularity-yearly", "className")],
    [Input("jobs-granularity-daily", "n_clicks"),
     Input("jobs-granularity-weekly", "n_clicks"),
     Input("jobs-granularity-monthly", "n_clicks"),
     Input("jobs-granularity-quarterly", "n_clicks"),
     Input("jobs-granularity-yearly", "n_clicks")],
    [State("jobs-granularity", "data")],
    prevent_initial_call=True
)
def update_jobs_granularity(daily_clicks, weekly_clicks, monthly_clicks, quarterly_clicks, yearly_clicks, current_granularity):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_granularity, no_update, no_update, no_update, no_update, no_update
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if "daily" in trigger_id:
        new_granularity = "daily"
    elif "weekly" in trigger_id:
        new_granularity = "weekly"
    elif "quarterly" in trigger_id:
        new_granularity = "quarterly"
    elif "yearly" in trigger_id:
        new_granularity = "yearly"
    else:
        new_granularity = "monthly"
    
    # Set button classes
    classes = []
    for btn in ["daily", "weekly", "monthly", "quarterly", "yearly"]:
        if btn == new_granularity:
            classes.append("btn btn-sm btn-primary granularity-btn granularity-btn-active")
        else:
            classes.append("btn btn-sm btn-outline-primary granularity-btn")
    
    return new_granularity, classes[0], classes[1], classes[2], classes[3], classes[4]

@app.callback(
    Output("jobs-trend-graph", "children"),
    [Input("jobs-granularity", "data"),
     Input("filtered-data-store", "data")]
)
def update_jobs_trend(granularity, filtered_json):
    if filtered_json is None:
        current_df = df
    else:
        current_df = pd.read_json(filtered_json, orient='split')
    
    df_agg = aggregate_by_time(current_df, granularity, 'jobs_placed', 'sum')
    
    title_map = {
        'daily': 'Daily Jobs Placed Trend',
        'weekly': 'Weekly Jobs Placed Trend',
        'monthly': 'Monthly Jobs Placed Trend',
        'quarterly': 'Quarterly Jobs Placed Trend',
        'yearly': 'Yearly Jobs Placed Trend'
    }
    
    fig = px.line(df_agg, x='x_label', y='jobs_placed', 
                  title=f'📈 {title_map.get(granularity, "Jobs Placed Trend")}',
                  markers=True, 
                  labels={'x_label': 'Time Period', 'jobs_placed': 'Jobs Placed'})
    fig.update_layout(height=450)
    
    return dcc.Graph(figure=fig)

# ============================================
# EVENTS GRANULARITY CALLBACKS
# ============================================
@app.callback(
    [Output("events-granularity", "data"),
     Output("events-granularity-daily", "className"),
     Output("events-granularity-weekly", "className"),
     Output("events-granularity-monthly", "className"),
     Output("events-granularity-quarterly", "className"),
     Output("events-granularity-yearly", "className")],
    [Input("events-granularity-daily", "n_clicks"),
     Input("events-granularity-weekly", "n_clicks"),
     Input("events-granularity-monthly", "n_clicks"),
     Input("events-granularity-quarterly", "n_clicks"),
     Input("events-granularity-yearly", "n_clicks")],
    [State("events-granularity", "data")],
    prevent_initial_call=True
)
def update_events_granularity(daily_clicks, weekly_clicks, monthly_clicks, quarterly_clicks, yearly_clicks, current_granularity):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_granularity, no_update, no_update, no_update, no_update, no_update
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if "daily" in trigger_id:
        new_granularity = "daily"
    elif "weekly" in trigger_id:
        new_granularity = "weekly"
    elif "quarterly" in trigger_id:
        new_granularity = "quarterly"
    elif "yearly" in trigger_id:
        new_granularity = "yearly"
    else:
        new_granularity = "monthly"
    
    # Set button classes
    classes = []
    for btn in ["daily", "weekly", "monthly", "quarterly", "yearly"]:
        if btn == new_granularity:
            classes.append("btn btn-sm btn-primary granularity-btn granularity-btn-active")
        else:
            classes.append("btn btn-sm btn-outline-primary granularity-btn")
    
    return new_granularity, classes[0], classes[1], classes[2], classes[3], classes[4]

@app.callback(
    Output("events-trend-graph", "children"),
    [Input("events-granularity", "data"),
     Input("filtered-data-store", "data")]
)
def update_events_trend(granularity, filtered_json):
    if filtered_json is None:
        current_df = df
    else:
        current_df = pd.read_json(filtered_json, orient='split')
    
    df_agg = aggregate_by_time(current_df, granularity, 'event_requested', 'sum')
    
    title_map = {
        'daily': 'Daily Event Requests Trend',
        'weekly': 'Weekly Event Requests Trend',
        'monthly': 'Monthly Event Requests Trend',
        'quarterly': 'Quarterly Event Requests Trend',
        'yearly': 'Yearly Event Requests Trend'
    }
    
    fig = px.line(df_agg, x='x_label', y='event_requested', 
                  title=f'📈 {title_map.get(granularity, "Event Requests Trend")}',
                  markers=True, 
                  labels={'x_label': 'Time Period', 'event_requested': 'Event Requests'})
    fig.update_layout(height=450)
    
    return dcc.Graph(figure=fig)

# ============================================
# AI GRANULARITY CALLBACKS
# ============================================
@app.callback(
    [Output("ai-granularity", "data"),
     Output("ai-granularity-daily", "className"),
     Output("ai-granularity-weekly", "className"),
     Output("ai-granularity-monthly", "className"),
     Output("ai-granularity-quarterly", "className"),
     Output("ai-granularity-yearly", "className")],
    [Input("ai-granularity-daily", "n_clicks"),
     Input("ai-granularity-weekly", "n_clicks"),
     Input("ai-granularity-monthly", "n_clicks"),
     Input("ai-granularity-quarterly", "n_clicks"),
     Input("ai-granularity-yearly", "n_clicks")],
    [State("ai-granularity", "data")],
    prevent_initial_call=True
)
def update_ai_granularity(daily_clicks, weekly_clicks, monthly_clicks, quarterly_clicks, yearly_clicks, current_granularity):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_granularity, no_update, no_update, no_update, no_update, no_update
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if "daily" in trigger_id:
        new_granularity = "daily"
    elif "weekly" in trigger_id:
        new_granularity = "weekly"
    elif "quarterly" in trigger_id:
        new_granularity = "quarterly"
    elif "yearly" in trigger_id:
        new_granularity = "yearly"
    else:
        new_granularity = "monthly"
    
    # Set button classes
    classes = []
    for btn in ["daily", "weekly", "monthly", "quarterly", "yearly"]:
        if btn == new_granularity:
            classes.append("btn btn-sm btn-primary granularity-btn granularity-btn-active")
        else:
            classes.append("btn btn-sm btn-outline-primary granularity-btn")
    
    return new_granularity, classes[0], classes[1], classes[2], classes[3], classes[4]

@app.callback(
    Output("ai-trend-graph", "children"),
    [Input("ai-granularity", "data"),
     Input("filtered-data-store", "data")]
)
def update_ai_trend(granularity, filtered_json):
    if filtered_json is None:
        current_df = df
    else:
        current_df = pd.read_json(filtered_json, orient='split')
    
    df_agg = aggregate_by_time(current_df, granularity, 'ai_assistant_requested', 'sum')
    
    title_map = {
        'daily': 'Daily AI Assistant Requests Trend',
        'weekly': 'Weekly AI Assistant Requests Trend',
        'monthly': 'Monthly AI Assistant Requests Trend',
        'quarterly': 'Quarterly AI Assistant Requests Trend',
        'yearly': 'Yearly AI Assistant Requests Trend'
    }
    
    fig = px.line(df_agg, x='x_label', y='ai_assistant_requested', 
                  title=f'🤖 {title_map.get(granularity, "AI Assistant Requests Trend")}',
                  markers=True, 
                  labels={'x_label': 'Time Period', 'ai_assistant_requested': 'AI Requests'})
    fig.update_layout(height=450)
    
    return dcc.Graph(figure=fig)

# ============================================
# MAIN CALLBACK FOR ALL TABS (except granularity-driven ones)
# ============================================
@app.callback(
    Output("tab-content", "children"),
    [Input("dashboard-tabs", "value"), Input("filtered-data-store", "data")]
)
def render_tab(tab_name, filtered_json):
    if filtered_json is None:
        current_df = df
    else:
        current_df = pd.read_json(filtered_json, orient='split')
    
    if len(current_df) == 0:
        return html.Div("No data available for the selected filters.", className="alert alert-warning")
    
    total_records = len(current_df)
    total_jobs = current_df['jobs_placed'].sum()
    total_events = current_df['event_requested'].sum()
    total_ai = current_df['ai_assistant_requested'].sum()
    
    # ========================================
    # TAB 1: OVERVIEW & KPIs
    # ========================================
    if tab_name == "tab-overview":
        kpis = html.Div([
            html.Div([
                html.Div("🌍 Total Countries", className="text-muted small"),
                html.H2(f"{current_df['country'].nunique()}", className="mb-0 text-primary"),
                html.Small("active regions", className="text-muted")
            ], className="col-md-3 card p-3 text-center shadow-sm m-1"),
            html.Div([
                html.Div("💼 Jobs Placed", className="text-muted small"),
                html.H2(f"{total_jobs:,}", className="mb-0 text-success"),
                html.Small(f"from {total_records:,} sessions", className="text-muted")
            ], className="col-md-3 card p-3 text-center shadow-sm m-1"),
            html.Div([
                html.Div("🎉 Event Requests", className="text-muted small"),
                html.H2(f"{total_events:,}", className="mb-0 text-warning"),
                html.Small(f"{(total_events/total_records*100):.1f}% rate", className="text-muted")
            ], className="col-md-3 card p-3 text-center shadow-sm m-1"),
            html.Div([
                html.Div("🤖 AI Assistant Requests", className="text-muted small"),
                html.H2(f"{total_ai:,}", className="mb-0 text-info"),
                html.Small(f"{(total_ai/total_records*100):.1f}% rate", className="text-muted")
            ], className="col-md-3 card p-3 text-center shadow-sm m-1"),
        ], className="row g-2 mb-4")
        
        kpis2 = html.Div([
            html.Div([
                html.Div("⭐ Avg Satisfaction", className="text-muted small"),
                html.H2(f"{current_df['satisfaction_score'].mean():.1f}", className="mb-0"),
                html.Small("/5 stars", className="text-muted")
            ], className="col-md-3 card p-3 text-center shadow-sm m-1"),
            html.Div([
                html.Div("📊 AI Usage Rate", className="text-muted small"),
                html.H2(f"{current_df['ai_usage_rate'].mean():.0f}%", className="mb-0"),
                html.Small("avg per location", className="text-muted")
            ], className="col-md-3 card p-3 text-center shadow-sm m-1"),
            html.Div([
                html.Div("📈 Escalation Rate", className="text-muted small"),
                html.H2(f"{current_df['escalation_rate'].mean():.0f}%", className="mb-0"),
                html.Small("AI → Human", className="text-muted")
            ], className="col-md-3 card p-3 text-center shadow-sm m-1"),
            html.Div([
                html.Div("⏱️ Resolution Time", className="text-muted small"),
                html.H2(f"{current_df['resolution_time_minutes'].mean():.0f}", className="mb-0"),
                html.Small("minutes avg", className="text-muted")
            ], className="col-md-3 card p-3 text-center shadow-sm m-1"),
        ], className="row g-2 mb-4")
        
        # Graph 1: Jobs by Country
        jobs_by_country = current_df.groupby('country')['jobs_placed'].sum().reset_index().sort_values('jobs_placed', ascending=False)
        fig_jobs_by_country = px.bar(jobs_by_country, x='country', y='jobs_placed', title='💼 Total Jobs Placed by Country',
                      color='jobs_placed', color_continuous_scale='Blues')
        fig_jobs_by_country.update_layout(height=450)
        
        # Graph 2: Events by Country
        events_by_country = current_df.groupby('country')['event_requested'].sum().reset_index().sort_values('event_requested', ascending=False)
        fig_events_by_country = px.bar(events_by_country, x='country', y='event_requested', title='🎉 Event Requests by Country',
                      color='event_requested', color_continuous_scale='Oranges')
        fig_events_by_country.update_layout(height=450)
        
        # Graph 3: AI by Country
        ai_by_country = current_df.groupby('country')['ai_assistant_requested'].sum().reset_index().sort_values('ai_assistant_requested', ascending=False)
        fig_ai_by_country = px.bar(ai_by_country, x='country', y='ai_assistant_requested', title='🤖 AI Assistant Requests by Country',
                      color='ai_assistant_requested', color_continuous_scale='Greens')
        fig_ai_by_country.update_layout(height=450)
        
        # Graph 4: Satisfaction Score by Region
        sat_by_region = current_df.groupby('region')['satisfaction_score'].mean().reset_index()
        fig_satisfaction = px.bar(sat_by_region, x='region', y='satisfaction_score', title='⭐ Satisfaction Score by Region',
                                   color='satisfaction_score', color_continuous_scale='RdYlGn', range_color=[1,5])
        
        # Graph 5: AI Usage Rate by Region
        usage_by_region = current_df.groupby('region')['ai_usage_rate'].mean().reset_index()
        fig_usage = px.bar(usage_by_region, x='region', y='ai_usage_rate', title='📊 AI Usage Rate by Region (%)',
                            color='ai_usage_rate', color_continuous_scale='Greens')
        
        # Graph 6: Escalation Rate by Region
        escalation_by_region = current_df.groupby('region')['escalation_rate'].mean().reset_index()
        fig_escalation = px.bar(escalation_by_region, x='region', y='escalation_rate', title='📈 Escalation Rate by Region (%)',
                                 color='escalation_rate', color_continuous_scale='Reds')
        
        # Graph 7: Resolution Time by Office
        resolution_by_office = current_df.groupby('office_location')['resolution_time_minutes'].mean().reset_index()
        fig_resolution = px.bar(resolution_by_office, x='office_location', y='resolution_time_minutes', title='⏱️ Resolution Time by Office Location',
                                 color='resolution_time_minutes', color_continuous_scale='Reds')
        
        return html.Div([
            html.Div(id="overview-kpis", className="graph-section", children=[kpis, kpis2]),
            html.Div(id="jobs-by-country", className="graph-section mt-4", children=[html.H5("📊 Graph: Jobs Placed by Country", className="mb-2"), dcc.Graph(figure=fig_jobs_by_country)]),
            html.Div(id="events-by-country", className="graph-section mt-4", children=[html.H5("📊 Graph: Event Requests by Country", className="mb-2"), dcc.Graph(figure=fig_events_by_country)]),
            html.Div(id="ai-by-country", className="graph-section mt-4", children=[html.H5("📊 Graph: AI Requests by Country", className="mb-2"), dcc.Graph(figure=fig_ai_by_country)]),
            html.Div(id="satisfaction-score", className="graph-section mt-4", children=[html.H5("📊 Graph: Satisfaction Score by Region", className="mb-2"), dcc.Graph(figure=fig_satisfaction)]),
            html.Div(id="ai-usage-rate", className="graph-section mt-4", children=[html.H5("📊 Graph: AI Usage Rate by Region", className="mb-2"), dcc.Graph(figure=fig_usage)]),
            html.Div(id="escalation-rate", className="graph-section mt-4", children=[html.H5("📊 Graph: Escalation Rate by Region", className="mb-2"), dcc.Graph(figure=fig_escalation)]),
            html.Div(id="resolution-time", className="graph-section mt-4", children=[html.H5("📊 Graph: Resolution Time by Office", className="mb-2"), dcc.Graph(figure=fig_resolution)]),
        ])
    
    # ========================================
    # TAB 2: COUNTRY ANALYSIS WITH ROTATING GLOBE (WITH ENHANCED TITLE)
    # ========================================
    elif tab_name == "tab-country":
        # Create the rotating globe map
        fig_map = create_rotating_globe(current_df, "🌍 Interactive Rotating Globe - Drag to Spin | Hover for Details")
        
        # Bar chart comparison
        country_comparison = current_df.groupby('country').agg({
            'jobs_placed': 'sum',
            'event_requested': 'sum',
            'ai_assistant_requested': 'sum'
        }).reset_index().sort_values('jobs_placed', ascending=False)
        
        fig_comparison = px.bar(country_comparison, x='country', y=['jobs_placed', 'event_requested', 'ai_assistant_requested'],
                                 title='Country Comparison: Jobs vs Events vs AI Requests',
                                 barmode='group')
        fig_comparison.update_layout(height=450)
        
        # Get current date range for subtitle
        date_range_text = f"Data Period: {current_df['date'].min()} to {current_df['date'].max()}"
        
        return html.Div([
            # Enhanced Title Section for Globe Map
            html.Div([
                html.H2([
                    html.Span("🌍 ", style={"fontSize": "32px"}),
                    html.Span("AI-Solutions Global Activity Atlas", style={"fontWeight": "bold"}),
                    html.Span(" 🌍", style={"fontSize": "32px"})
                ], style={"margin": "0", "fontSize": "28px"}),
                html.P([
                    "Interactive 3D Rotating Globe | ",
                    html.Span("📊 Jobs Placed", style={"color": "#4CAF50", "fontWeight": "bold"}),
                    " | ",
                    html.Span("🎉 Events", style={"color": "#FF9800", "fontWeight": "bold"}),
                    " | ",
                    html.Span("🤖 AI Assistant", style={"color": "#2196F3", "fontWeight": "bold"}),
                    " | ",
                    html.Span("⭐ Satisfaction Scores", style={"color": "#9C27B0", "fontWeight": "bold"})
                ], style={"margin": "10px 0 0 0", "fontSize": "14px"}),
                html.P([
                    html.Span("📅 ", style={"fontSize": "12px"}),
                    html.Span(date_range_text, style={"fontSize": "12px"}),
                    html.Span(" | 💡 Tip: Click and drag to rotate the globe | Scroll to zoom", style={"fontSize": "12px", "fontStyle": "italic"})
                ], style={"margin": "5px 0 0 0", "color": "#666"})
            ], className="globe-title"),
            
            # Globe Map Container
            html.Div(id="world-map-globe", className="graph-section globe-container", children=[
                dcc.Graph(figure=fig_map, config={'displayModeBar': True, 'scrollZoom': True})
            ]),
            
            # Country Comparison Chart
            html.Div(id="country-comparison", className="graph-section mt-4", children=[
                html.H4("📊 Country Performance Comparison", className="mb-3"),
                dcc.Graph(figure=fig_comparison)
            ]),
        ])
    
    # ========================================
    # TAB 3: JOBS PLACED (WITH TIME GRANULARITY)
    # ========================================
    elif tab_name == "tab-jobs":
        # Add time granularity selector
        granularity_selector = html.Div([
            html.Label("📊 Time Granularity:", className="fw-bold me-2"),
            html.Div([
                html.Button("Daily", id="jobs-granularity-daily", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
                html.Button("Weekly", id="jobs-granularity-weekly", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
                html.Button("Monthly", id="jobs-granularity-monthly", className="btn btn-sm btn-primary granularity-btn granularity-btn-active", n_clicks=0),
                html.Button("Quarterly", id="jobs-granularity-quarterly", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
                html.Button("Yearly", id="jobs-granularity-yearly", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
            ], className="time-granularity-group")
        ], className="d-flex align-items-center mb-3")
        
        jobs_country = current_df.groupby('country')['jobs_placed'].sum().reset_index().sort_values('jobs_placed', ascending=False)
        fig1 = px.bar(jobs_country, x='country', y='jobs_placed', title='💼 Total Jobs Placed by Country',
                      color='jobs_placed', color_continuous_scale='Blues', text='jobs_placed')
        fig1.update_traces(textposition='outside')
        fig1.update_layout(height=450)
        
        jobs_dept = current_df.groupby('job_department')['jobs_placed'].sum().reset_index().sort_values('jobs_placed', ascending=False)
        fig2 = px.bar(jobs_dept, x='job_department', y='jobs_placed', title='💼 Jobs Placed by Department',
                      color='jobs_placed', color_continuous_scale='Teal')
        fig2.update_layout(height=450)
        
        jobs_salary = current_df.groupby('job_salary_band')['jobs_placed'].sum().reset_index()
        fig3 = px.pie(jobs_salary, values='jobs_placed', names='job_salary_band', title='💰 Jobs Distribution by Salary Band',
                      hole=0.3, color_discrete_sequence=px.colors.qualitative.Set2)
        fig3.update_layout(height=450)
        
        return html.Div([
            html.H4("💼 Jobs Placed Analytics", className="mb-3"),
            html.Div([
                html.Div([
                    granularity_selector,
                    html.Div(id="jobs-trend-graph", children=[dcc.Graph(figure=px.line(title="Loading..."))])
                ], className="graph-section", id="jobs-trend")
            ]),
            html.Div([
                html.Div([html.H5("Jobs by Country"), dcc.Graph(figure=fig1)], className="col-md-6 graph-section", id="jobs-country"), 
                html.Div([html.H5("Jobs by Department"), dcc.Graph(figure=fig2)], className="col-md-6 graph-section", id="jobs-department")
            ], className="row mt-4"),
            html.Div([
                html.Div([html.H5("Jobs by Salary Band"), dcc.Graph(figure=fig3)], className="col-md-6 graph-section", id="jobs-salary")
            ], className="row mt-3"),
        ])
    
    # ========================================
    # TAB 4: TYPES OF JOBS REQUESTED
    # ========================================
    elif tab_name == "tab-job-types":
        top_jobs = current_df['job_title'].value_counts().head(15).reset_index()
        top_jobs.columns = ['Job Title', 'Count']
        fig1 = px.bar(top_jobs, x='Count', y='Job Title', title='🔝 Top 15 Most Requested Job Types',
                      orientation='h', color='Count', color_continuous_scale='Viridis')
        fig1.update_layout(height=550)
        
        job_dept = current_df.groupby(['job_department', 'job_title']).size().reset_index(name='count')
        job_dept = job_dept.sort_values('count', ascending=False).head(20)
        fig2 = px.treemap(job_dept, path=['job_department', 'job_title'], values='count',
                          title='📊 Job Types Distribution by Department')
        fig2.update_layout(height=500)
        
        exp_level = current_df['job_experience_level'].value_counts().reset_index()
        exp_level.columns = ['Experience Level', 'Count']
        fig3 = px.bar(exp_level, x='Experience Level', y='Count', title='📈 Job Demand by Experience Level',
                      color='Experience Level')
        fig3.update_layout(height=450)
        
        remote_data = current_df['job_remote_allowed'].value_counts().reset_index()
        remote_data.columns = ['Remote Allowed', 'Count']
        remote_data['Remote Allowed'] = remote_data['Remote Allowed'].map({True: '✅ Remote Allowed', False: '🏢 On-Site Only'})
        fig4 = px.pie(remote_data, values='Count', names='Remote Allowed', title='🏠 Remote vs On-Site Job Opportunities',
                      hole=0.3, color_discrete_sequence=['#2ecc71', '#e74c3c'])
        fig4.update_layout(height=450)
        
        return html.Div([
            html.H4("🛠️ Types of Jobs Requested Analysis", className="mb-3"),
            html.Div(id="top-job-titles", className="graph-section", children=[dcc.Graph(figure=fig1)]),
            html.Div(id="job-department-treemap", className="graph-section mt-4", children=[dcc.Graph(figure=fig2)]),
            html.Div(id="experience-level", className="graph-section mt-4", children=[dcc.Graph(figure=fig3)]),
            html.Div(id="remote-jobs", className="graph-section mt-4", children=[dcc.Graph(figure=fig4)]),
        ])
    
    # ========================================
    # TAB 5: DEMOS & EVENTS (WITH TIME GRANULARITY)
    # ========================================
    elif tab_name == "tab-events":
        # Add time granularity selector for events
        granularity_selector_events = html.Div([
            html.Label("📊 Time Granularity:", className="fw-bold me-2"),
            html.Div([
                html.Button("Daily", id="events-granularity-daily", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
                html.Button("Weekly", id="events-granularity-weekly", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
                html.Button("Monthly", id="events-granularity-monthly", className="btn btn-sm btn-primary granularity-btn granularity-btn-active", n_clicks=0),
                html.Button("Quarterly", id="events-granularity-quarterly", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
                html.Button("Yearly", id="events-granularity-yearly", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
            ], className="time-granularity-group")
        ], className="d-flex align-items-center mb-3")
        
        event_dist = current_df[current_df['event_requested'] == True]['event_type'].value_counts().reset_index()
        event_dist.columns = ['Event Type', 'Count']
        fig1 = px.bar(event_dist, x='Event Type', y='Count', title='🎉 Event Requests by Type',
                      color='Count', color_continuous_scale='Oranges')
        fig1.update_layout(height=450)
        
        events_country = current_df.groupby('country')['event_requested'].sum().reset_index().sort_values('event_requested', ascending=False)
        fig2 = px.bar(events_country, x='country', y='event_requested', title='🎉 Event Requests by Country',
                      color='event_requested', color_continuous_scale='Reds')
        fig2.update_layout(height=450)
        
        attendance = current_df[current_df['event_requested'] == True]['event_attended'].value_counts().reset_index()
        attendance.columns = ['Attended', 'Count']
        attendance['Attended'] = attendance['Attended'].map({True: '✅ Attended', False: '❌ No Show'})
        fig3 = px.pie(attendance, values='Count', names='Attended', title='📅 Event Attendance Rate',
                      hole=0.3, color_discrete_sequence=['#2ecc71', '#e74c3c'])
        fig3.update_layout(height=400)
        
        return html.Div([
            html.H4("🎉 Schedule Demos & Promotional Events Analysis", className="mb-3"),
            html.Div([
                html.Div([
                    granularity_selector_events,
                    html.Div(id="events-trend-graph", children=[dcc.Graph(figure=px.line(title="Loading..."))])
                ], className="graph-section", id="event-trend")
            ]),
            html.Div([
                html.Div([html.H5("Event Types"), dcc.Graph(figure=fig1)], className="col-md-6 graph-section", id="event-types"), 
                html.Div([html.H5("Events by Country"), dcc.Graph(figure=fig2)], className="col-md-6 graph-section", id="events-country")
            ], className="row mt-4"),
            html.Div([
                html.Div([html.H5("Event Attendance Rate"), dcc.Graph(figure=fig3)], className="col-md-6 graph-section", id="event-attendance")
            ], className="row mt-3"),
        ])
    
    # ========================================
    # TAB 6: AI VIRTUAL ASSISTANT
    # ========================================
    elif tab_name == "tab-ai":
        # Add time granularity selector for AI
        granularity_selector_ai = html.Div([
            html.Label("📊 Time Granularity:", className="fw-bold me-2"),
            html.Div([
                html.Button("Daily", id="ai-granularity-daily", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
                html.Button("Weekly", id="ai-granularity-weekly", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
                html.Button("Monthly", id="ai-granularity-monthly", className="btn btn-sm btn-primary granularity-btn granularity-btn-active", n_clicks=0),
                html.Button("Quarterly", id="ai-granularity-quarterly", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
                html.Button("Yearly", id="ai-granularity-yearly", className="btn btn-sm btn-outline-primary granularity-btn", n_clicks=0),
            ], className="time-granularity-group")
        ], className="d-flex align-items-center mb-3")
        
        ai_queries = current_df[current_df['ai_assistant_requested'] == True]['ai_query_type'].value_counts().reset_index()
        ai_queries.columns = ['Query Type', 'Count']
        fig1 = px.bar(ai_queries, x='Query Type', y='Count', title='🤖 AI Virtual Assistant - Query Types',
                      color='Count', color_continuous_scale='Greens')
        fig1.update_layout(height=450)
        
        ai_helpful = current_df[current_df['ai_assistant_requested'] == True]['ai_helpful'].value_counts().reset_index()
        ai_helpful.columns = ['Helpful', 'Count']
        ai_helpful['Helpful'] = ai_helpful['Helpful'].map({True: '✅ Helpful', False: '❌ Not Helpful'})
        fig2 = px.pie(ai_helpful, values='Count', names='Helpful', title='🤖 AI Assistant Helpfulness Rating',
                      hole=0.3, color_discrete_sequence=['#2ecc71', '#e74c3c'])
        fig2.update_layout(height=400)
        
        ai_satisfaction = current_df[current_df['ai_assistant_requested'] == True]['ai_satisfaction'].value_counts().sort_index().reset_index()
        ai_satisfaction.columns = ['Rating', 'Count']
        fig3 = px.bar(ai_satisfaction, x='Rating', y='Count', title='⭐ AI Assistant Satisfaction Score Distribution (1-5)',
                      color='Rating', color_continuous_scale='RdYlGn', range_color=[1,5])
        fig3.update_layout(height=450)
        
        ai_country = current_df.groupby('country')['ai_assistant_requested'].sum().reset_index().sort_values('ai_assistant_requested', ascending=False)
        fig4 = px.bar(ai_country, x='country', y='ai_assistant_requested', title='🤖 AI Assistant Requests by Country',
                      color='ai_assistant_requested', color_continuous_scale='Teal')
        fig4.update_layout(height=450)
        
        return html.Div([
            html.H4("🤖 AI-Powered Virtual Assistant Analytics", className="mb-3"),
            html.Div([
                html.Div([
                    granularity_selector_ai,
                    html.Div(id="ai-trend-graph", children=[dcc.Graph(figure=px.line(title="Loading..."))])
                ], className="graph-section", id="ai-trend")
            ]),
            html.Div(id="ai-query-types", className="graph-section mt-4", children=[dcc.Graph(figure=fig1)]),
            html.Div([
                html.Div([html.H5("AI Helpfulness"), dcc.Graph(figure=fig2)], className="col-md-6 graph-section", id="ai-helpfulness"), 
                html.Div([html.H5("AI Satisfaction"), dcc.Graph(figure=fig3)], className="col-md-6 graph-section", id="ai-satisfaction")
            ], className="row mt-4"),
            html.Div(id="ai-country", className="graph-section mt-4", children=[dcc.Graph(figure=fig4)]),
        ])
    
    # ========================================
    # TAB 7: ALL METRICS BY COUNTRY
    # ========================================
    elif tab_name == "tab-all-metrics":
        country_metrics = current_df.groupby('country').agg({
            'jobs_placed': 'sum',
            'job_title': 'count',
            'event_requested': 'sum',
            'ai_assistant_requested': 'sum',
            'satisfaction_score': 'mean',
            'ai_usage_rate': 'mean',
            'escalation_rate': 'mean',
            'resolution_time_minutes': 'mean'
        }).reset_index()
        country_metrics.columns = ['Country', 'Jobs Placed', 'Total Sessions', 'Event Requests', 'AI Requests', 
                                   'Avg Satisfaction', 'AI Usage Rate %', 'Escalation Rate %', 'Avg Resolution Time (min)']
        country_metrics = country_metrics.round(1)
        
        table_header = html.Thead(html.Tr([html.Th(col, className="px-3 py-2 bg-dark text-white") for col in country_metrics.columns]))
        table_body = html.Tbody([
            html.Tr([html.Td(str(row[col]), className="px-3 py-2") for col in country_metrics.columns])
            for _, row in country_metrics.iterrows()
        ])
        
        metrics_table = html.Table([table_header, table_body], className="table table-striped table-hover table-bordered", style={"fontSize": "14px"})
        
        return html.Div([
            html.H4("📈 All Metrics by Country - Comprehensive Report", className="mb-3"),
            html.Div(id="all-metrics-table", className="graph-section", children=[metrics_table]),
        ])
    
    return html.Div("Select a tab to view analytics")

# ============================================
# RUN THE APP
# ============================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🚀 DASHBOARD READY - SINGLE LOGIN REQUIRED")
    print("=" * 70)
    print("\n📍 http://127.0.0.1:8050")
    print("\n🔐 Demo Accounts (Login once, then access all graphs):")
    print("   📧 Username: admin  |  Password: admin123")
    print("   📧 Username: user   |  Password: user123")
    print("\n🌍 ROTATING ATLAS-STYLE GLOBE MAP WITH ENHANCED TITLE:")
    print("   ✅ Beautiful gradient title section at the top")
    print("   ✅ 3D Orthographic Projection (like a real globe)")
    print("   ✅ Click and drag to rotate the Earth")
    print("   ✅ Scroll to zoom in/out")
    print("   ✅ Hover over countries for detailed metrics")
    print("   ✅ Shows current data period and key metrics legend")
    print("\n📊 TIME GRANULARITY CONTROLS:")
    print("   ✅ Daily, Weekly, Monthly, Quarterly, Yearly views available")
    print("   ✅ Found in Jobs, Events, and AI Assistant tabs")
    print("   ✅ Click any button to instantly change time aggregation")
    print("   ✅ Active button highlighted in blue")
    print("\n🔍 GRAPH SEARCH:")
    print("   Type keywords like 'globe', 'map', 'jobs', 'country', 'ai', 'events'")
    print("   Click Search - Automatically switches tab and scrolls to matching graph")
    print("\n🎨 LOGIN PAGE:")
    print("   ✅ Beautiful technology background image")
    print("   ✅ Semi-transparent card with blur effect")
    print("   ✅ Professional gradient overlay")
    print("\n📊 Dashboard Includes:")
    print("   ✅ Rotating 3D Globe Map (Atlas-style) with enhanced title")
    print("   ✅ Country Analysis Charts")
    print("   ✅ Number of Jobs Placed")
    print("   ✅ Types of Jobs Requested (15+ job types)")
    print("   ✅ Schedule Demos & Promotional Events")
    print("   ✅ AI-Powered Virtual Assistant Requests")
    print("   ✅ All Metrics by Country Table")
    print("   ✅ Time granularity controls (Daily/Weekly/Monthly/Quarterly/Yearly)")
    print("\n🚀 Starting server...\n")
    app.run(debug=True, port=8050)