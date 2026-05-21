"""
NAFISA'S VISUAL CAREER DASHBOARD
Modern web-based dashboard for tracking job search progress
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json

# Page config
st.set_page_config(
    page_title="Career Dashboard | Nafisa Anjum",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f1f1f;
        font-weight: 600;
    }
    h3 {
        color: #4a4a4a;
        font-weight: 500;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class DashboardData:
    def __init__(self):
        self.data_dir = "career_data"
        self.ensure_data_files()
    
    def ensure_data_files(self):
        """Create data files if they don't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        files = {
            'applications.csv': pd.DataFrame(columns=['date', 'company', 'role', 'status', 'url', 'notes']),
            'interviews.csv': pd.DataFrame(columns=['date', 'company', 'role', 'stage', 'result', 'notes']),
            'daily_log.csv': pd.DataFrame(columns=['date', 'applications_sent', 'hours_focused', 'tasks_completed', 'posts_made']),
            'learning_log.csv': pd.DataFrame(columns=['date', 'tool_practiced', 'time_spent', 'completed', 'notes'])
        }
        
        for filename, df in files.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                df.to_csv(filepath, index=False)
        
        # Create goals and learning plan JSONs
        goals_path = os.path.join(self.data_dir, 'goals.json')
        if not os.path.exists(goals_path):
            goals = {
                'month_1': {'applications': 40, 'interviews': 3, 'posts': 5},
                'month_2': {'applications': 100, 'interviews': 10, 'offers': 2},
                'month_3': {'job_secured': True, 'salary': 60000}
            }
            with open(goals_path, 'w') as f:
                json.dump(goals, f, indent=2)
        
        learning_path = os.path.join(self.data_dir, 'learning_plan.json')
        if not os.path.exists(learning_path):
            learning = {
                'tier_1': {'ChatGPT': False, 'Claude': False, 'Gemini': False, 'Prompt_Engineering': False},
                'tier_2': {'Google_Analytics': False, 'SQL': False, 'Notion': False, 'Support_Tools': False},
                'tier_3': {'AI_Concepts': False, 'Product_Feedback': False, 'Metrics': False},
                'tier_4': {'Demo_Project': False, 'Blog_Posts': False}
            }
            with open(learning_path, 'w') as f:
                json.dump(learning, f, indent=2)
    
    def load_data(self, filename):
        """Load CSV data"""
        filepath = os.path.join(self.data_dir, filename)
        return pd.read_csv(filepath)
    
    def load_json(self, filename):
        """Load JSON data"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def save_data(self, filename, df):
        """Save CSV data"""
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath, index=False)

# Initialize data
@st.cache_resource
def init_dashboard():
    return DashboardData()

data = init_dashboard()

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150/667eea/ffffff?text=NA", width=100)
    st.title("Nafisa Anjum")
    st.caption("AI Product Specialist")
    
    st.divider()
    
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "➕ Add Application", "📚 Learning", "🎯 Goals", "📈 Analytics"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Quick stats in sidebar
    apps_df = data.load_data('applications.csv')
    st.metric("Total Applications", len(apps_df))
    
    if not apps_df.empty:
        apps_df['date'] = pd.to_datetime(apps_df['date'])
        week_ago = datetime.now() - timedelta(days=7)
        week_apps = apps_df[apps_df['date'] >= week_ago]
        st.metric("This Week", len(week_apps), f"+{len(week_apps)}")

# Main content
if page == "📊 Dashboard":
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        current_time = datetime.now()
        greeting = "Good morning" if current_time.hour < 12 else "Good afternoon" if current_time.hour < 18 else "Good evening"
        st.title(f"{greeting}, Nafisa")
        st.caption(f"Today is {current_time.strftime('%A, %B %d, %Y')}")
    
    with col2:
        st.markdown(f"### {current_time.strftime('%B %Y')}")
    
    st.divider()
    
    # Load data
    apps_df = data.load_data('applications.csv')
    interviews_df = data.load_data('interviews.csv')
    daily_df = data.load_data('daily_log.csv')
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Applications",
            len(apps_df),
            f"Goal: 40"
        )
    
    with col2:
        st.metric(
            "Interviews",
            len(interviews_df),
            f"Goal: 3"
        )
    
    with col3:
        if not daily_df.empty:
            total_hours = daily_df['hours_focused'].sum()
            st.metric(
                "Hours Focused",
                f"{total_hours:.0f}h",
                "This month"
            )
        else:
            st.metric("Hours Focused", "0h")
    
    with col4:
        if not apps_df.empty:
            response_rate = len(apps_df[apps_df['status'] != 'Applied']) / len(apps_df) * 100
            st.metric(
                "Response Rate",
                f"{response_rate:.0f}%",
                f"{len(apps_df[apps_df['status'] != 'Applied'])} responses"
            )
        else:
            st.metric("Response Rate", "0%")
    
    st.divider()
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Application Progress")
        if not apps_df.empty:
            apps_df['date'] = pd.to_datetime(apps_df['date'])
            apps_by_date = apps_df.groupby(apps_df['date'].dt.date).size().reset_index()
            apps_by_date.columns = ['date', 'count']
            apps_by_date['cumulative'] = apps_by_date['count'].cumsum()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=apps_by_date['date'],
                y=apps_by_date['cumulative'],
                mode='lines+markers',
                name='Applications',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            fig.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="Month 1 Goal")
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="",
                yaxis_title="Total Applications",
                showlegend=False,
                plot_bgcolor='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No applications yet. Add your first one!")
    
    with col2:
        st.subheader("📊 Application Status")
        if not apps_df.empty:
            status_counts = apps_df['status'].value_counts()
            colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
            
            fig = go.Figure(data=[go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                hole=.4,
                marker=dict(colors=colors)
            )])
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No status data yet")
    
    st.divider()
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Recent Applications")
        if not apps_df.empty:
            recent_apps = apps_df.tail(5).sort_values('date', ascending=False)
            for _, row in recent_apps.iterrows():
                status_color = {
                    'Applied': '🔵',
                    'Interview': '🟢',
                    'Rejected': '🔴',
                    'Offer': '🟡'
                }.get(row['status'], '⚪')
                
                st.markdown(f"""
                <div style='background: white; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #667eea;'>
                    <div style='font-weight: 600; font-size: 16px;'>{row['company']}</div>
                    <div style='color: #666; font-size: 14px;'>{row['role']}</div>
                    <div style='color: #999; font-size: 12px; margin-top: 5px;'>{status_color} {row['status']} • {row['date']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No applications yet")
    
    with col2:
        st.subheader("📚 Learning Progress")
        learning_plan = data.load_json('learning_plan.json')
        
        for tier, skills in learning_plan.items():
            completed = sum(1 for v in skills.values() if v)
            total = len(skills)
            percentage = (completed / total * 100) if total > 0 else 0
            
            tier_name = tier.replace('_', ' ').title()
            st.markdown(f"**{tier_name}**")
            st.progress(percentage / 100)
            st.caption(f"{completed}/{total} completed ({percentage:.0f}%)")

elif page == "➕ Add Application":
    st.title("Add New Application")
    
    with st.form("add_application"):
        col1, col2 = st.columns(2)
        
        with col1:
            company = st.text_input("Company Name*", placeholder="e.g., JLL")
            role = st.text_input("Role Title*", placeholder="e.g., Product Specialist - AI")
            url = st.text_input("Job URL", placeholder="https://...")
        
        with col2:
            status = st.selectbox("Status", ["Applied", "Interview", "Rejected", "Offer", "Accepted"])
            date = st.date_input("Application Date", datetime.now())
            notes = st.text_area("Notes", placeholder="Any additional details...")
        
        submitted = st.form_submit_button("Add Application", use_container_width=True)
        
        if submitted:
            if company and role:
                apps_df = data.load_data('applications.csv')
                new_row = pd.DataFrame([{
                    'date': date.strftime('%Y-%m-%d'),
                    'company': company,
                    'role': role,
                    'status': status,
                    'url': url,
                    'notes': notes
                }])
                apps_df = pd.concat([apps_df, new_row], ignore_index=True)
                data.save_data('applications.csv', apps_df)
                st.success(f"✅ Added application: {company} - {role}")
                st.balloons()
            else:
                st.error("Please fill in Company Name and Role Title")

elif page == "📚 Learning":
    st.title("Learning Tracker")
    
    tabs = st.tabs(["📖 Learning Plan", "➕ Log Learning", "📊 Progress"])
    
    with tabs[0]:
        learning_plan = data.load_json('learning_plan.json')
        
        st.subheader("🎯 30-Day Learning Plan")
        
        for tier, skills in learning_plan.items():
            with st.expander(f"{tier.replace('_', ' ').title()} - {sum(1 for v in skills.values() if v)}/{len(skills)} completed"):
                for skill, completed in skills.items():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"{'✅' if completed else '⬜'} {skill.replace('_', ' ')}")
                    with col2:
                        if not completed:
                            if st.button("Complete", key=f"{tier}_{skill}"):
                                learning_plan[tier][skill] = True
                                with open(os.path.join(data.data_dir, 'learning_plan.json'), 'w') as f:
                                    json.dump(learning_plan, f, indent=2)
                                st.rerun()
    
    with tabs[1]:
        st.subheader("Log Learning Activity")
        
        with st.form("log_learning"):
            tool = st.text_input("What did you practice?", placeholder="e.g., ChatGPT, SQL, Notion")
            minutes = st.number_input("Time spent (minutes)", min_value=1, value=30)
            notes = st.text_area("Notes", placeholder="What did you learn?")
            
            submitted = st.form_submit_button("Log Learning")
            
            if submitted and tool:
                learning_df = data.load_data('learning_log.csv')
                new_row = pd.DataFrame([{
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'tool_practiced': tool,
                    'time_spent': minutes,
                    'completed': True,
                    'notes': notes
                }])
                learning_df = pd.concat([learning_df, new_row], ignore_index=True)
                data.save_data('learning_log.csv', learning_df)
                st.success(f"✅ Logged: {tool} - {minutes} minutes")
    
    with tabs[2]:
        st.subheader("Learning Activity")
        learning_df = data.load_data('learning_log.csv')
        
        if not learning_df.empty:
            learning_df['date'] = pd.to_datetime(learning_df['date'])
            learning_by_date = learning_df.groupby(learning_df['date'].dt.date)['time_spent'].sum().reset_index()
            
            fig = px.bar(
                learning_by_date,
                x='date',
                y='time_spent',
                title="Daily Learning Time (minutes)",
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Recent Activities")
            recent = learning_df.tail(10).sort_values('date', ascending=False)
            for _, row in recent.iterrows():
                st.markdown(f"**{row['tool_practiced']}** - {row['time_spent']} min • {row['date']}")
        else:
            st.info("No learning activities logged yet")

elif page == "🎯 Goals":
    st.title("Monthly Goals")
    
    goals = data.load_json('goals.json')
    apps_df = data.load_data('applications.csv')
    interviews_df = data.load_data('interviews.csv')
    daily_df = data.load_data('daily_log.csv')
    
    # Month 1 Goals
    st.subheader("📅 Month 1 Goals")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        target = goals['month_1']['applications']
        current = len(apps_df)
        progress = min(current / target * 100, 100)
        st.metric("Applications", f"{current}/{target}", f"{progress:.0f}%")
        st.progress(progress / 100)
    
    with col2:
        target = goals['month_1']['interviews']
        current = len(interviews_df)
        progress = min(current / target * 100, 100)
        st.metric("Interviews", f"{current}/{target}", f"{progress:.0f}%")
        st.progress(progress / 100)
    
    with col3:
        target = goals['month_1']['posts']
        current = daily_df['posts_made'].sum() if not daily_df.empty else 0
        progress = min(current / target * 100, 100)
        st.metric("Posts/Content", f"{int(current)}/{target}", f"{progress:.0f}%")
        st.progress(progress / 100)

elif page == "📈 Analytics":
    st.title("Analytics & Insights")
    
    apps_df = data.load_data('applications.csv')
    daily_df = data.load_data('daily_log.csv')
    
    if not apps_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Applications by Company")
            top_companies = apps_df['company'].value_counts().head(10)
            fig = px.bar(
                x=top_companies.values,
                y=top_companies.index,
                orientation='h',
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(height=400, showlegend=False, xaxis_title="Applications", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Daily Productivity")
            if not daily_df.empty:
                daily_df['date'] = pd.to_datetime(daily_df['date'])
                fig = px.line(
                    daily_df,
                    x='date',
                    y='hours_focused',
                    markers=True,
                    color_discrete_sequence=['#764ba2']
                )
                fig.update_layout(height=400, xaxis_title="", yaxis_title="Hours")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No productivity data yet")
    else:
        st.info("Add applications to see analytics")

# Footer
st.divider()
st.caption("Career Dashboard v1.0 | Built for Nafisa Anjum | Last updated: " + datetime.now().strftime('%Y-%m-%d'))