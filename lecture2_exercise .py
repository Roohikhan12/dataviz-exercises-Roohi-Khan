#!/usr/bin/env python
# coding: utf-8

# # Lecture 2 — Class Exercise
# # Bar Charts: World Happiness Report 2023
# 
# ---
# 
# > **Your task:** Create **2 polished bar charts** using the World Happiness Report dataset.  
# > **Push to:** `week02/lecture02_exercise.ipynb` in **your own GitHub repo** before the end of class.
# 
# ---
# 
# ### Rules (these will be checked in the model answer review next week)
# 1. Every bar chart **must have a zero baseline** — no exceptions (SWD p.51)
# 2. Every chart **must have an insight title**, not a topic title (SWD p.29)
# 3. Aim for **professional quality** — clean background, readable font, no clutter
# 4. Horizontal bars for long category names (SWD p.57)
# 
# ---
# 

# ## Setup — Run this cell first
# 

# In[6]:


import pandas as pd
import numpy as np

# World Happiness Report 2023 — representative data
# Source: https://www.kaggle.com/datasets/ajaypalsinghlo/world-happiness-report-2023

df = pd.read_csv(r'C:\Users\Mubeen Khan\Downloads\world_happiness_2023.csv')
df.columns = ['Country','Region','Happiness_Score','GDP','Social_Support',
              'Life_Expectancy','Freedom','Generosity','Corruption']


print(f"Dataset: {len(df)} countries, {len(df.columns)} columns")
print(df.head())


# In[7]:


import plotly.express as px
import plotly.graph_objects as go

# Explore the dataset before you start
print("Regions in dataset:")
print(df['Region'].value_counts())
print("\nScore range:", df['Happiness_Score'].min(), "–", df['Happiness_Score'].max())
print("\nBottom 10 countries:")
print(df.nsmallest(10, 'Happiness_Score')[['Country','Region','Happiness_Score']])


# ---
# ## Task 1 — Regional Comparison Bar Chart
# 
# **What to build:** A horizontal bar chart showing the **average happiness score by region**, sorted from highest to lowest.
# 
# **Requirements:**
# - Horizontal orientation (category names are long)
# - Sorted by score, descending (so the happiest region is at the top)
# - Zero baseline on x-axis
# - At least one design choice that goes beyond the Plotly default (colour, annotation, labels, etc.)
# - An insight title that answers: *which region stands out and why does it matter?*
# 
# **Hint:** Use `df.groupby('Region')['Happiness_Score'].mean()` to compute the averages.
# 

# In[8]:


# Task 1: Regional comparison bar chart
# -------------------------------------

# Step 1: Compute average happiness score by region
region_avg = (df.groupby('Region')['Happiness_Score']
              .mean()
              .reset_index()
              .sort_values('Happiness_Score'))  # sort ascending for horizontal bar (top = highest)

print(region_avg)

# Step 2: Build the chart
global_avg = df['Happiness_Score'].mean()

# Colour: highlight the top region in a warm gold, others in steel blue
colors = ['#4a90d9' if score < region_avg['Happiness_Score'].max() else '#f5a623'
          for score in region_avg['Happiness_Score']]

fig1 = go.Figure()

fig1.add_trace(go.Bar(
    y=region_avg['Region'],
    x=region_avg['Happiness_Score'],
    orientation='h',
    marker_color=colors,
    text=region_avg['Happiness_Score'].round(2),
    textposition='outside',
    textfont=dict(size=11, color='#333333'),
    cliponaxis=False
))

# Add global average reference line
fig1.add_vline(
    x=global_avg,
    line_dash='dash',
    line_color='#e05c2a',
    line_width=1.5,
    annotation_text=f'Global avg: {global_avg:.2f}',
    annotation_position='top',
    annotation_font=dict(size=10, color='#e05c2a')
)

fig1.update_layout(
    title=dict(
        text='Western Europe leads global happiness by a wide margin — Sub-Saharan Africa lags nearly 3 points behind',
        font=dict(size=14, color='#1a1a2e'),
        x=0
    ),
    xaxis=dict(
        title='Average Happiness Score',
        range=[0, region_avg['Happiness_Score'].max() * 1.15],  # zero baseline enforced
        showgrid=True,
        gridcolor='#e8e8e8',
        zeroline=True,
        zerolinecolor='#333333',
        zerolinewidth=1.5
    ),
    yaxis=dict(
        title='',
        tickfont=dict(size=11)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=10, r=80, t=70, b=50),
    height=420,
    showlegend=False
)

fig1.show()


# ---
# ## Task 2 — Bottom vs. Top: A Contrast Story
# 
# **What to build:** A bar chart that highlights the **gap between the happiest and least happy countries**, focusing on a specific insight.
# 
# **Requirements:**
# - Show the **top 8 AND bottom 8 countries** together (16 bars total)
# - Use **colour** to distinguish the two groups (not Plotly's default rainbow)
# - Add a **visual separator or annotation** that emphasises the gap
# - Insight title that tells the story of the gap
# 
# **Hint:** Use `pd.concat([df.nlargest(8,'Happiness_Score'), df.nsmallest(8,'Happiness_Score')])` to get both groups.
# 
# **Stretch goal:** Add a vertical reference line showing the global average.
# 

# In[19]:


# Task 2: Top 8 vs. Bottom 8 contrast
# ------------------------------------

# Step 1: Get top and bottom countries
top8 = df.nlargest(8, 'Happiness_Score').copy()
top8['Group'] = 'Top 8'
bottom8 = df.nsmallest(8, 'Happiness_Score').copy()
bottom8['Group'] = 'Bottom 8'

