# Collections & Recovery Analytics

### End-to-End Data Analytics | Python • SQL • Power BI

An end-to-end data analytics project focused on evaluating collections and recovery performance, identifying data-quality issues, validating business KPIs and delivering actionable insights through Python, SQL and Power BI.

## Project Overview

This project examines collections-related datasets to assess recovery performance, payment trends, operational outcomes and data reliability.

The analysis focuses on an important business question:

**Does the available payment data support the reported 11% month-on-month improvement in collections performance?**

The project combines data preprocessing, SQL-based analysis, KPI evaluation, interactive dashboards and executive-level recommendations.

## Key Findings

| Performance Metric | Result |
|---|---:|
| June 2026 Gross Successful Payments | ₹17.59 Cr |
| July 2026 Gross Successful Payments | ₹18.72 Cr |
| July Month-on-Month Growth | **6.48%** |
| Reported Growth Benchmark | 11% |
| Total Accounts Analysed | 30,000 |

**Primary Insight:** The analysis identifies approximately 6.48% month-on-month growth in gross successful payments for July 2026, rather than the reported 11%.

These figures represent gross successful payment value rather than net settled recovery. Payment reference inconsistencies and incomplete reversal linkage limit the reliability of net recovery calculations.

## Technology Stack

| Technology | Application |
|---|---|
| Python | Data cleaning, preprocessing, analysis and KPI calculations |
| Pandas & NumPy | Data manipulation and numerical analysis |
| PostgreSQL | SQL querying, aggregation and analytical transformations |
| Power BI | Interactive dashboards, KPI tracking and performance visualization |
| Jupyter Notebook / Google Colab | Exploratory analysis and analytical documentation |

## Project Structure

```text
Collections_Recovery_Perfor/
│
├── Collections_Analytics_Submission/
│   ├── data/
│   │   ├── raw/
│   │   └── golden/
│   ├── notebooks/
│   │   └── Collections_Analytics_Colab.ipynb
│   ├── sql/
│   ├── src/
│   │   └── build_analysis.py
│   ├── reports/
│   │   ├── executive_memo.pdf
│   │   ├── executive_memo.md
│   │   └── data_quality_report.md
│   ├── figures/
│   └── Collections_Recovery_Performance_Dashboard_Pushkar.pbix
│
├── README.md
└── SUBMISSION_CONTENTS.txt
```

## Analytical Methodology

### 1. Data Exploration & Quality Assessment

- Examined the supplied collections and recovery datasets.
- Identified duplicate payment records and identifier inconsistencies.
- Assessed missing information, timestamp limitations and data reliability.
- Documented data-quality issues affecting business interpretation.

### 2. Data Cleaning & Transformation

- Processed source datasets using Python and Pandas.
- Removed exact duplicate payment records according to the analytical methodology.
- Created structured datasets for downstream analysis.
- Developed aggregated outputs for KPI reporting.

### 3. SQL-Based Analysis

- Developed PostgreSQL analytical queries.
- Performed data aggregation and performance comparisons.
- Analysed payment and operational metrics.
- Supported structured reporting and analytical validation.

### 4. Recovery Performance Analysis

- Evaluated monthly gross successful payment values.
- Calculated month-on-month recovery trends.
- Compared observed performance with the reported growth benchmark.
- Examined operational data limitations affecting KPI interpretation.

### 5. Power BI Dashboard Development

Developed a Power BI dashboard to support:

- Collections and recovery performance monitoring
- Monthly recovery trend analysis
- KPI visualization
- Interactive exploration of analytical results
- Business performance reporting

## Data Quality & Analytical Limitations

Several important data-quality issues were identified:

- **Duplicate Payments:** Exact duplicate payment records could inflate reported gross payment values.
- **Payment References:** Reference collisions and incomplete reversal linkage restrict reliable net recovery calculations.
- **Identifier Consistency:** Borrower and agent identifier inconsistencies affect certain analytical comparisons.
- **Portfolio Denominators:** Current account snapshots may not accurately represent historical eligible portfolios.
- **Partial Data:** August records are incomplete and require cautious interpretation.
- **Operational Metrics:** Promise-to-pay status and call outcomes should not automatically be interpreted as verified cash recovery.

These limitations are documented to ensure transparent and defensible business conclusions.

## Business Recommendations

**Improve KPI Reliability**

Establish consistent definitions for gross payments, net settled recovery, payer rates and operational performance indicators.

**Strengthen Data Governance**

Improve payment reference integrity, reversal tracking and identifier consistency across source systems.

**Validate Collection Strategies**

Use randomized treatment and holdout groups to evaluate whether proposed collection strategies generate measurable incremental recovery.

**Enhance Performance Monitoring**

Develop reliable reporting processes and monitor operational effectiveness alongside customer complaints, consent requirements and disputes.

## Project Deliverables

- Python-based data analysis notebook
- PostgreSQL analytical SQL scripts
- Raw and transformed datasets
- Data-quality assessment and documentation
- Executive analysis memo
- Analytical figures and visualizations
- Interactive Power BI dashboard

## Skills Demonstrated

`Python` `SQL` `PostgreSQL` `Power BI` `Pandas` `NumPy` `Data Cleaning` `Exploratory Data Analysis` `Data Quality` `KPI Analysis` `Business Intelligence` `Data Visualization` `Business Analytics`

---

**Collections & Recovery Analytics — Data-driven insights for reliable performance measurement and informed business decision-making.**
