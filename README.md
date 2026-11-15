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
