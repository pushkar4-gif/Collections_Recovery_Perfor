-- Snapshot segment/DPD associations; account DPD is not historized at month grain in the account master.
SELECT risk_segment,dpd,COUNT(*) accounts,COUNT(*) FILTER(WHERE payer_flag=1) payers,SUM(gross_success_inr) gross_recovery_inr FROM mart.golden_account_month GROUP BY 1,2;
-- Status history: use event time for effective state, recorded_at for ingestion-lag analysis.
SELECT status,source,COUNT(*) events,COUNT(DISTINCT account_id) accounts,AVG(EXTRACT(EPOCH FROM(recorded_at::timestamp-event_at::timestamp))/3600) avg_recording_lag_hours FROM raw.account_status_history GROUP BY 1,2;
-- Complaint safety guardrails
SELECT complaint_type,severity,status,COUNT(*) complaints FROM raw.complaints GROUP BY 1,2,3;
