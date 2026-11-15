SQL REPOSITORY - POSTGRESQL

Suggested run order

1. 00_source_contracts.sql - create schemas and note the raw table structure.
2. Load the supplied CSV files into raw tables. Keep source IDs as text at first.
3. 01_staging_and_normalization.sql - trim IDs and standardize status fields.
4. 02_payment_reconciliation.sql - remove exact duplicate rows and review reversals.
5. 03_identity_resolution.sql - check account and agent ID mapping issues.
6. 04_golden_account_month.sql - create the account-month analysis table.
7. 05_metrics_recovery_and_funnel.sql - calculate payment, call and PTP measures.
8. 06_channel_campaign_analysis.sql - review digital events, campaigns and field visits.
9. 07_agent_vendor_productivity.sql - review agent, vendor and session data.
10. 08_risk_dpd_cohort_and_status.sql - review risk, DPD, status history and complaints.
11. 09_data_quality_tests.sql - run duplicate, missing key, orphan and date checks.

A few notes before running

- The scripts use PostgreSQL syntax. They are a starting point and not a complete database deployment. Raw tables need to be created and loaded first.
- The timestamp fields are not localized in the scripts because the source timezone details are not clear.
- The accounts table is a current snapshot, so it should not be used as a historical active-account denominator.
- Payment references repeat. Do not deduplicate using payment reference alone. Reversal netting needs a reliable processor transaction link.
- Agent identities are not clean enough for agent rankings or recovery per agent-hour.
- Contact rate, RPC and channel attribution need verified person IDs, right-party flags and actual channel exposure records.
