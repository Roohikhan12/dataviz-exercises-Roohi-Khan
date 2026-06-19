import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="🌍",
    layout="wide",
)

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\Mubeen Khan\OneDrive\Desktop\world Happiness\world_happiness_2023.csv")

df = load_data()

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("🌍 Dashboard Controls")
st.sidebar.markdown("---")

regions = ["All Regions"] + sorted(
    df["Regional indicator"].dropna().unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

min_score = float(df["Ladder score"].min())
max_score = float(df["Ladder score"].max())

score_range = st.sidebar.slider(
    "Happiness Score Range",
    min_score,
    max_score,
    (min_score, max_score)
)

# ----------------------------
# FILTERING
# ----------------------------
filtered_df = df.copy()

if selected_region != "All Regions":
    filtered_df = filtered_df[
        filtered_df["Regional indicator"] == selected_region
    ]

filtered_df = filtered_df[
    (filtered_df["Ladder score"] >= score_range[0]) &
    (filtered_df["Ladder score"] <= score_range[1])
]

# ----------------------------
# HEADER
# ----------------------------
st.title("🌍 World Happiness Report 2023 Dashboard")
st.markdown(
    "Comprehensive analytics dashboard for global happiness indicators."
)

st.markdown("---")

# ----------------------------
# KPI SECTION
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Countries",
    len(filtered_df)
)

col2.metric(
    "Average Happiness",
    round(filtered_df["Ladder score"].mean(), 2)
)

col3.metric(
    "Average GDP",
    round(filtered_df["Logged GDP per capita"].mean(), 2)
)

col4.metric(
    "Average Life Expectancy",
    round(filtered_df["Healthy life expectancy"].mean(), 2)
)

st.markdown("---")

# ----------------------------
# TOP ROW
# ----------------------------
left, right = st.columns([2, 1])

with left:

    top10 = filtered_df.sort_values(
        "Ladder score",
        ascending=False
    ).head(10)

    fig = px.bar(
        top10,
        x="Ladder score",
        y="Country name",
        orientation="h",
        title="Top 10 Happiest Countries",
        text="Ladder score"
    )

    fig.update_layout(
        height=500,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    region_counts = (
        filtered_df["Regional indicator"]
        .value_counts()
        .reset_index()
    )

    region_counts.columns = ["Region", "Count"]

    fig = px.pie(
        region_counts,
        names="Region",
        values="Count",
        title="Regional Distribution"
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# SECOND ROW
# ----------------------------
col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df,
        x="Logged GDP per capita",
        y="Ladder score",
        color="Regional indicator",
        size="Healthy life expectancy",
        hover_name="Country name",
        title="GDP vs Happiness"
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    corr_columns = [
        "Ladder score",
        "Logged GDP per capita",
        "Social support",
        "Healthy life expectancy",
        "Freedom to make life choices",
        "Generosity",
        "Perceptions of corruption"
    ]

    corr_matrix = filtered_df[corr_columns].corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# THIRD ROW
# ----------------------------
col3, col4 = st.columns(2)

with col3:

    fig = px.box(
        filtered_df,
        x="Regional indicator",
        y="Ladder score",
        title="Happiness Score Distribution by Region"
    )

    fig.update_layout(
        height=500,
        xaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col4:

    metrics = [
        "Social support",
        "Healthy life expectancy",
        "Freedom to make life choices",
        "Generosity",
        "Perceptions of corruption"
    ]

    avg_metrics = (
        filtered_df[metrics]
        .mean()
        .reset_index()
    )

    avg_metrics.columns = [
        "Metric",
        "Value"
    ]

    fig = px.bar(
        avg_metrics,
        x="Metric",
        y="Value",
        title="Average Key Indicators",
        text="Value"
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# COUNTRY RANKINGS
# ----------------------------
st.subheader("🏆 Country Rankings")

ranking_df = (
    filtered_df[
        [
            "Country name",
            "Regional indicator",
            "Ladder score"
        ]
    ]
    .sort_values(
        "Ladder score",
        ascending=False
    )
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ----------------------------
# DATA TABLE
# ----------------------------
st.subheader("📋 Full Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ----------------------------
# DOWNLOAD
# ----------------------------
st.download_button(
    label="📥 Download Filtered Dataset",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_world_happiness.csv",
    mime="text/csv"
)

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption("World Happiness Report 2023 Dashboard | Built with Streamlit & Plotly")