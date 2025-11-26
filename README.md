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

---

# 🛠️ System Architecture

The project follows a structured data pipeline:

