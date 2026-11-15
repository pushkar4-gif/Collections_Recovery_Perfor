-- PostgreSQL reference layer. Create raw_* tables using source CSV headers and text-safe ingestion.
-- Never cast source identifiers to integers. Preserve raw payloads and ingestion metadata.
CREATE SCHEMA IF NOT EXISTS raw; CREATE SCHEMA IF NOT EXISTS stg; CREATE SCHEMA IF NOT EXISTS clean; CREATE SCHEMA IF NOT EXISTS mart;
-- Expected raw tables: accounts, borrowers, agents, agent_sessions, campaigns, daily_targeting,
-- calls, call_attempts, call_dispositions, whatsapp_events, sms_events, field_visits,
-- promises_to_pay, payments, vendor_telephony, complaints, account_status_history.
-- Add ingestion_batch_id, source_file, ingested_at to every production landing table.