combined = pd.concat([bottom8, top8]).sort_values('Happiness_Score')
global_avg = df['Happiness_Score'].mean()
print(f"Global average: {global_avg:.2f}")
print(f"Gap between top and bottom groups: {top8['Happiness_Score'].mean() - bottom8['Happiness_Score'].mean():.2f} points")

# Step 2: Build the chart
color_map = {'Top 8': '#2ecc71', 'Bottom 8': '#e74c3c'}
bar_colors = [color_map[g] for g in combined['Group']]

fig2 = go.Figure()

# Add bars for each group separately so legend works
for group, color in color_map.items():
    subset = combined[combined['Group'] == group]
    fig2.add_trace(go.Bar(
        y=subset['Country'],
        x=subset['Happiness_Score'],
        orientation='h',
        name=group,
        marker_color=color,
        text=subset['Happiness_Score'].round(2),
        textposition='outside',
        textfont=dict(size=10, color='#333333'),
        cliponaxis=False
    ))

# Global average reference line (stretch goal)
fig2.add_vline(
    x=global_avg,
    line_dash='dot',
    line_color='#f39c12',
    line_width=2,
    annotation_text=f'Global avg {global_avg:.2f}',
    annotation_position='top',
    annotation_font=dict(size=10, color='#f39c12', family='Arial')
)

# Separator annotation between the two groups
top8_min = top8['Happiness_Score'].min()
bottom8_max = bottom8['Happiness_Score'].max()
gap_midpoint = (top8_min + bottom8_max) / 2

fig2.add_annotation(
    x=gap_midpoint,
    y=7.5,          # position between bar 8 and bar 9 (0-indexed)
    text=f"← {top8['Happiness_Score'].mean() - bottom8['Happiness_Score'].mean():.1f} point gap →",
    showarrow=False,
    font=dict(size=11, color='#555555', family='Arial'),
    bgcolor='#f9f9f9',
    bordercolor='#cccccc',
    borderwidth=1,
    borderpad=4
)

# Horizontal separator line between top and bottom groups
fig2.add_hline(
    y=7.5,
    line_dash='solid',
    line_color='#bbbbbb',
    line_width=1
)

fig2.update_layout(
    title=dict(
        text='The happiness gap is stark: top countries score over 3 points higher than the bottom — a near-unbridgeable divide',
        font=dict(size=13, color='#1a1a2e'),
        x=0
    ),
    xaxis=dict(
        title='Happiness Score',
        range=[0, combined['Happiness_Score'].max() * 1.15],  # zero baseline
        showgrid=True,
        gridcolor='#eeeeee',
        zeroline=True,
        zerolinecolor='#333333',
        zerolinewidth=1.5
    ),
    yaxis=dict(
        title='',
        tickfont=dict(size=10)
    ),
    barmode='overlay',
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=11)
    ),
    margin=dict(l=10, r=80, t=80, b=50),
    height=520
)

fig2.show()



# ---
# ## Done? Stretch Goal
# 
# If you finish both tasks with time to spare, try this:
# 
# **Task 3 (stretch):** Build a **grouped bar chart** comparing 2 sub-factors (e.g. `GDP_per_capita` and `Freedom`) across the 5 most populated regions. Use colour meaningfully and write an insight title.
# 
# Regions to include: `'Western Europe'`, `'Latin America'`, `'East Asia'`, `'Sub-Saharan Africa'`, `'South Asia'`
# 

# In[11]:


# Stretch goal — grouped bar chart: GDP vs Freedom across 5 key regions
# -----------------------------------------------------------------------

regions_of_interest = ['Western Europe', 'Latin America and Caribbean',
                       'East Asia', 'Sub-Saharan Africa', 'South Asia']

# Filter and compute averages for the two factors
stretch_df = (df[df['Region'].isin(regions_of_interest)]
              .groupby('Region')[['GDP', 'Freedom']]
              .mean()
              .reset_index())

# Shorten region names for readability
stretch_df['Region'] = stretch_df['Region'].replace({
    'Latin America and Caribbean': 'Latin America'
})

# Sort by GDP descending
stretch_df = stretch_df.sort_values('GDP', ascending=False)

print(stretch_df)

fig3 = go.Figure()

fig3.add_trace(go.Bar(
    name='GDP per Capita',
    x=stretch_df['Region'],
    y=stretch_df['GDP'],
    marker_color='#000000',
    text=stretch_df['GDP'].round(2),
    textposition='outside',
    textfont=dict(size=10)
))

fig3.add_trace(go.Bar(
    name='Freedom to Make Life Choices',
    x=stretch_df['Region'],
    y=stretch_df['Freedom'],
    marker_color='#ff1493',
    text=stretch_df['Freedom'].round(2),
    textposition='outside',
    textfont=dict(size=10)
))

fig3.update_layout(
    title=dict(
        text='Wealth and freedom diverge: Latin America scores higher on freedom than GDP would predict, while East Asia shows the reverse',
        font=dict(size=13, color='#1a1a2e'),
        x=0
    ),
    barmode='group',
    xaxis=dict(
        title='',
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        title='Score (0–1 scale)',
        range=[0, stretch_df[['GDP','Freedom']].max().max() * 1.2],  # zero baseline
        showgrid=True,
        gridcolor='#eeeeee',
        zeroline=True,
        zerolinecolor='#333333',
        zerolinewidth=1.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=11)
    ),
    margin=dict(l=10, r=20, t=90, b=50),
    height=440
)

fig3.show()


# In[ ]:




