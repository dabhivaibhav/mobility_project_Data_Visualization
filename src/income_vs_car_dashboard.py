import pandas as pd
import plotly.express as px

# ========= LOAD DATA =========
df = pd.read_csv("./data_processed/tract_mobility_master.csv")

# Keep only rows with both income + no-vehicle percentage
df = df.dropna(subset=["median_income", "pct_hh_no_vehicle"]).copy()
print("Rows used:", len(df))

# ========= INCOME QUARTILES =========
q25 = df["median_income"].quantile(0.25)
q50 = df["median_income"].quantile(0.50)
q75 = df["median_income"].quantile(0.75)


def assign_quartile(income):
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

# ========= BUILD VIOLIN (NO BOX) =========
fig = px.violin(
    df,
    x="Income Group",
    y="pct_hh_no_vehicle",
    color="Income Group",
    category_orders={"Income Group": income_order},
    box=False,  # ❌ no internal box-plot inside violin
    points="all",  # ✅ show all tracts as dots
)

fig.update_traces(
    jitter=0.25,
    marker_size=4,
    opacity=0.45,
)

# ========= LAYOUT & LEGEND BEHAVIOR =========
fig.update_layout(
    title=(
        "Income Quartile vs % Households with No Vehicle<br>"
        "<sup>Each dot is a census tract; violins show the distribution within each income group.</sup>"
    ),
    xaxis_title="Income Quartile (Q1 = lowest income, Q4 = highest income)",
    yaxis_title="% Households with No Vehicles",
    yaxis_tickformat=".0%",
    template="plotly_white",
    legend_title_text="Income Group",
    # 🔧 Legend behavior:
    # single-click -> isolate that category (show only it)
    # double-click -> normal toggle
    legend_itemclick="toggleothers",
    legend_itemdoubleclick="toggle",
)

# Add instruction text inside the chart
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

# ========= REMOVE LASSO & BOX-SELECT TOOLS =========
config = {
    # keep modebar, but remove box & lasso selection tools
    "modeBarButtonsToRemove": ["select2d", "lasso2d", "boxSelect"],
    "displaylogo": False,
}


# (Optional) also save to HTML & PNG with same config
fig.write_html(
    "./figs/income_vs_no_vehicle_violin.html",
    include_plotlyjs="cdn",
    config=config,
)
print("Saved HTML to ./figs/income_vs_no_vehicle_violin.html")
