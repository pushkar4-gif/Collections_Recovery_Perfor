-- Exact-row dedupe only. A payment_reference collision is a review queue, not a dedupe key.
CREATE OR REPLACE VIEW clean.payments_exact_dedup AS SELECT DISTINCT * FROM stg.payments;
CREATE OR REPLACE VIEW clean.successful_payment_events AS SELECT * FROM clean.payments_exact_dedup WHERE payment_status='SUCCESS' AND amount > 0;
CREATE OR REPLACE VIEW clean.payment_reference_collisions AS SELECT payment_reference, COUNT(*) row_count, COUNT(DISTINCT account_id) accounts, COUNT(DISTINCT amount) amounts, COUNT(DISTINCT payment_status) statuses FROM clean.payments_exact_dedup WHERE payment_reference IS NOT NULL GROUP BY payment_reference HAVING COUNT(*)>1;
CREATE OR REPLACE VIEW clean.payment_reversal_review AS SELECT s.account_id,s.payment_id,s.payment_reference,s.event_at_source,s.amount success_amount, r.payment_id reversal_payment_id,r.event_at_source reversal_at,r.amount reversal_amount FROM clean.successful_payment_events s LEFT JOIN clean.payments_exact_dedup r ON r.payment_reference=s.payment_reference AND r.payment_status='REVERSED' AND r.account_id=s.account_id;
-- Do not net reversals until processor transaction IDs and reversal linkage are verified.
