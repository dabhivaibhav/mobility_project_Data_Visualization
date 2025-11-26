# 🚌 Mobility Inequality in Cook County  
### Income, Transportation, and Commute Burden — A Data Visualization Project

**Author:** Vaibhav Dabhi  
---

## 📌 Overview

This project investigates how income levels influence transportation access and mobility outcomes within **Cook County, Illinois**.

Using tract-level census data, it explores three major mobility dimensions:

- **Vehicle Ownership**
- **Commute Duration**
- **Public Transit Reliance**

Instead of individuals, each record represents a **neighborhood**.  
This allows mobility patterns to be analyzed at a community level — revealing geographic, structural inequality.

All results are presented through **interactive dashboards built with Python and Plotly.**

---

## 🎯 Research Motivation

Transportation access determines opportunity.

Lower-income neighborhoods often:
- Have fewer private vehicles
- Work farther from job centers
- Rely on public transit
- Experience longer and more unpredictable commutes

Higher-income areas typically:
- Own cars at much higher rates
- Live closer to resources
- Have flexible housing + mobility choices
- Face shorter commute paths

**Core question:**

> Does income level predict mobility access and commute burden at the neighborhood scale?

---

## 📊 Dataset Description

📌 **Source:** U.S. Census American Community Survey (ACS) — Cook County Tract Data

Each row corresponds to a single census tract (neighborhood).  
Key columns:

| Variable | Meaning |
|--------|--------|
| `median_income` | Median household income (USD) |
| `mean_travel_time_min` | Average commute time in minutes |
| `pct_hh_no_vehicle` | % of households with no private vehicle |
| `pct_public` | % of workers using public transit |
| `pct_car` | % of workers commuting by car |
| `tract_name` | Friendly neighborhood name |

These variables capture **mobility, access, and inequality** across the region.

<img width="975" height="309" alt="image" src="https://github.com/user-attachments/assets/ae6284c4-4635-402b-9369-d7a8cfe52cb4" />


---

# 📁 Project Structure
```
MOBILITY PROJECT
├── data_processed/
│   ├── cta_ridership_clean.csv
│   ├── means_transport_clean.csv
│   ├── median_income_clean.csv
│   ├── tract_mobility_master.csv
│   ├── travel_time_clean.csv
│   ├── vehicles_available_clean.csv
│
├── data_raw/
│   ├── community_boundaries.csv
│   ├── cta_entries.csv
│   ├── means_transport.csv
│   ├── median_income.csv
│   ├── travel_time.csv
│   ├── vehicles_available.csv
│
├── figs/
│   ├── commute_inequality.html
│   ├── commute_threshold_slider.html
│   ├── income_vs_no_vehicle_violin.html
│
├── src/
│   ├── build_master_tracts.py
│   ├── check_columns.py
│   ├── clean_cta_ridership.py
│   ├── clean_means_transport.py
│   ├── clean_median_income.py
│   ├── clean_travel_time.py
│   ├── clean_vehicles_available.py
│   ├── commute_inequality_dashboard.py
│   ├── commute_threshold_dashboard.py
│   ├── explore_master_dataset.py
│   ├── income_vs_car_dashboard.py
│   ├── read_data.py
│
├── .gitignore
└── README.md
```
---

# 🛠️ System Architecture

The project follows a structured data pipeline:

Raw Mobility Data ──► Data Cleaning
──► Feature Engineering
──► Master Dataset
──► Interactive Dashboards (3 Visualizations)


**Key design principle:**  
All dashboards reference the **same master dataset**, ensuring consistent comparisons.

---

# 🧽 Data Preparation

To ensure reliable visual insights, several preprocessing steps were implemented:

### ✔ Missing Value Removal
Rows lacking commute or income data were dropped.  
Incomplete tracts distort distribution shapes and bias quartile boundaries.

### ✔ Standardization
- Percent columns were normalized into decimal numeric form.
- Income was stored as raw USD.
- Commute times were rounded to whole minutes (powers animation frames).

### ✔ Income Quartiles
Income groups were generated dynamically:

- Q1 — Lowest 25%
- Q2 — Lower-middle
- Q3 — Upper-middle
- Q4 — Highest 25%

This segmentation ensures **fair comparison within comparable economic bands**.

### ✔ Transit Reliance Metric
A custom tier was derived:
> **Top 25% of transit usage = “High Transit”**

This reveals neighborhoods where transit is necessity rather than choice.

---

# 🛠️ Tools & Libraries

- **Python**
- **Pandas** — data cleaning & ETL
- **NumPy** — correlations & numeric ops
- **Plotly Express** — early prototypes
- **Plotly Graph Objects** — custom UI, animations, frames, legends

Plotly was chosen because visualization happens **in-browser**, not just in code.  
Users can interact naturally without running Python notebooks.

---

# 🎨 Visualization Strategy

Each dashboard answers a different analytical question.

### 🔹 Distribution Visuals
Show inequality *within* groups  
(violins, density histograms)

