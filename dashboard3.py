import dash
from dash import dcc, html, Input, Output, dash_table, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data with new structure
def load_data():
    try:
        # Read Excel file
        df = pd.read_excel('tcas_data.xlsx', sheet_name='ข้อมูลหลักสูตร')
        
        # Clean data
        df = df.dropna(subset=['มหาวิทยาลัย', 'ค่าเทอม/เทอม'])
        
        # Determine university type
        private_keywords = ['รามคำแหง', 'สยาม', 'รังสิต', 'เกษมบัณฑิต', 'กรุงเทพ', 
                          'หอการค้าไทย', 'ธุรกิจบัณฑิต', 'ปัญญาภิวัฒน์', 'เทคโนโลยีมหานคร']
        
        df['university_type'] = df['มหาวิทยาลัย'].apply(
            lambda x: 'เอกชน' if any(keyword in str(x) for keyword in private_keywords) else 'รัฐ'
        )
        
        # Clean course names
        df['course_short'] = df['หลักสูตร'].apply(
            lambda x: str(x)[:60] + "..." if len(str(x)) > 60 else str(x)
        )
        
        # Translate payment methods for display
        df['payment_method_en'] = df['รูปแบบการชำระ'].map({
            'ต่อภาคการศึกษา': 'Per Semester',
            'ตลอดหลักสูตร': 'Total Program'
        })
        
        # Use appropriate tuition column based on payment method
        df['main_tuition'] = df.apply(
            lambda row: row['ค่าเทอม/เทอม'] if row['รูปแบบการชำระ'] == 'ต่อภาคการศึกษา' else row['ค่าเทอมจากเว็บ'],
            axis=1
        )
        
        # Calculate 4-year cost
        df['four_year_cost'] = df.apply(
            lambda row: row['ค่าเทอม/เทอม'] * 8 if row['รูปแบบการชำระ'] == 'ต่อภาคการศึกษา' else row['ค่าเทอมจากเว็บ'],
            axis=1
        )
        
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "TCAS Computer Engineering Dashboard"

