import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

#Page configuration
st.set_page_config(
    page_title="Financial Budget Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Custom CSS
st.markdown("""
<style>

/*MAIN APP*/
.stApp{
    background-color:#0E1117;
}

/*GLOBAL TEXT*/
html,
body,
p,
span,
label,
h1,
h2,
h3,
h4,
h5,
h6{

    color:white !important;
}

/*HEADER*/
.main-header{

    background:linear-gradient(
        90deg,
        #00D4FF,
        #7C3AED
    );
    color:white !important;
    padding:20px;
    border-radius:20px;
    text-align:center;
    font-size:40px;
    font-weight:bold;
    box-shadow:
    0px 8px 20px rgba(
        0,
        212,
        255,
        0.3
    );
}

/*PREMIUM SIDEBAR*/
section[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #0F172A,
        #111827,
        #1E293B
    );

    border-right: 2px solid rgba(
        0,
        212,
        255,
        0.15
    );
}

/* FILTER PANEL HEADER */
.filter-title{
    background: linear-gradient(
        90deg,
        #00D4FF,
        #7C3AED
    );

    color: white;
    padding: 18px;
    border-radius: 18px; 
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 25px;
    box-shadow:
    0px 8px 25px rgba(
        0,
        212,
        255,
        0.35
    );
}

/* LABELS */
section[data-testid="stSidebar"] label{
    color: #E2E8F0 !important;
    font-size: 17px !important;
    font-weight: 600 !important;
}

/* SELECT BOX */
div[data-baseweb="select"]{
    background:#111827 !important;
    border:2px solid #38BDF8 !important;
    border-radius:14px !important;

    box-shadow:
    0 0 10px rgba(
        56,
        189,
        248,
        0.20
    );

    transition:all 0.3s ease;
}

/* DROPDOWN */
div[data-baseweb="popover"]{
    background: #111827 !important;
}

/* HOVER */
div[data-baseweb="select"]:hover{

    border:2px solid #60A5FA !important;
    box-shadow:
    0 0 15px rgba(
        96,
        165,
        250,
        0.50
    );

    transform:translateY(-2px);
}


/* Hide Sidebar Scrollbar */
section[data-testid="stSidebar"]::-webkit-scrollbar {
    display: none;
}

section[data-testid="stSidebar"] {
    scrollbar-width: none;
    -ms-overflow-style: none;
}

/*KPI CARDS*/
div[data-testid="metric-container"]{
    background: linear-gradient(
        135deg,
        #2563EB,
        #1D4ED8
    );

    border: 1px solid rgba(
        255,
        255,
        255,
        0.15
    );

    border-radius: 20px;
    padding: 25px;
    min-height: 150px;
    box-shadow:
    0px 8px 25px rgba(
        37,
        99,
        235,
        0.40
    );

    transition: all 0.3s ease;
}

/* Hover Effect */
div[data-testid="metric-container"]:hover{

    transform: translateY(-6px);
    box-shadow:
    0px 12px 30px rgba(
        37,
        99,
        235,
        0.60
    );
}

/* KPI Label */
div[data-testid="metric-container"] label{
    color: #E2E8F0 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* KPI Value */
div[data-testid="metric-container"] [data-testid="stMetricValue"]{
    color: white !important;
    font-size: 34px !important;
    font-weight: bold !important;
}

/* KPI Delta */
div[data-testid="metric-container"] [data-testid="stMetricDelta"]{
    color: #BBF7D0 !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

/*CHART CONTAINERS*/
[data-testid="stPlotlyChart"]{
    background:#161B22;
    border:1px solid #2D3748;
    border-radius:15px;
    padding:10px;
}

/*DATAFRAME*/
[data-testid="stDataFrame"]{
    border:1px solid #2D3748;
    border-radius:15px;
    overflow:hidden;
}

/*BUTTONS*/
.stButton > button{
    background:#00D4FF;
    color:black;
    border:none;
    border-radius:10px;
    font-weight:bold;
}

.stButton > button:hover{
    background:#00B8E6;
}

/*DOWNLOAD BUTTON*/
.stDownloadButton > button{
    width:100%;
    background: linear-gradient(90deg, #00D4FF, #7C3AED);
    color:black;
    border:none;
    border-radius:10px;
    font-weight:bold;
    padding:12px;
}

.stDownloadButton > button:hover{
    background:#00B8E6;
}

/*FILTERS*/
div[data-baseweb="select"]{
    background:#161B22 !important;
    color:white !important;
}

/*ALERT BOXES*/
[data-testid="stAlert"]{
    border-radius:15px;
}

/*DIVIDER*/
hr{
    border:1px solid #2D3748;
}

/*SCROLLBAR*/
::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-track{
    background:#161B22;
}

::-webkit-scrollbar-thumb{
    background:#00D4FF;
    border-radius:10px;
}


/*FIX SIDEBAR TOGGLE ARROW*/
/* Stable sidebar toggle button */
[data-testid="collapsedControl"] {
    position: fixed !important;
    top: 10px !important;
    left: 10px !important;
    z-index: 999999 !important;
}

/*REMOVE OUTER CHART BOX*/
[data-testid="stPlotlyChart"] {
    background: transparent !important;
    border: none !important;
    padding: 0px !important;
    box-shadow: none !important;
}

/* Plotly inner frame remove */
.js-plotly-plot {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Extra wrapper clean */
.element-container {
    border: none !important;
    box-shadow: none !important;
}

/* Remove white border feel */
.plot-container {
    border: none !important;
    box-shadow: none !important;
}

</style>
""", unsafe_allow_html=True)


# Load data
@st.cache_data
def load_data():
    return pd.read_csv(
        "Financial_Budgeting_Dataset.csv"
    )

df = load_data()


# Header
st.markdown(
"""
<div class="main-header">
📈 Financial Budget Allocation Dashboard
</div>
""",
unsafe_allow_html=True
)

st.markdown("")

st.markdown("<br>", unsafe_allow_html=True)


# Sidebar
st.sidebar.markdown("""
<div style="
background: linear-gradient(90deg, #00D4FF, #7C3AED);
padding:18px;
border-radius:18px;
text-align:center;
font-size:22px;
font-weight:bold;
color:white;
margin-bottom:25px;
border:none;
box-shadow:0px 0px 15px rgba(56,189,248,0.25);
">
🎛️ Filter Panel
</div>
""", unsafe_allow_html=True)

quarter = st.sidebar.selectbox(
    "📅 Fiscal Quarter",
    ["All"] + sorted(df["Fiscal_Quarter"].unique())
)

department = st.sidebar.selectbox(
    "🏢 Department",
    ["All"] + sorted(df["Department"].unique())
)

expense = st.sidebar.selectbox(
    "💳 Expense Category",
    ["All"] + sorted(df["Expense_Category"].unique())
)

status = st.sidebar.selectbox(
    "📊 Budget Status",
    ["All"] + sorted(df["Budget_Status"].unique())
)


# Filter data
filtered_df = df.copy()

if quarter != "All":
    filtered_df = filtered_df[
        filtered_df["Fiscal_Quarter"] == quarter
    ]

if department != "All":
    filtered_df = filtered_df[
        filtered_df["Department"] == department
    ]

if expense != "All":
    filtered_df = filtered_df[
        filtered_df["Expense_Category"] == expense
    ]

if status != "All":
    filtered_df = filtered_df[
        filtered_df["Budget_Status"] == status
    ]



# KPI Calculations
total_budget = filtered_df[
    "Budget_Allocated"
].sum()

utilized_budget = filtered_df[
    "Budget_Utilized"
].sum()

revenue = filtered_df[
    "Actual_Revenue"
].sum()

efficiency = filtered_df[
    "Allocation_Efficiency"
].mean()

remaining_budget = (
    total_budget -
    utilized_budget
)

utilization_rate = (
    utilized_budget /
    total_budget * 100
    if total_budget > 0
    else 0
)


# Premium KPI Cards
st.markdown("""
<div class="section-header">
<h2>📊 Financial Overview</h2>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)

card_style = """
background: linear-gradient(135deg, #38BDF8, #2563EB);
padding: 20px;
border-radius: 20px;
text-align: center;
box-shadow: 0px 8px 20px rgba(56,189,248,0.35);
height: 160px;
"""

# Card 1
with c1:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="color:white;font-size:20px;font-weight:600;">
            💰 Budget Allocated
        </div>
        <div style="color:white;font-size:25px;font-weight:bold;margin-top:15px;">
            ${total_budget/1000000:.1f}M
        </div>
    </div>
    """, unsafe_allow_html=True)

# Card 2
with c2:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="color:white;font-size:20px;font-weight:600;">
            📊 Budget Utilized
        </div>
        <div style="color:white;font-size:25px;font-weight:bold;margin-top:15px;">
            ${utilized_budget/1000000:.1f}M
        </div>
    </div>
    """, unsafe_allow_html=True)

# Card 3
with c3:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="color:white;font-size:20px;font-weight:600;">
            💵 Remaining Budget
        </div>
        <div style="color:white;font-size:25px;font-weight:bold;margin-top:15px;">
            ${remaining_budget/1000000:.1f}M
        </div>
    </div>
    """, unsafe_allow_html=True)

# Card 4
with c4:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="color:white;font-size:20px;font-weight:600;">
            📈 Revenue
        </div>
        <div style="color:white;font-size:25px;font-weight:bold;margin-top:15px;">
            ${revenue/1000000:.1f}M
        </div>
    </div>
    """, unsafe_allow_html=True)

# Card 5
with c5:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="color:white;font-size:20px;font-weight:600;">
            ⚡ Efficiency
        </div>
        <div style="color:white;font-size:25px;font-weight:bold;margin-top:15px;">
            {efficiency:.2f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# Data table
st.markdown(
    "## 📋 Filtered Financial Dataset",
    unsafe_allow_html=True
)

st.dataframe(
    filtered_df,
    width="stretch",
    height=500
)

st.markdown("---")


# Gauge and comparison
col1, col2 = st.columns(2, gap="large")
with col1:

    st.subheader("⚡ Budget Efficiency Score")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=efficiency,
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "limegreen"},
                "steps": [
                    {"range": [0, 50], "color": "#ef4444"},
                    {"range": [50, 80], "color": "#f59e0b"},
                    {"range": [80, 100], "color": "#22c55e"},
                ],
            },
        )
    )

    gauge.update_layout(
    height=420,
    margin=dict(t=30, b=20, l=20, r=20),
    paper_bgcolor="#0E1117",  
    plot_bgcolor="#0E1117",  
    font=dict(color="white")   
)

    st.plotly_chart(
        gauge,
        width="stretch"
    )

with col2:

    st.subheader("💰 Budget vs Revenue")

    comparison = pd.DataFrame({
        "Category": ["Budget Allocated", "Revenue"],
        "Value": [total_budget, revenue]
    })

    fig = px.bar(
        comparison,
        x="Category",
        y="Value",
        color="Category",
        text_auto=True
    )

    fig.update_layout(
    height=420,
    margin=dict(t=30, b=20, l=20, r=20),
    paper_bgcolor="#0E1117",  
    plot_bgcolor="#0E1117",   
    font=dict(color="white"), 
    showlegend=False
)

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.markdown("---")


# Sunburst and treemap
col3, col4 = st.columns(2, gap="large")
with col3:

    st.subheader("🌞 Budget Hierarchy")

    fig = px.sunburst(
        filtered_df,
        path=[
            "Department",
            "Expense_Category",
            "Budget_Status"
        ],
        values="Budget_Allocated",
        color="Allocation_Efficiency",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        height=650,
        margin=dict(t=30, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

with col4:

    st.subheader("🌳 Budget Treemap")

    fig = px.treemap(
        filtered_df,
        path=[
            "Department",
            "Expense_Category"
        ],
        values="Budget_Allocated",
        color="Budget_Variance",
        color_continuous_scale="RdYlGn"
    )

    fig.update_layout(
        height=650,
        margin=dict(t=30, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.markdown("---")


# Sankey diagram
st.subheader("🔄 Budget Flow Analysis")

sankey_data = (
    filtered_df
    .groupby(["Department", "Expense_Category"])["Budget_Allocated"]
    .sum()
    .reset_index()
)

labels = list(
    pd.concat([
        sankey_data["Department"],
        sankey_data["Expense_Category"]
    ]).unique()
)

source = [labels.index(i) for i in sankey_data["Department"]]
target = [labels.index(i) for i in sankey_data["Expense_Category"]]
value = sankey_data["Budget_Allocated"]

fig = go.Figure(
    data=[
        go.Sankey(
            node=dict(
                pad=20,
                thickness=20,
                label=labels
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            )
        )
    ]
)

fig.update_layout(
    height=700,
    margin=dict(t=30, b=20, l=20, r=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.markdown("---")



# Trend and pie chart
col5, col6 = st.columns(2, gap="large")

with col5:

    st.subheader("📈 Quarterly Budget Trend")

    trend = (
        filtered_df
        .groupby("Fiscal_Quarter")["Budget_Allocated"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend,
        x="Fiscal_Quarter",
        y="Budget_Allocated",
        markers=True
    )

    fig.update_layout(
        height=550,
        margin=dict(t=30, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


with col6:

    st.subheader("🥧 Budget Status Distribution")

    fig = px.pie(
        filtered_df,
        names="Budget_Status"
    )

    fig.update_layout(
        height=550,
        margin=dict(t=30, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.markdown("---")


# Heatmap and scatter
col7, col8 = st.columns(2, gap="large")

with col7:

    st.subheader("🔥 Department Expense Heatmap")

    heat = filtered_df.pivot_table(
        values="Budget_Allocated",
        index="Department",
        columns="Expense_Category",
        aggfunc="sum",
        fill_value=0
    )

    fig = px.imshow(
        heat,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        height=600,
        margin=dict(t=30, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


with col8:

    st.subheader("💹 Budget vs Utilization")

    fig = px.scatter(
        filtered_df,
        x="Budget_Allocated",
        y="Budget_Utilized",
        color="Department",
        size="Monthly_Expense",
        hover_data=["Expense_Category"]
    )

    fig.update_layout(
        height=600,
        margin=dict(t=30, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.markdown("---")

# Bar chart and top depatments
col9, col10 = st.columns(2, gap="large")


with col9:

    st.subheader("🏆 Department Budget Allocation")

    dept = (
        filtered_df
        .groupby("Department")["Budget_Allocated"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        dept,
        x="Department",
        y="Budget_Allocated",
        color="Budget_Allocated",
        text_auto=True
    )

    fig.update_layout(
        height=600,
        margin=dict(t=30, b=20, l=20, r=20),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


with col10:

    st.subheader("🥇 Top Departments")

    top_dept = (
        filtered_df
        .groupby("Department")["Actual_Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Actual_Revenue", ascending=False)
        .head(5)
    )

    st.dataframe(
        top_dept,
        width="stretch",
        height=210   # 🔥 reduced height (important)
    )

    # Download center
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📥 Download Center")
    
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Financial Dataset",
        data=csv,
        file_name="financial_budget_data.csv",
        mime="text/csv",
        width="stretch"
    )




#Key insights
if not filtered_df.empty:

    highest_budget_department = (
        filtered_df
        .groupby("Department")
        ["Budget_Allocated"]
        .sum()
        .idxmax()
    )

    highest_revenue_department = (
        filtered_df
        .groupby("Department")
        ["Actual_Revenue"]
        .sum()
        .idxmax()
    )

else:

    highest_budget_department = "No Data"

    highest_revenue_department = "No Data"


st.subheader("📌 Key Dashboard Insights")

st.markdown(f"""
<div style="
background: linear-gradient(90deg, #00D4FF, #7C3AED);
padding: 25px;
border-radius: 18px;
color: white;
box-shadow: 0px 8px 25px rgba(0, 212, 255, 0.25);
font-size: 23px;
line-height: 1.7;
">

<b>✅ Total Budget Allocated:</b> ${total_budget:,.0f}

<b>💰 Total Revenue Generated:</b> ${revenue:,.0f}

<b>📈 Budget Utilization Rate:</b> {utilization_rate:.2f}%

<b>⚡ Allocation Efficiency:</b> {efficiency:.2f}%

<b>🏆 Highest Budget Department:</b> {highest_budget_department}

<b>🥇 Highest Revenue Department:</b> {highest_revenue_department}


</div>
""", unsafe_allow_html=True)

st.markdown("---")

#Dashboard Summary
st.subheader("🎯 Executive Summary")

st.markdown(
f"""
<div style="
background:linear-gradient(
90deg,
#0ea5e9,
#6366f1
);
padding:25px;
border-radius:20px;
color:white;
font-size: 23px;
">

<h3>Financial Performance Summary</h3>

<p>
This dashboard provides a comprehensive view of
financial budget allocation, utilization,
revenue generation and departmental performance.
Current analysis includes
<b>{len(filtered_df)}</b> records,
covering
<b>{filtered_df['Department'].nunique()}</b>
departments and
<b>{filtered_df['Expense_Category'].nunique()}</b>
expense categories.
The organization has allocated
<b>${total_budget:,.0f}</b>
with an overall utilization rate of
<b>{utilization_rate:.2f}%</b>.

</p>

</div>
""",
unsafe_allow_html=True
)

st.markdown("---")