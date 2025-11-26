# Dashboard 3: Transit Reliance vs Income (animated by commute time)
# This dashboard shows how public transit use varies across income groups,
# and how that pattern changes as we move through different mean commute times.

import os
import pandas as pd
import plotly.graph_objects as go

# Load input data produced by the preprocessing pipeline.
# This file contains one row per census tract with income, commute time,
# and mode-share percentages (car, transit, etc.).
df = pd.read_csv("./data_processed/tract_mobility_master.csv")

# Keep only rows that have all fields needed for this dashboard.
# We need: income (median), transit share (% using public transit),
# and mean travel time to work.
df = df.dropna(subset=["median_income", "pct_public", "mean_travel_time_min"]).copy()
print("Rows used:", len(df))

# Build income quartiles so each tract is assigned to an income group.
# This matches the same grouping used in the other dashboards.
q25 = df["median_income"].quantile(0.25)
q50 = df["median_income"].quantile(0.50)
q75 = df["median_income"].quantile(0.75)


def income_group(v):
    """Map a median income value to one of four income quartile labels."""
    if v <= q25:
        return "Q1 – Lowest income"
    if v <= q50:
        return "Q2 – Lower-middle"
    if v <= q75:
        return "Q3 – Upper-middle"
    return "Q4 – Highest income"


df["Income Group"] = df["median_income"].apply(income_group)

# Fixed quartile ordering keeps colors and legend ordering predictable.
quartile_order = [
    "Q1 – Lowest income",
    "Q2 – Lower-middle",
    "Q3 – Upper-middle",
    "Q4 – Highest income",
]

# Consistent colors across all dashboards so viewers can build intuition:
# purple = lowest income, yellow = highest income.
colors = {
    "Q1 – Lowest income": "#440154",  # purple
    "Q2 – Lower-middle": "#31688e",  # blue
    "Q3 – Upper-middle": "#35b779",  # green
    "Q4 – Highest income": "#fde725",  # yellow
}

# Convert mean commute time into whole minutes.
# This rounded value is used as the animation frame variable.
df["commute_min"] = df["mean_travel_time_min"].round().astype(int)

# Remove tracts with extremely short commute values (under 5 minutes),
# which are often unusual and can make the slider less meaningful.
df = df[df["commute_min"] >= 5].copy()

# Collect the sorted list of unique commute minutes to use as frames.
minutes = sorted(df["commute_min"].unique())
print("Commute minutes in data:", minutes[0], "to", minutes[-1])

# Fix axis ranges for all frames so the animation feels stable.
x_min = df["median_income"].min()
x_max = df["median_income"].max()
y_min = 0.0
y_max = df["pct_public"].max() * 1.05

# Build the initial figure for the "All minutes" view.
# In this starting view, we show all tracts together with no commute filter.
fig = go.Figure()
all_traces = []

for q in quartile_order:
    sub = df[df["Income Group"] == q]

    # customdata stores extra fields for the hover tooltip:
    # tract name and commute minutes.
    customdata = list(zip(sub["tract_name"], sub["commute_min"]))

    trace = go.Scatter(
        x=sub["median_income"],
        y=sub["pct_public"],
        mode="markers",
        name=q,
        marker=dict(color=colors[q], size=7, opacity=0.7),
        customdata=customdata,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Income group: " + q + "<br>"
            "Mean commute: %{customdata[1]} minutes<br>"
            "Median income: $%{x:,.0f}<br>"
            "Transit share: %{y:.1%}<extra></extra>"
        ),
    )

    fig.add_trace(trace)
    all_traces.append(trace)

# Build animation frames.
# Each frame represents either:
# "all"  → all commute minutes together, or
# a specific minute (e.g., "25") → tracts whose mean commute equals that value.

frames = []

# Frame 0: "all" minutes with the full dataset.
frames.append(go.Frame(name="all", data=all_traces))

# Frames for each commute minute value.
for m in minutes:
    df_m = df[df["commute_min"] == m]
    minute_traces = []

    for q in quartile_order:
        sub = df_m[df_m["Income Group"] == q]
        customdata = list(zip(sub["tract_name"], sub["commute_min"]))

        minute_traces.append(
            go.Scatter(
                x=sub["median_income"],
                y=sub["pct_public"],
                mode="markers",
                name=q,
                marker=dict(color=colors[q], size=7, opacity=0.7),
                customdata=customdata,
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Income group: " + q + "<br>"
                    "Mean commute: %{customdata[1]} minutes<br>"
                    "Median income: $%{x:,.0f}<br>"
                    "Transit share: %{y:.1%}<extra></extra>"
                ),
            )
        )

    frames.append(go.Frame(name=str(m), data=minute_traces))

fig.frames = frames

# The slider controls which frame is visible: "All minutes" or a specific minute.
slider_steps = []

# First slider step: show all tracts at once (no filtering by commute time).
slider_steps.append(
    dict(
        label="All minutes",
        method="animate",
        args=[
            ["all"],
            {
                "frame": {"duration": 0, "redraw": True},
                "mode": "immediate",
                "transition": {"duration": 0},
            },
        ],
    )
)

# Add one step per commute minute so the user can scrub through the distribution.
for m in minutes:
    slider_steps.append(
        dict(
            label=str(m),
            method="animate",
            args=[
                [str(m)],
                {
                    "frame": {"duration": 0, "redraw": True},
                    "mode": "immediate",
                    "transition": {"duration": 0},
                },
            ],
        )
    )

sliders = [
    dict(
        active=0,  # start with the "All minutes" view selected
        pad={"t": 60},
        currentvalue={
            "prefix": "Mean commute time (minutes): ",
            "visible": True,
        },
        steps=slider_steps,
    )
]

# Play / Pause buttons for automatic animation.
# Play walks through each minute frame; Pause stops on the current one.
updatemenus = [
    dict(
        type="buttons",
        direction="left",
        x=0.05,
        y=-0.1,
        showactive=False,
        pad={"r": 10, "t": 40},
        buttons=[
            dict(
                label="▶",
                method="animate",
                args=[
                    None,
                    {
                        "frame": {"duration": 400, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 0},
                    },
                ],
            ),
            dict(
                label="⏸",
                method="animate",
                args=[
                    [None],
                    {
                        "frame": {"duration": 0, "redraw": False},
                        "mode": "immediate",
                    },
                ],
            ),
        ],
    )
]

# Layout settings: axes, legend behavior, title, margins, and controls.
fig.update_layout(
    template="plotly_white",
    title=(
        "Transit Reliance vs Income (animated by commute time)<br>"
        "<sup>Initial view shows all tracts. Move the slider or press Play "
        "to see only tracts with a given mean commute time; use the legend "
        "to highlight an income group.</sup>"
    ),
    xaxis=dict(
        title="Median household income (USD)",
        tickprefix="$",
        tickformat=",",
        range=[x_min, x_max],
    ),
    yaxis=dict(
        title="% of workers using public transit",
        tickformat=".0%",
        rangemode="tozero",
        range=[y_min, y_max],
    ),
    legend_title="Income Group",
    legend=dict(
        itemclick="toggleothers",  # click once to isolate one income group
        itemdoubleclick="toggle",  # double click to toggle normally
    ),
    sliders=sliders,
    updatemenus=updatemenus,
    margin=dict(l=70, r=40, t=110, b=120),
)

# Save dashboard as an interactive HTML file and display it.
os.makedirs("./figs", exist_ok=True)

fig.write_html(
    "./figs/commute_threshold_slider.html",
    include_plotlyjs="cdn",
)

print("Saved interactive figure to ./figs/commute_threshold_slider.html")