# Enhanced CSS styling for multi-page
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #1f2937;
                line-height: 1.6;
                min-height: 100vh;
            }
            
            .app-container {
                min-height: 100vh;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            }
            
            .navbar {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                position: sticky;
                top: 0;
                z-index: 1000;
                border-bottom: 1px solid rgba(102, 126, 234, 0.2);
            }
            
            .navbar-content {
                max-width: 1400px;
                margin: 0 auto;
                padding: 1rem 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .logo {
                font-size: 1.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .nav-links {
                display: flex;
                gap: 0.5rem;
            }
            
            .nav-link {
                padding: 0.75rem 1.5rem;
                border-radius: 25px;
                text-decoration: none;
                font-weight: 600;
                color: #6b7280;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            
            .nav-link:hover {
                color: #667eea;
                background: rgba(102, 126, 234, 0.1);
                border-color: rgba(102, 126, 234, 0.2);
                transform: translateY(-2px);
            }
            
            .nav-link.active {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            .page-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 2rem;
            }
            
            .hero-section {
                text-align: center;
                padding: 3rem 0;
                margin-bottom: 3rem;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 24px;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .hero-title {
                font-size: 3.5rem;
                font-weight: 900;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 1rem;
                line-height: 1.2;
            }
            
            .hero-subtitle {
                font-size: 1.25rem;
                color: #6b7280;
                max-width: 600px;
                margin: 0 auto;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
                margin-bottom: 3rem;
            }
            
            .stat-card {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(20px);
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .stat-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            .stat-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
            }
            
            .stat-number {
                font-size: 2.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 0.5rem;
            }
            
            .stat-label {
                color: #6b7280;
                font-size: 0.95rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .content-grid {
                display: grid;
                grid-template-columns: 350px 1fr;
                gap: 2rem;
                margin-bottom: 3rem;
            }
            
            .sidebar {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(20px);
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                height: fit-content;
                position: sticky;
                top: 120px;
            }
            
            .sidebar-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: #374151;
                margin-bottom: 1.5rem;
                padding-bottom: 0.75rem;
                border-bottom: 2px solid #e5e7eb;
            }
            
            .content-area {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(20px);
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .chart-card {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .filter-group {
                margin-bottom: 2rem;
            }
            
            .filter-label {
                font-weight: 700;
                color: #374151;
                margin-bottom: 0.75rem;
                display: block;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            /* Enhanced form controls */
            .Select-control {
                border: 2px solid #e5e7eb;
                border-radius: 12px;
                min-height: 48px;
                background: rgba(255, 255, 255, 0.8);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }
            
            .Select-control:hover {
                border-color: #667eea;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
            }
            
            .Select--is-focused .Select-control {
                border-color: #667eea;
                box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
            }
            
            /* Custom input styling */
            input[type="text"] {
                border: 2px solid #e5e7eb !important;
                border-radius: 12px !important;
                padding: 12px 16px !important;
                background: rgba(255, 255, 255, 0.8) !important;
                backdrop-filter: blur(10px) !important;
                transition: all 0.3s ease !important;
                font-weight: 500 !important;
            }
            
            input[type="text"]:focus {
                border-color: #667eea !important;
                box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
                outline: none !important;
            }
            
            /* Table styling */
            .dash-table-container {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            /* Responsive design */
            @media (max-width: 1024px) {
                .content-grid {
                    grid-template-columns: 1fr;
                }
                
                .sidebar {
                    position: static;
                }
                
                .page-container {
                    padding: 1rem;
                }
                
                .hero-title {
                    font-size: 2.5rem;
                }
                
                .stats-grid {
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 1rem;
                }
            }
            
            @media (max-width: 768px) {
                .navbar-content {
                    flex-direction: column;
                    gap: 1rem;
                    padding: 1rem;
                }
                
                .nav-links {
                    flex-wrap: wrap;
                    justify-content: center;
                }
                
                .hero-title {
                    font-size: 2rem;
                }
                
                .stats-grid {
                    grid-template-columns: 1fr;
                }
            }
            
            /* Animation keyframes */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .fade-in-up {
                animation: fadeInUp 0.6s ease-out;
            }
            
            /* Loading animation */
            .loading {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 200px;
                font-size: 1.1rem;
                color: #6b7280;
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #f1f5f9;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
            }
        </style>
    </head>
    <body>
        <div class="app-container">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Navigation component
def create_navbar():
    return html.Div([
        html.Div([
            html.Div("🎓 TCAS Engineering Dashboard", className="logo"),
            html.Div([
                dcc.Link("Home", href="/", className="nav-link"),
                dcc.Link("Compare", href="/compare", className="nav-link"),
                dcc.Link("Analytics", href="/analytics", className="nav-link"),
                dcc.Link("Data", href="/data", className="nav-link"),
            ], className="nav-links")
        ], className="navbar-content")
    ], className="navbar")

# Home page layout
def create_home_page():
    # Calculate statistics
    total_programs = len(df)
    avg_price_semester = int(df[df['รูปแบบการชำระ'] == 'ต่อภาคการศึกษา']['ค่าเทอม/เทอม'].mean()) if len(df[df['รูปแบบการชำระ'] == 'ต่อภาคการศึกษา']) > 0 else 0
    avg_price_total = int(df[df['รูปแบบการชำระ'] == 'ตลอดหลักสูตร']['ค่าเทอมจากเว็บ'].mean()) if len(df[df['รูปแบบการชำระ'] == 'ตลอดหลักสูตร']) > 0 else 0
    cheapest_program = int(df['main_tuition'].min())
    
    return html.Div([
        # Hero Section
        html.Div([
            html.H1("Computer/AI Engineering Programs in Thailand", className="hero-title"),
            html.P("Compare tuition fees and program details from universities across the country", className="hero-subtitle")
        ], className="hero-section fade-in-up"),
        
        # Statistics Cards
        html.Div([
            html.Div([
                html.Div(f"{total_programs}", className="stat-number"),
                html.Div("Total Programs", className="stat-label")
            ], className="stat-card fade-in-up"),
            
            html.Div([
                html.Div(f"{avg_price_semester:,}", className="stat-number"),
                html.Div("Avg Per Semester (THB)", className="stat-label")
            ], className="stat-card fade-in-up"),
            
            html.Div([
                html.Div(f"{avg_price_total:,}", className="stat-number"),
                html.Div("Avg Total Program (THB)", className="stat-label")
            ], className="stat-card fade-in-up"),
            
            html.Div([
                html.Div(f"{cheapest_program:,}", className="stat-number"),
                html.Div("Lowest Tuition (THB)", className="stat-label")
            ], className="stat-card fade-in-up"),
        ], className="stats-grid"),
        
        # Quick Overview Chart
        html.Div([
            html.H3("📊 Tuition Overview by University Type", style={'margin-bottom': '1.5rem', 'color': '#374151'}),
            dcc.Graph(
                figure=create_overview_chart(),
                config={'displayModeBar': False}
            )
        ], className="chart-card fade-in-up"),
        
        # Quick Actions
        html.Div([
            html.H3("🚀 Getting Started", style={'margin-bottom': '1.5rem', 'color': '#374151', 'text-align': 'center'}),
            html.Div([
                html.Div([
                    html.H4("🔍 Compare Programs"),
                    html.P("Compare tuition fees and program details"),
                    dcc.Link(html.Button("Start Comparing", style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 'color': 'white', 'border': 'none', 'padding': '12px 24px', 'border-radius': '25px', 'font-weight': '600', 'cursor': 'pointer'}), href="/compare")
                ], style={'background': 'rgba(255,255,255,0.8)', 'padding': '2rem', 'border-radius': '16px', 'text-align': 'center', 'backdrop-filter': 'blur(10px)'}),
                
                html.Div([
                    html.H4("📈 View Analytics"),
                    html.P("See detailed statistics and trends"),
                    dcc.Link(html.Button("View Analytics", style={'background': 'linear-gradient(135deg, #10b981 0%, #059669 100%)', 'color': 'white', 'border': 'none', 'padding': '12px 24px', 'border-radius': '25px', 'font-weight': '600', 'cursor': 'pointer'}), href="/analytics")
                ], style={'background': 'rgba(255,255,255,0.8)', 'padding': '2rem', 'border-radius': '16px', 'text-align': 'center', 'backdrop-filter': 'blur(10px)'}),
                
                html.Div([
                    html.H4("📋 Browse All Data"),
                    html.P("Complete data table with all programs"),
                    dcc.Link(html.Button("Browse Data", style={'background': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', 'color': 'white', 'border': 'none', 'padding': '12px 24px', 'border-radius': '25px', 'font-weight': '600', 'cursor': 'pointer'}), href="/data")
                ], style={'background': 'rgba(255,255,255,0.8)', 'padding': '2rem', 'border-radius': '16px', 'text-align': 'center', 'backdrop-filter': 'blur(10px)'})
            ], style={'display': 'grid', 'grid-template-columns': 'repeat(auto-fit, minmax(250px, 1fr))', 'gap': '2rem'})
        ], className="chart-card fade-in-up")
    ], className="page-container")

def create_overview_chart():
    # Create overview chart
    overview_data = []
    for payment_type in df['payment_method_en'].unique():
        for uni_type in df['university_type'].unique():
            subset = df[(df['payment_method_en'] == payment_type) & (df['university_type'] == uni_type)]
            if not subset.empty:
                avg_price = subset['main_tuition'].mean()
                overview_data.append({
                    'Payment Method': payment_type,
                    'University Type': uni_type,
                    'Average Tuition': int(avg_price),
                    'Program Count': len(subset)
                })
    
    overview_df = pd.DataFrame(overview_data)
    
    fig = px.bar(
        overview_df,
        x='Payment Method',
        y='Average Tuition',
        color='University Type',
        barmode='group',
        title="",
        labels={'Average Tuition': 'Average Tuition (THB)'},
        color_discrete_map={'รัฐ': '#3b82f6', 'เอกชน': '#ef4444'},
        text='Average Tuition'
    )
    
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(
        font_family="Inter",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

# Compare page layout
def create_compare_page():
    return html.Div([
        html.Div([
            html.H1("🔍 Compare Programs", className="hero-title"),
            html.P("Filter and compare programs based on your preferences", className="hero-subtitle")
        ], className="hero-section fade-in-up"),
        
        html.Div([
            # Sidebar with filters
            html.Div([
                html.H3("🎛️ Filter Controls", className="sidebar-title"),
                
                # Payment method filter
                html.Div([
                    html.Label("Payment Method", className="filter-label"),
                    dcc.Dropdown(
                        id='compare-payment-method',
                        options=[
                            {'label': 'All', 'value': 'All'},
                            {'label': 'Per Semester', 'value': 'Per Semester'},
                            {'label': 'Total Program', 'value': 'Total Program'}
                        ],
                        value='All',
                        clearable=False
                    )
                ], className="filter-group"),
                
                # University type filter
                html.Div([
                    html.Label("University Type", className="filter-label"),
                    dcc.Dropdown(
                        id='compare-university-type',
                        options=[
                            {'label': 'รัฐ', 'value': 'รัฐ'},
                            {'label': 'เอกชน', 'value': 'เอกชน'}
                        ],
                        value=['รัฐ', 'เอกชน'],
                        multi=True,
                        clearable=False
                    )
                ], className="filter-group"),
                
                # Price range filter
                html.Div([
                    html.Label("Price Range (THB)", className="filter-label"),
                    dcc.RangeSlider(
                        id='compare-price-range',
                        min=int(df['main_tuition'].min()),
                        max=int(df['main_tuition'].max()),
                        value=[int(df['main_tuition'].min()), int(df['main_tuition'].max())],
                        marks={
                            int(df['main_tuition'].min()): f'{int(df["main_tuition"].min()):,}',
                            int(df['main_tuition'].max()): f'{int(df["main_tuition"].max()):,}'
                        },
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], className="filter-group"),
                
                # Search
                html.Div([
                    html.Label("Search University", className="filter-label"),
                    dcc.Input(
                        id='compare-search',
                        type='text',
                        placeholder='เช่น: ธรรมศาสตร์, นานาชาติ',
                        style={'width': '100%'}
                    )
                ], className="filter-group"),
                
                # Statistics display
                html.Div(id="compare-stats", className="filter-group")
                
            ], className="sidebar"),
            
            # Main content
            html.Div([
                html.Div(id="compare-chart", className="chart-card"),
                
                # Calculator section
                html.Div([
                    html.H3("🧮 Cost Calculator", style={'margin-bottom': '1.5rem', 'color': '#374151'}),
                    html.Div([
                        html.Label("Select universities to compare (max 3)", style={'font-weight': '600', 'margin-bottom': '1rem', 'display': 'block'}),
                        dcc.Dropdown(
                            id='calculator-dropdown',
                            options=[{'label': uni, 'value': uni} for uni in df['มหาวิทยาลัย'].unique()],
                            value=df.nsmallest(3, 'main_tuition')['มหาวิทยาลัย'].tolist(),
                            multi=True
                        )
                    ], style={'margin-bottom': '1.5rem'}),
                    html.Div(id="calculator-chart")
                ], className="chart-card")
            ], className="content-area")
        ], className="content-grid")
    ], className="page-container")

# Analytics page layout
def create_analytics_page():
    return html.Div([
        html.Div([
            html.H1("📈 Data Analytics", className="hero-title"),
            html.P("In-depth statistics and trends analysis", className="hero-subtitle")
        ], className="hero-section fade-in-up"),
        
        # Analytics charts
        html.Div([
            html.Div([
                html.H3("📊 Tuition Distribution", style={'margin-bottom': '1.5rem', 'color': '#374151'}),
                dcc.Graph(
                    figure=create_distribution_chart(),
                    config={'displayModeBar': False}
                )
            ], className="chart-card fade-in-up"),
            
            html.Div([
                html.H3("🏛️ University Type Proportion", style={'margin-bottom': '1.5rem', 'color': '#374151'}),
                dcc.Graph(
                    figure=create_pie_chart(),
                    config={'displayModeBar': False}
                )
            ], className="chart-card fade-in-up"),
            
            html.Div([
                html.H3("💰 รัฐ vs เอกชน Comparison", style={'margin-bottom': '1.5rem', 'color': '#374151'}),
                dcc.Graph(
                    figure=create_comparison_chart(),
                    config={'displayModeBar': False}
                )
            ], className="chart-card fade-in-up"),
        ])
    ], className="page-container")

def create_distribution_chart():
    fig = px.histogram(
        df, 
        x='main_tuition', 
        nbins=20,
        title="",
        labels={'main_tuition': 'Tuition (THB)', 'count': 'Number of Programs'},
        color_discrete_sequence=['#667eea']
    )
    
    fig.update_layout(
        font_family="Inter",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig

def create_pie_chart():
    type_counts = df['university_type'].value_counts()
    
    fig = px.pie(
        values=type_counts.values,
        names=type_counts.index,
        title="",
        color_discrete_map={'รัฐ': '#3b82f6', 'เอกชน': '#ef4444'}
    )
    
    fig.update_layout(
        font_family="Inter",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig

def create_comparison_chart():
    comparison_data = []
    for payment_type in df['payment_method_en'].unique():
        for uni_type in df['university_type'].unique():
            subset = df[(df['payment_method_en'] == payment_type) & (df['university_type'] == uni_type)]
            if not subset.empty:
                comparison_data.append({
                    'Category': f"{uni_type} ({payment_type})",
                    'Minimum': int(subset['main_tuition'].min()),
                    'Maximum': int(subset['main_tuition'].max()),
                    'Average': int(subset['main_tuition'].mean())
                })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=comparison_df['Category'],
        y=comparison_df['Minimum'],
        name='Minimum',
        marker_color='#10b981'
    ))
    
    fig.add_trace(go.Bar(
        x=comparison_df['Category'],
        y=comparison_df['Average'],
        name='Average',
        marker_color='#667eea'
    ))
    
    fig.add_trace(go.Bar(
        x=comparison_df['Category'],
        y=comparison_df['Maximum'],
        name='Maximum',
        marker_color='#ef4444'
    ))
    
    fig.update_layout(
        barmode='group',
        font_family="Inter",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        xaxis_title="University Category",
        yaxis_title="Tuition (THB)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

# Data page layout
def create_data_page():
    return html.Div([
        html.Div([
            html.H1("📋 All Program Data", className="hero-title"),
            html.P("Complete data table with search and filter functionality", className="hero-subtitle")
        ], className="hero-section fade-in-up"),
        
        html.Div([
            create_data_table()
        ], className="dash-table-container fade-in-up")
    ], className="page-container")

def create_data_table():
    # Prepare table data
    table_df = df[['มหาวิทยาลัย', 'course_short', 'ค่าเทอม/เทอม', 'ค่าเทอมจากเว็บ', 'payment_method_en', 'university_type']].copy()
    table_df.columns = ['University', 'Program', 'Per Semester', 'Total Program', 'Payment Method', 'Type']
    table_df = table_df.sort_values('Per Semester')
    
    # Convert to int
    table_df['Per Semester'] = table_df['Per Semester'].astype(int)
    table_df['Total Program'] = table_df['Total Program'].astype(int)
    
    return dash_table.DataTable(
        data=table_df.to_dict('records'),
        columns=[
            {'name': 'University', 'id': 'University'},
            {'name': 'Program', 'id': 'Program'},
            {'name': 'Per Semester (THB)', 'id': 'Per Semester', 'type': 'numeric', 'format': {'specifier': ','}},
            {'name': 'Total Program (THB)', 'id': 'Total Program', 'type': 'numeric', 'format': {'specifier': ','}},
            {'name': 'Payment Method', 'id': 'Payment Method'},
            {'name': 'Type', 'id': 'Type'}
        ],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '16px',
            'fontFamily': 'Inter',
            'fontSize': '14px',
            'border': 'none',
            'backgroundColor': 'rgba(255, 255, 255, 0.8)'
        },
        style_header={
            'backgroundColor': 'rgba(102, 126, 234, 0.1)',
            'fontWeight': 'bold',
            'color': '#374151',
            'border': 'none',
            'fontSize': '13px',
            'textTransform': 'uppercase',
            'letterSpacing': '0.5px'
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{Type} = รัฐ'},
                'backgroundColor': 'rgba(59, 130, 246, 0.05)',
            },
            {
                'if': {'filter_query': '{Type} = เอกชน'},
                'backgroundColor': 'rgba(239, 68, 68, 0.05)',
            },
            {
                'if': {'state': 'selected'},
                'backgroundColor': 'rgba(102, 126, 234, 0.2)',
            }
        ],
        page_size=20,
        sort_action='native',
        filter_action='native',
        style_as_list_view=True
    )

# Main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    create_navbar(),
    html.Div(id='page-content')
])

# Page routing callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/compare':
        return create_compare_page()
    elif pathname == '/analytics':
        return create_analytics_page()
    elif pathname == '/data':
        return create_data_page()
    else:
        return create_home_page()

# Compare page callbacks
@app.callback(
    [Output('compare-stats', 'children'),
     Output('compare-chart', 'children')],
    [Input('compare-payment-method', 'value'),
     Input('compare-university-type', 'value'),
     Input('compare-price-range', 'value'),
     Input('compare-search', 'value')]
)
def update_compare_page(payment_method, university_types, price_range, search_term):
    # Filter data
    filtered_df = df.copy()
    
    if payment_method != 'All':
        filtered_df = filtered_df[filtered_df['payment_method_en'] == payment_method]
    
    filtered_df = filtered_df[filtered_df['university_type'].isin(university_types)]
    filtered_df = filtered_df[
        (filtered_df['main_tuition'] >= price_range[0]) & 
        (filtered_df['main_tuition'] <= price_range[1])
    ]
    
    if search_term:
        search_mask = filtered_df['มหาวิทยาลัย'].str.contains(search_term, case=False, na=False)
        filtered_df = filtered_df[search_mask]
    
    # Statistics
    total_programs = len(filtered_df)
    avg_price = int(filtered_df['main_tuition'].mean()) if total_programs > 0 else 0
    min_price = int(filtered_df['main_tuition'].min()) if total_programs > 0 else 0
    max_price = int(filtered_df['main_tuition'].max()) if total_programs > 0 else 0
    
    stats_content = html.Div([
        html.H4("📊 Filtered Statistics", style={'color': '#374151', 'margin-bottom': '1rem'}),
        html.P(f"Programs Found: {total_programs}", style={'margin': '0.5rem 0'}),
        html.P(f"Average Price: {avg_price:,} THB", style={'margin': '0.5rem 0'}),
        html.P(f"Lowest Price: {min_price:,} THB", style={'margin': '0.5rem 0'}),
        html.P(f"Highest Price: {max_price:,} THB", style={'margin': '0.5rem 0'}),
        html.P(f"รัฐ: {len(filtered_df[filtered_df['university_type'] == 'รัฐ'])} programs", style={'margin': '0.5rem 0'}),
        html.P(f"เอกชน: {len(filtered_df[filtered_df['university_type'] == 'เอกชน'])} programs", style={'margin': '0.5rem 0'})
    ], style={'background': 'rgba(102, 126, 234, 0.1)', 'padding': '1rem', 'border-radius': '12px'})
    
    # Chart
    if filtered_df.empty:
        chart_content = html.Div([
            html.H3("No data found matching the filter criteria", style={'text-align': 'center', 'color': '#6b7280', 'margin': '2rem 0'})
        ])
    else:
        filtered_df = filtered_df.sort_values('main_tuition')
        
        fig = px.bar(
            filtered_df.head(20),  # Show top 20 to avoid overcrowding
            x='main_tuition',
            y='มหาวิทยาลัย',
            color='university_type',
            orientation='h',
            title=f"Tuition Fees - {payment_method}" if payment_method != 'All' else "Filtered Program Tuition Fees (Top 20)",
            labels={'main_tuition': 'Tuition (THB)', 'มหาวิทยาลัย': ''},
            color_discrete_map={'รัฐ': '#3b82f6', 'เอกชน': '#ef4444'},
            height=max(500, len(filtered_df.head(20)) * 30)
        )
        
        fig.update_layout(
            font_family="Inter",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=18,
            title_font_color='#374151',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        chart_content = dcc.Graph(figure=fig, config={'displayModeBar': False})
    
    return stats_content, chart_content

# Calculator callback
@app.callback(
    Output('calculator-chart', 'children'),
    [Input('calculator-dropdown', 'value')]
)
def update_calculator(selected_universities):
    if not selected_universities:
        return html.Div([
            html.P("Please select universities to compare", style={'text-align': 'center', 'color': '#6b7280', 'margin': '2rem 0'})
        ])
    
    # Limit to 3 universities
    selected_universities = selected_universities[:3]
    
    comparison_df = df[df['มหาวิทยาลัย'].isin(selected_universities)]
    
    # Create comparison data
    comparison_data = []
    for _, row in comparison_df.iterrows():
        uni_name = str(row['มหาวิทยาลัย'])
        semester_fee = int(row['ค่าเทอม/เทอม'])
        total_fee = int(row['ค่าเทอมจากเว็บ'])
        
        if row['รูปแบบการชำระ'] == 'ต่อภาคการศึกษา':
            comparison_data.append({
                'University': uni_name,
                'Category': 'Per Semester',
                'Amount': semester_fee
            })
            comparison_data.append({
                'University': uni_name,
                'Category': '4 Years Total',
                'Amount': semester_fee * 8
            })
        else:
            comparison_data.append({
                'University': uni_name,
                'Category': 'Total Program',
                'Amount': total_fee
            })
    
    comparison_df_chart = pd.DataFrame(comparison_data)
    
    fig = px.bar(
        comparison_df_chart,
        x='University',
        y='Amount',
        color='Category',
        barmode='group',
        title="Cost Comparison",
        labels={'Amount': 'Tuition (THB)'},
        text='Amount'
    )
    
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(
        font_family="Inter",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
        title_font_size=16,
        title_font_color='#374151'
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

# Add active link styling callback
@app.callback(
    Output('url', 'href'),
    [Input('url', 'pathname')]
)
def update_nav_links(pathname):
    return pathname

if __name__ == '__main__':
    print(f"📊 Loading dashboard with {len(df)} programs...")
    print("🚀 Starting Modern Multi-page Dashboard...")
    print("📱 Open http://127.0.0.1:8050/ in your browser")
    app.run(debug=True, host='127.0.0.1', port=8050)