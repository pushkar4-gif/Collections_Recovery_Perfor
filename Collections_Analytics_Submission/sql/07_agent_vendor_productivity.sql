-- Agent identity is not stable in supplied snapshot; use only as anomaly audit until crosswalk exists.
SELECT agent_id,COUNT(*) rows,COUNT(DISTINCT employee_code) employee_codes,COUNT(DISTINCT agent_name) names,COUNT(DISTINCT vendor_id) vendors FROM raw.agents GROUP BY 1 HAVING COUNT(DISTINCT employee_code)>1 OR COUNT(DISTINCT agent_name)>1 OR COUNT(DISTINCT vendor_id)>1;
-- Vendor outcomes are descriptive. Do not compare rates without normalized timezone, stable vendor mapping and traffic mix.
SELECT c.vendor_id,v.vendor_name,UPPER(c.call_status) call_status,COUNT(*) call_rows,COUNT(DISTINCT c.call_id) call_ids,AVG(NULLIF(c.duration_sec,0)) avg_duration_sec FROM raw.calls c LEFT JOIN raw.vendor_telephony v USING(vendor_id) GROUP BY 1,2,3 ORDER BY 1,3;
-- Session duration is source-time arithmetic only; investigate negative/overlong sessions before use.
SELECT channel,COUNT(*) sessions,COUNT(*) FILTER(WHERE logout_at::timestamp < login_at::timestamp) negative_sessions,AVG(EXTRACT(EPOCH FROM(logout_at::timestamp-login_at::timestamp))/3600) avg_session_hours FROM raw.agent_sessions GROUP BY 1;
