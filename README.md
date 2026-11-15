Collections & Recovery Analytics
An end-to-end data analytics project investigating collections and recovery performance using Python, SQL and Power BI.
Project Overview
This project analyses collections-related datasets to evaluate payment performance, identify data-quality issues, track recovery trends and develop actionable business recommendations.

The central business question is whether the reported 11% month-on-month improvement can be supported by the available payment data.
Key Finding
After removing exact duplicate payment records:
- June 2026 gross successful payments: approximately ₹17.59 Cr
- July 2026 gross successful payments: approximately ₹18.72 Cr
- July month-on-month growth: 6.48%
The analysis therefore does not reproduce the reported 11% improvement using this payment-based calculation.

Note: These figures represent gross successful payment value, not net settled cash. Payment reference collisions and insufficient reversal linkage limit the ability to calculate reliable net recovery.
Tools & Technologies
- Python: Data cleaning, preprocessing, exploratory analysis and KPI calculations
- SQL (PostgreSQL): Data querying, aggregation and analytical transformations
- Power BI: Interactive dashboard and performance monitoring
- Pandas & NumPy: Data manipulation and analysis
- Jupyter Notebook / Google Colab: Analysis workflow and documentation
Project Structure
Collections_Recovery_Perfor/
│
├── data/
│   ├── raw/                  # Original assignment datasets
│   └── golden/               # Cleaned and aggregated datasets
│
├── notebooks/
│   └── Collections_Analytics_Colab.ipynb
│
├── sql/                      # PostgreSQL analytical scripts
│
├── src/
│   └── build_analysis.py
│
├── reports/
│   ├── executive_memo.pdf
│   ├── executive_memo.md
│   ├── data_quality_report.md
│   └── assignment_brief.pdf
│
├── figures/                  # Analytical charts and visuals
│
├── Collections_Recovery_Performance_Dashboard_Pushkar.pbix
│
├── README.md
└── SUBMISSION_CONTENTS.txt
Analytical Workflow
1. Data Understanding: Reviewed the supplied datasets and identified their structure and limitations.
2. Data Quality Assessment: Examined duplicates, missing values, identifier inconsistencies and timestamp issues.
3. Data Preparation: Cleaned and transformed source data using Python.
4. SQL Analysis: Developed SQL scripts for querying, aggregating and analysing collections performance.
5. KPI Analysis: Evaluated successful payment values and month-on-month trends.
6. Dashboard Development: Created a Power BI dashboard for monitoring collections and recovery performance.
7. Business Recommendations: Documented findings, limitations and potential next steps.
Important Data Limitations
- Payment reference collisions prevent reliable reversal-to-payment matching.
- Gross successful payment value should not be interpreted as net settled cash.
- Account-level joins are preferred over unreliable borrower identifiers in event records.
- The agent dataset contains identifier inconsistencies, limiting agent-level productivity conclusions.
- August data is partial and should be interpreted cautiously.
- PTP kept status is not independently verified cash recovery.
- The analysis does not establish causal impact of campaigns or collection channels.
Business Recommendations
- Introduce a randomized treatment and holdout pilot to measure the impact of collection strategies.
- Track net settled cash using reliable payment and reversal linkage.
- Improve consistency of account, borrower and agent identifiers.
- Monitor customer consent, disputes, complaints and DND compliance.
- Use clearly defined and auditable KPIs for recovery performance
