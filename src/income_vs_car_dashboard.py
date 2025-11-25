import pandas as pd
import plotly.express as px

# Load the mobility master dataset
# Contains census-tract level income + mobility data
df = pd.read_csv("./data_processed/tract_mobility_master.csv")

# Keep only tracts that have valid income and % of households without vehicles
df = df.dropna(subset=["median_income", "pct_hh_no_vehicle"]).copy()
print("Rows used:", len(df))

# Create income groups using statistical quartiles
# Q1 is the lowest 25% of incomes, Q4 is the highest 25%
# This ensures fair comparisons between neighborhoods
q25 = df["median_income"].quantile(0.25)
q50 = df["median_income"].quantile(0.50)
q75 = df["median_income"].quantile(0.75)


def assign_quartile(income):
    """
    Assign an income group label based on quartile thresholds.
    Quartiles divide the population into 4 equal-sized economic groups.
    """
    if income <= q25:
        return "Q1 – Lowest income"
    elif income <= q50:
        return "Q2 – Lower-middle"
    elif income <= q75:
        return "Q3 – Upper-middle"
    else:
        return "Q4 – Highest income"


df["Income Group"] = df["median_income"].apply(assign_quartile)

income_order = [
    "Q1 – Lowest income",
    "Q2 – Lower-middle",
    "Q3 – Upper-middle",
    "Q4 – Highest income",
]

# Build the violin plot
# - X axis: income groups (Q1–Q4)
# - Y axis: % households without a vehicle
# - Each dot represents a census tract
#
# Why violin?
# It shows the full distribution: peaks, tails, and density.
# Bar charts hide inequality — violins expose it.
fig = px.violin(
    df,
    x="Income Group",
    y="pct_hh_no_vehicle",
    color="Income Group",
    category_orders={"Income Group": income_order},
    box=False,  # hide internal box — we want pure distribution
    points="all",  # show each tract as a point to preserve raw detail
)

# Improve visual readability of scattered points
fig.update_traces(
    jitter=0.25,  # spread points horizontally to prevent overlap
    marker_size=4,
    opacity=0.45,
)


# Chart formatting and interaction
fig.update_layout(
    title=(
        "Income Quartile vs % Households with No Vehicle<br>"
        "<sup>Each dot represents a census tract; violins show the distribution within each income group.</sup>"
    ),
    xaxis_title="Income Quartile (Q1 = lowest income, Q4 = highest income)",
    yaxis_title="% Households with No Vehicles",
    yaxis_tickformat=".0%",  # show percentages like 35%
    template="plotly_white",  # clean visual style
    legend_title_text="Income Group",
    # Legend interaction:
    # Single click: isolate a single income group
    # Double click: hide/show normally
    legend_itemclick="toggleothers",
    legend_itemdoubleclick="toggle",
)

# Add a short guidance hint above the chart
fig.add_annotation(
    text="Legend: click an income group to show only that group; click again to restore all.",
    xref="paper",
    yref="paper",
    x=0.5,
    y=1.12,
    showarrow=False,
    font=dict(size=11),
    align="center",
)

# Disable selection tools
# These tools cause mass highlighting and make the violins unreadable.
# We keep hover and legend interactivity only.
config = {
    "modeBarButtonsToRemove": ["select2d", "lasso2d", "boxSelect"],
    "displaylogo": False,
}

# Export interactive HTML file
# Students and professors can open it in any browser
# without needing Python installed
fig.write_html(
    "./figs/income_vs_no_vehicle_violin.html",
    include_plotlyjs="cdn",
    config=config,
)
print("Saved HTML to ./figs/income_vs_no_vehicle_violin.html")
