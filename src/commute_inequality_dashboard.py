# commute_inequality.py
#
# Visualization 2: Commute Time Inequality
# This dashboard investigates whether lower-income neighborhoods face longer commute times.
# The plot combines three linked views:
#   1. Income distribution per quartile (histogram)
#   2. Income vs commute time relationship (scatter)
#   3. Commute time distribution per quartile (horizontal histogram)

import os
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Load mobility dataset produced during preprocessing.
# It contains one row per census tract with income, commute time, and mobility stats.
df = pd.read_csv("./data_processed/tract_mobility_master.csv")

# We are only analyzing commute inequality, so rows without key metrics are dropped.
# Missing values here would bias correlations and distributions.
df = df.dropna(subset=["median_income", "mean_travel_time_min"]).copy()


# Calculate income quartile thresholds.
# Quartiles split census tracts into 4 equally sized economic groups.
q25 = df["median_income"].quantile(0.25)
q50 = df["median_income"].quantile(0.50)
q75 = df["median_income"].quantile(0.75)


def income_quartile(v):
    """Assign a tract to an income quartile based on median household income."""
    if v <= q25:
        return "Q1 – Lowest income"
    if v <= q50:
        return "Q2 – Lower-middle"
    if v <= q75:
        return "Q3 – Upper-middle"
    return "Q4 – Highest income"


df["Income Quartile"] = df["median_income"].apply(income_quartile)

# Fixed order of quartiles ensures consistent visual encoding across all dashboards.
quartile_order = [
    "Q1 – Lowest income",
    "Q2 – Lower-middle",
    "Q3 – Upper-middle",
    "Q4 – Highest income",
]

# Assign a unique color to each quartile for visual continuity.
colors = {
    "Q1 – Lowest income": "#440154",  # purple
    "Q2 – Lower-middle": "#31688e",  # blue
    "Q3 – Upper-middle": "#35b779",  # green
    "Q4 – Highest income": "#fde725",  # yellow
}


# Compute overall correlation between income and commute time.
# This helps quantify the strength of inequality, not just visualize it.
overall_r = df[["median_income", "mean_travel_time_min"]].corr().iloc[0, 1]

# Also compute correlation within each income quartile to reveal internal inequality.
r_by_q = {}
for q in quartile_order:
    sub = df[df["Income Quartile"] == q]
    if len(sub) > 1:
        r_by_q[q] = sub[["median_income", "mean_travel_time_min"]].corr().iloc[0, 1]
    else:
        r_by_q[q] = np.nan


# Create a compound subplot layout:
# Row 1  - income distribution only (histogram)
# Row 2  - scatter plot + commute histogram side panel
# This provides multiple perspectives using the same population.
fig = make_subplots(
    rows=2,
    cols=2,
    row_heights=[0.25, 0.75],  # small header, larger analytical area
    column_widths=[0.75, 0.25],  # main scatter on left, distribution on right
    specs=[
        [{"type": "xy", "colspan": 2}, None],
        [{"type": "xy"}, {"type": "xy"}],
    ],
    shared_xaxes=True,  # income axis shared vertically
    vertical_spacing=0.06,
    horizontal_spacing=0.08,
)


# First layer: income histogram per quartile.
# Shows how economically separated the neighborhoods are.
for q in quartile_order:
    sub = df[df["Income Quartile"] == q]
    fig.add_trace(
        go.Histogram(
            x=sub["median_income"],
            name=q,
            legendgroup=q,  # link with scatter + commute histogram
            marker=dict(color=colors[q]),
            opacity=0.5,
            nbinsx=30,
            histnorm="probability density",  # shape-based visualization
            showlegend=False,  # avoid duplicate legend rows
        ),
        row=1,
        col=1,
    )


# Second layer: scatter of income vs commute time.
# Every point represents a census tract.
# This plot exposes the core inequality pattern visually.
for q in quartile_order:
    sub = df[df["Income Quartile"] == q]
    fig.add_trace(
        go.Scatter(
            x=sub["median_income"],
            y=sub["mean_travel_time_min"],
            mode="markers",
            name=q,
            legendgroup=q,
            marker=dict(
                color=colors[q],
                size=7,
                opacity=0.65,
            ),
            customdata=np.stack([sub["tract_name"], sub["Income Quartile"]], axis=-1),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Income group: %{customdata[1]}<br>"
                "Median income: $%{x:,.0f}<br>"
                "Mean commute: %{y:.1f} minutes"
                "<extra></extra>"
            ),
        ),
        row=2,
        col=1,
    )


# Third layer: commute time histogram per quartile (horizontal).
# Shows distribution of commute durations per group.
for q in quartile_order:
    sub = df[df["Income Quartile"] == q]
    fig.add_trace(
        go.Histogram(
            y=sub["mean_travel_time_min"],
            name=q,
            legendgroup=q,
            marker=dict(color=colors[q]),
            opacity=0.5,
            nbinsy=30,
            histnorm="probability density",
            orientation="h",
            showlegend=False,
        ),
        row=2,
        col=2,
    )


# Display the correlation summary directly on the canvas.
# This helps the viewer understand inequality numerically.
lines = [f"Overall r = {overall_r:.2f}"]
for q in quartile_order:
    r = r_by_q[q]
    label = q.split("–")[0].strip()  # keep labels compact
    lines.append(f"{label}  r = {r:.2f}" if not np.isnan(r) else f"{label}  r = NA")

fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0.02,
    y=0.96,
    align="left",
    showarrow=False,
    text="<br>".join(lines),
    font=dict(size=11),
)


# Global layout settings:
# - unified color system
# - interaction rules
# - meaningfully formatted axes
fig.update_layout(
    template="plotly_white",
    title=(
        "Does commute time increase for lower-income neighborhoods?<br>"
        "<sup>Income vs mean travel time to work — Cook County census tracts</sup>"
    ),
    height=700,
    legend_title="Income Group",
    legend=dict(
        itemclick="toggleothers",  # click one - isolate group
        itemdoubleclick="toggle",  # double click - traditional toggle
    ),
    bargap=0.05,
)


# Axis formatting for each subplot
fig.update_xaxes(
    title_text="Median household income (USD)",
    tickprefix="$",
    tickformat=",",
    row=2,
    col=1,
)
fig.update_yaxes(
    title_text="Mean travel time to work (minutes)",
    row=2,
    col=1,
)

fig.update_xaxes(
    title_text="Median household income (USD)",
    tickprefix="$",
    tickformat=",",
    showticklabels=False,  # avoid duplicate labels above scatter
    row=1,
    col=1,
)
fig.update_yaxes(
    title_text="Density",
    row=1,
    col=1,
)

fig.update_xaxes(
    title_text="Density",
    row=2,
    col=2,
)
fig.update_yaxes(
    title_text="Mean travel time to work (minutes)",
    row=2,
    col=2,
)


# Disable lasso selection, since it interferes with linked filtering.
# Box-select remains available.
fig.update_layout(modebar_remove=["lasso2d"])


# Export to interactive HTML so anyone can explore without Python installed.
os.makedirs("./figs", exist_ok=True)
fig.write_html(
    "./figs/commute_inequality.html",
    include_plotlyjs="cdn",
    full_html=True,
)

print("Saved interactive figure to ./figs/commute_inequality.html")