### 🔹 Relationship Visuals
Show how variables move together  
(scatter: income vs commute)

### 🔹 Segmentation by Income
Every visualization uses **income quartiles** for fair comparison.

### 🔹 Interactivity
- **Legend: isolate one group**
- **Hover: view tract-level details**
- **Slider: explore commute time frames**

### 🔹 Consistent Color System
| Quartile | Color |
|---------|------|
| Q1 | Purple |
| Q2 | Blue |
| Q3 | Green |
| Q4 | Yellow |

Visual continuity reduces cognitive load.

---

---

# 🟣 Dashboard 1 — Income vs Vehicle Ownership

### **Purpose**
Reveal whether lower-income neighborhoods lack private vehicle access.

### 🔧 Visualization Design
- **Violin plot** — displays full distribution, not just averages
- **Each dot = one census tract**
- **Color-coded quartiles (Q1–Q4)**

This emphasizes variation *within* income groups.

<img width="975" height="514" alt="image" src="https://github.com/user-attachments/assets/800cd161-6bc0-4724-a2b7-8579e4ce2667" />

---

### 🧠 Key Insight

> Q1 neighborhoods can reach **20–50% car-less households**.  
> Q4 neighborhoods rarely exceed **8%**.

Private vehicle access increases dramatically with income.

---

### 💡 Why a Violin Plot?

Averages hide inequality.  
Violin plots expose:

- clusters
- long tails
- distribution shape
- outliers

This turns vehicle ownership into a **story of lived inequality**, not just numbers.

---

---

# 🟢 Dashboard 2 — Commute Inequality (3-View)

### **Purpose**
Show how commute burden changes across income groups.

### Visualization Layout
Top — Income Histogram
BottomL — Income vs Commute Scatter
BottomR — Commute Time Density Histogram

<img width="975" height="415" alt="image" src="https://github.com/user-attachments/assets/0fc8d56c-13bc-4c65-b455-5246cda2a326" />

### What It Shows
- Long commutes cluster in **low-income tracts**
- Wealthy neighborhoods enjoy **shorter commute windows**

The views reinforce each other:
- Histogram shows distribution
- Scatter shows correlation
- Density histogram shows inequality *within* bins

---

### 🔍 Findings

- Q1 neighborhoods dominate **35–45+ minute** commutes
- Q4 tracts concentrate **18–28 minutes**
- Correlation becomes strongest at extremes
- At the Q4 level, commute distribution is narrow and compressed

This demonstrates mobility inequality as **systemic**, not behavioral.

---

---

# 🟡 Dashboard 3 — Transit Reliance vs Income (Animated)

### **Purpose**
Introduce commute time as a dynamic layer.

Instead of static plots:
👉 users “walk through” commute minutes using a slider

### Implementation
Built using **plotly.graph_objects** to enable:

- Custom animation frames
- Stable axis bounds across time
- Legend filtering
- Hover tooltips
- Frame-based filtering

<img width="975" height="512" alt="image" src="https://github.com/user-attachments/assets/e22bd981-54eb-4555-9592-03dbfc7d1ae0" />

### Behavior

- **Default view = All neighborhoods**
- **Slider = only tracts with mean commute == M**
- **Legend = isolate an income group**

---

### 🧩 Emerging Pattern

> Short commutes → **high-income tracts dominate (Q3–Q4)**  
> Long commutes → **low-income tracts dominate (Q1–Q2)**

Transit use is **not a preference**.  
It is a **constraint tied to commute burden**.

---

# 💡 Technical Contribution

I selected `plotly.graph_objects` over Plotly Express to build the final dashboard because:

- It allows manual construction of animation frames
- Axes remain fixed across time (no jittering scale)
- Legend interaction can isolate groups
- Hover tooltips show tract name + commute minutes
- Sliders and play/pause controls can be fully customized

Express → great for prototypes  
Graph Objects → **required for professional interactive dashboards**

---

# ⭐ Key Findings

✔ **Income strongly predicts vehicle access**  
Lower quartiles show up to 50% car-less households.

✔ **Commute Time Burden is Unequal**  
Poor neighborhoods spend more time traveling — cost paid in hours.

✔ **Transit Reliance Concentrates in Q1–Q2**  
Reliance increases as income decreases.

✔ **Mobility is structural**  
Not based on preference — based on resources.

---

# ⚠️ Limitations

- Dataset is cross-sectional (not time-series)
- Tract averages ≠ individual lives
- Commute duration ≠ commute reliability
- No causal inference models used

---

# 🧭 Future Improvements

- Add time-series mobility trends
- Include CTA or Metra infrastructure layers
- Combine jobs-housing accessibility metrics
- Expand to other metro regions

---

# 📚 References (APA)

American Community Survey. (2023). *Transportation Characteristics of Workers by Means of Transportation.*  
U.S. Census Bureau. https://www.census.gov/programs-surveys/acs/

U.S. Census Bureau. (2021). *American Community Survey 5-Year Estimates (Table DP03: Selected Economic Characteristics).*  
https://data.census.gov

---

