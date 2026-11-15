COLLECTIONS ANALYTICS ASSIGNMENT

This project looks at the collections data shared for the Data Analyst assignment. The main question was whether the reported 11% month-on-month improvement can be seen in the payment data.

My calculation shows July 2026 gross successful payments of about Rs 18.72 Cr, compared with Rs 17.59 Cr in June. That is an increase of 6.48%. July is almost the same as January. So, using this calculation, I could not match the reported 11% figure.

This number needs to be read carefully. It is gross successful payment value after removing exact duplicate rows. It is not net settled cash, because the payment reference field has collisions and reversals cannot be linked back to original payments with enough confidence.

FILES IN THIS PROJECT

- notebooks/ contains the Google Colab notebook. Run it from the first cell onwards.
- sql/ contains the SQL scripts. The README inside that folder gives the suggested run order.
- src/ contains the Python script used to create the analysis outputs.
- data/raw/ contains the original files supplied with the assignment. These have been kept unchanged.
- data/golden/ contains cleaned and summarized outputs used in the analysis.
- reports/ contains the data quality report, executive memo and assignment brief.
- figures/ contains the charts used in the report.

HOW TO RUN

For Colab, upload the project ZIP when the first notebook cell asks for it. The notebook extracts the files and then runs the analysis. For local use, install the packages in requirements.txt and run `python src/build_analysis.py` from the project folder.

The SQL is written mainly for PostgreSQL. Table loading and data types need to be set up before running the scripts.

LIMITATIONS I RAN INTO

The main event data is mostly from January to 8 August 2026. Calls go up to 12 August, and August is incomplete. I used January to July for full-month comparisons.

Borrower IDs in event tables do not agree with the account master in many matched records, so I used account_id for account-level joins. I have not made borrower-level claims from these joins. Agent IDs also appear under more than one employee identity, so agent rankings and recovery per agent-hour are not reliable.

Payment references are repeated. I removed exact duplicate rows, but did not remove rows just because they shared a reference. The account master is a current snapshot, not a historical month-end portfolio. Timezone details are also incomplete, so I have not made strong claims about best calling hours.

The investment figures are examples for thinking about the decision. They are not measured uplift or confirmed vendor costs. A controlled pilot would be needed before spending the full amount.
