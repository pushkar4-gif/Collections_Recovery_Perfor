-- Run on each load; fail pipeline for key violations, warn for known unresolved source issues.
SELECT 'payment_null_id' test,COUNT(*) failures FROM raw.payments WHERE payment_id IS NULL UNION ALL SELECT 'payment_null_account',COUNT(*) FROM raw.payments WHERE account_id IS NULL UNION ALL SELECT 'payment_negative_amount',COUNT(*) FROM raw.payments WHERE amount::numeric < 0 UNION ALL SELECT 'orphan_payment_account',COUNT(*) FROM raw.payments p LEFT JOIN stg.accounts a USING(account_id) WHERE a.account_id IS NULL;
-- Duplicate IDs and non-unique business keys
SELECT payment_id,COUNT(*) n FROM raw.payments GROUP BY 1 HAVING COUNT(*)>1;
SELECT call_id,COUNT(*) n FROM raw.calls GROUP BY 1 HAVING COUNT(*)>1;
SELECT payment_reference,COUNT(DISTINCT account_id) accounts,COUNT(DISTINCT amount) amounts,COUNT(DISTINCT payment_status) statuses FROM raw.payments WHERE payment_reference IS NOT NULL GROUP BY 1 HAVING COUNT(*)>1;
-- Date coverage and invalid event timestamps
SELECT COUNT(*) FILTER(WHERE event_at IS NULL) null_event_at FROM raw.payments;
-- Alert if daily source volume changes > 3 standard deviations from trailing 28-day mean (illustrative).
WITH d AS (SELECT event_at::date dt,COUNT(*) n FROM raw.payments GROUP BY 1), x AS (SELECT dt,n,AVG(n) OVER(ORDER BY dt ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING) mu,STDDEV_POP(n) OVER(ORDER BY dt ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING) sd FROM d) SELECT * FROM x WHERE sd>0 AND ABS(n-mu)>3*sd;
