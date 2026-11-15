-- Event mix by channel. These are events, not unique reached borrowers or incremental recovery.
SELECT 'SMS' channel,UPPER(event_type) event_type,COUNT(*) events,COUNT(DISTINCT account_id) accounts FROM raw.sms_events GROUP BY 1,2 UNION ALL SELECT 'WHATSAPP',UPPER(event_type),COUNT(*),COUNT(DISTINCT account_id) FROM raw.whatsapp_events GROUP BY 1,2;
-- Campaign definitions and targeting recommendations are not equivalent; inspect mismatches.
SELECT t.recommended_channel,c.channel campaign_channel,c.strategy_version,COUNT(*) target_rows FROM stg.targeting t LEFT JOIN raw.campaigns c USING(campaign_id) GROUP BY 1,2,3 ORDER BY 1,2,3;
-- Field outcomes: descriptive operational output only, not causal channel conversion.
SELECT UPPER(visit_type) visit_type,UPPER(outcome) outcome,COUNT(*) visits,COUNT(DISTINCT account_id) accounts FROM raw.field_visits GROUP BY 1,2;
