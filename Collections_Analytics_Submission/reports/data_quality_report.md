DATA QUALITY CHECKS AND FINDINGS

Project: Collections analytics challenge  
Source: 17 supplied CSV tables, `data_dictionary.csv`, README and assignment PDF  
Analysis date: 15 November 2026  
Scope: Full forensic review of the supplied extract; descriptive conclusions only where the source supports them.

1. Executive assessment

Using the payment-based calculation in this project, I could not reproduce the reported 11% month-on-month improvement. After removing exact full-row duplicate payment records, July 2026 gross successful payment value is **₹18.7248 Cr**, versus **₹17.5853 Cr** in June: **+6.48% MoM**. July is only **+0.01%** above January. The 11% claim cannot be accepted or definitively disproved until the business supplies its exact numerator, denominator, netting rules, attribution window and comparison period.

I have moderate confidence for the descriptive gross-successful-payment totals after exact-row deduplication; low for net cash recovery, borrower-level conversion, agent productivity, channel/campaign attribution and causal explanation. The event extract is not a complete 12-month history.

2. Source inventory and temporal coverage

All 17 supplied CSV datasets were loaded and profiled. The complete table-level counts and missingness are in `data/golden/dataset_quality_profile.csv`; timestamp field ranges are in `data/golden/timestamp_coverage.csv`.

| Dataset | Rows | Exact duplicate rows | Missing cells |
|---|---:|---:|---:|
| accounts | 30,000 | 0 | 455 |
| borrowers | 30,600 | 600 | 1,509 |
| agents | 30,000 | 0 | 0 |
| agent_sessions | 15,000 | 0 | 0 |
| campaigns | 120 | 0 | 0 |
| daily_targeting | 45,000 | 0 | 0 |
| calls | 91,350 | 1,271 | 1,827 |
| call_attempts | 120,000 | 0 | 2,400 |
| call_dispositions | 35,000 | 0 | 0 |
| whatsapp_events | 60,600 | 600 | 0 |
| sms_events | 45,000 | 0 | 0 |
| field_visits | 25,000 | 0 | 250 |
| promises_to_pay | 18,000 | 0 | 0 |
| payments | 25,500 | 486 | 382 |
| vendor_telephony | 15 | 0 | 0 |
| complaints | 8,000 | 0 | 0 |
| account_status_history | 60,000 | 0 | 0 |

Main event streams generally run **1 Jan–8 Aug 2026**. Calls have one early outlying record dated **29 Dec 2025** and extend to **12 Aug 2026**; other major event streams extend through 8 Aug. August is partial and excluded from full-month MoM comparisons. `complaints.resolution_at` extends to 26 Aug and `promises_to_pay.promised_date` to 6 Sep; these are resolution/maturity dates, not additional collection-event coverage. `agent_sessions.logout_at` extends to 9 Aug.

Source timestamp strings include UTC, Asia/Kolkata and Asia/Dubai indicators/fields in different tables, while event timestamp semantics are not consistently documented. For calendar-month summaries, the pipeline parses source strings without asserting timezone localization. Hour-of-day/day-of-week analysis is intentionally withheld pending source-system timezone documentation and offset-aware event timestamps.

3. Identity and entity resolution

| Event dataset | Matched account rows | Orphan account rows | Borrower-ID mismatch among matched rows |
|---|---:|---:|---:|
| payments | 25,114 | 386 | 100.00% |
| calls | 89,947 | 1,403 | 99.99% |
| call_attempts | 118,137 | 1,863 | 99.99% |
| call_dispositions | 34,476 | 524 | 99.99% |
| SMS | 44,267 | 733 | 99.99% |
| WhatsApp | 59,677 | 923 | 99.99% |
| field_visits | 24,623 | 377 | 99.99% |
| promises_to_pay | 17,707 | 293 | 99.99% |
| complaints | 7,893 | 107 | 99.99% |
| account_status_history | 59,038 | 962 | 99.99% |

**Decision:** Use `account_id` as the event-to-account join key, and use the borrower ID from the account master only as the current snapshot borrower attribute. Do not join event borrower IDs to the borrower master or make person-level claims. These widespread mismatches suggest synthetic/inconsistent identifiers or a missing crosswalk; they do not establish that all underlying people are genuinely different.

The agents table contains 30,000 rows but only 1,000 distinct `agent_id` values and 1,099 distinct employee codes. Repeated `agent_id` values map to multiple employee codes, names, vendors and teams. Agent tenure, agent rankings, and recovery per agent-hour are therefore not reliable until an effective-dated employee/agent crosswalk is supplied.

The borrowers table has 600 exact duplicate rows and 30,600 rows against 11,015 distinct borrower IDs. It should not be used as a one-row-per-person dimension without an explicit survivorship rule and stable identity key.

4. Payment forensics and recovery metric

CLEANING AND DEFINITION

- Raw payments: 25,500 rows.
- Exact full-row duplicates: **486 (1.91%)**.
- Successful exact-duplicate rows removed: **335**, representing **₹2.5011 Cr** of repeated gross successful value in the raw extract.
- Missing payment references: **382** rows after exact-row deduplication.
- Payment references are repeated and collide across accounts, amounts and statuses; reference alone is not a safe unique transaction key.
- Recovery numerator: sum of positive `amount` for rows with `payment_status='SUCCESS'`, after exact full-row deduplication.
- `FAILED`, `PENDING` and `REVERSED` are excluded from the gross-success numerator. Reversed amounts are shown separately, not netted, because original/reversal linkage is not reliable.

The ₹2.5011 Cr duplicate amount is a data-cleaning adjustment in this extract, **not proof** that the same value was incorrectly recognized in the company's finance ledger. Processor settlement reconciliation is required.

MONTHLY RESULTS

| Month | Gross successful payments | MoM change | Payer rate on 30k snapshot |
|---|---:|---:|---:|
| Jan | ₹18.7229 Cr | — | 7.91% |
| Feb | ₹17.0280 Cr | -9.05% | 7.24% |
| Mar | ₹18.9190 Cr | +11.10% | 8.06% |
| Apr | ₹17.5229 Cr | -7.34% | 7.68% |
| May | ₹18.4335 Cr | +5.20% | 7.81% |
| Jun | ₹17.5853 Cr | -4.60% | 7.62% |
| Jul | ₹18.7248 Cr | **+6.48%** | 7.78% |
| Aug (partial) | ₹4.7110 Cr | Not comparable | 2.03% |

The denominator is the 30,000-account current master snapshot, not an effective-dated historical eligible/active portfolio. Payer rate and recovery/account are consequently snapshot-denominator proxies.

5. Operational and channel forensics

CALLS, ATTEMPTS AND DISPOSITIONS

`calls` contains 91,350 rows and 1,271 exact duplicate rows; call IDs repeat. `call_attempts` contains 120,000 rows and 2,400 missing cells. `call_dispositions` has legacy, v1 and v2 disposition versions, with both `PTP` and `PROMISE_TO_PAY` codes. A versioned mapping table is required before comparing contact/PTP trends. `ANSWERED` is not a right-party contact (RPC) flag; RPC cannot be measured reliably from this source alone.

SMS AND WHATSAPP

SMS has SENT, DELIVERED, CLICKED and FAILED events. WhatsApp has SENT, DELIVERED, READ, REPLIED, PAYMENT_CLICK and FAILED events; 600 exact duplicate WhatsApp rows are present. Raw event counts are not unique recipients or conversion rates. Message lifecycle deduplication, delivery receipts, account identity resolution and a pre-defined click-to-settlement attribution window are needed.

PTP

PTP records contain KEPT, BROKEN, OPEN and CANCELLED statuses. A defensible matured PTP kept rate is `KEPT / (KEPT + BROKEN)`, with OPEN excluded and cancellation treatment specified. A cash-kept metric must link payments to a promise and promised date. The supplied status alone is a descriptive status, not verified cash realization.

FIELD VISITS

Field visit outcomes include CONTACTED, NOT_AVAILABLE, PAID, PTP, REFUSED and WRONG_ADDRESS. These are operational visit outcomes; PAID/ PTP should not be treated as settled payment or kept promise without linking to the payment/PTP ledger. No causal field-versus-digital comparison is identified.

CAMPAIGNS AND TARGETING

Daily targeting's `recommended_channel` does not consistently match the campaign table's `channel`; campaign definitions also include `MIXED` and multiple strategy versions. A campaign label is not proof of actual channel delivery. There is no trustworthy treatment-exposure-to-payment bridge.

VENDOR AND AGENT SESSIONS

Vendor outcomes are descriptive only. Vendor mapping/schema versions and agent identity conflicts prevent clean vendor/agent causal comparisons. Session login/logout arithmetic should not be equated with productive paid hours without validating overnight sessions, timezone, breaks and session/device identifiers.

COMPLAINTS AND ACCOUNT STATUS

Complaints include harassment, privacy, DND, agent behaviour and dispute categories. These must be treated as collection-policy guardrails, not merely operational metrics. Account status history includes both event time and recorded time; use event time for effective status and recorded time to measure ingestion lag, while preserving both fields.

6. Statistical investigation: what is identified

| Threat | Current assessment |
|---|---|
| Portfolio mix | Current risk/DPD snapshot can describe associations, but cannot reconstruct historical mix. |
| Cohort effects | Account origination cohorts can be explored; historical eligibility/status still needs validation. |
| Selection bias | Targeted accounts are not compared with a complete eligible population; targeted-vs-untargeted lift is biased. |
| Survivorship bias | Current account snapshot may omit closed/removed accounts; historical denominator is unavailable. |
| Simpson's paradox | Cannot reliably test using non-effective-dated current segment labels. |
| Attribution-window bias | No validated interaction-to-payment mapping/window; channel credit is not estimable. |
| Time-series effects | Seven complete monthly observations (Jan–Jul) support description, not robust seasonality or causal break inference. |

No causal conclusion is drawn from observed correlations. The full notebook includes segment, DPD, channel event, PTP, field, complaint, status-history and vendor descriptive tables.

7. Golden dataset decisions and exclusions

`data/golden/account_month_golden.csv` creates a 30,000-account snapshot crossed with observed payment months, then attaches account-month targeting and successful payments. It contains 240,000 rows for eight observed months, including partial August. It is an account-month analytical scaffold, **not** a historical snapshot of active accounts or balances. Risk/DPD/status attributes are current master values and must not be interpreted as historically effective values.

| Decision | Treatment | Business impact |
|---|---|---|
| Exact duplicate payments | Remove exact full-row duplicates only | Avoid repeated event rows; 335 successful duplicate rows / ₹2.5011 Cr removed |
| Reference collisions | Retain; publish collision audit | Avoid deleting potentially valid payments |
| Reversals | Report separately; do not net | Gross recovery is not net settled cash |
| Borrower ID mismatch | Join on account_id; quarantine person-level analysis | Prevent false borrower joins |
| Orphan account events | Retain in raw; exclude from account-level golden joins and report count | Account-level event totals may not equal raw event totals |
| Mixed timezone semantics | Preserve raw source timestamp; no local-hour conclusions | Avoid misclassifying calling hour/day |
| Static account denominator | Label snapshot proxy | Payer rate not historical portfolio penetration |
| Campaign/channel mismatch | Keep recommendation and campaign channel separately | No channel causal attribution |
| Agent identity collisions | No agent ranking or agent-hour metric | Productivity and tenure not estimable |

8. Metric definitions and availability

| Metric | Definition | Status |
|---|---|---|
| Gross recovery | Positive successful payment amounts after exact-row dedup | Available |
| Net recovery | Settled successful cash less linked reversals/refunds | Not estimable reliably |
| Payer rate | Unique paying account IDs / current 30k snapshot | Proxy available |
| Contact rate | Unique eligible accounts with a verified contact / eligible accounts | Not estimable; answered calls are only a call-level proxy |
| RPC | Verified right-party contacts / eligible accounts or attempts | Not estimable |
| PTP rate | Valid PTPs / verified RPCs | Not estimable consistently; disposition versions differ |
| PTP kept rate | Matured KEPT / (KEPT + BROKEN), then validate payment | Status proxy available; cash-kept not verified |
| Recovery/account | Gross recovery / historically eligible accounts | Snapshot proxy only |
| Recovery/agent-hour | Net recovery / validated productive paid hours | Not estimable |
| Cost per ₹ recovered | Fully loaded channel cost / net recovery | Not estimable; costs absent |
| Channel conversion | Attributed net payer accounts / unique delivered eligible accounts | Not estimable; exposure and attribution missing |

9. Production controls and recommended next steps

1. Require unique source event IDs, ingestion batch IDs, source file, ingestion timestamp and schema version.
2. Obtain processor transaction ID, idempotency key, settlement state, original-payment link and reversal/refund link.
3. Build effective-dated account↔borrower and employee↔agent crosswalks; reject ambiguous joins from golden marts.
4. Store event timestamp in UTC plus original timezone/offset and source timestamp; define event-time versus recorded-time semantics.
5. Maintain historical daily/month-end account eligibility, balance, DPD, risk and status snapshots.
6. Version campaign definitions and disposition mappings; log actual channel exposure and provider delivery lifecycle.
7. Build matured PTP and payment matching with pre-registered attribution windows.
8. Add DND, consent, dispute and complaint suppression guardrails to targeting.
9. Monitor duplicates, null keys, orphan rates, identity mismatches, late-arrival lag, daily volume anomalies, schema drift and reconciliation variance.
10. Backfill from immutable raw events using deterministic event keys and documented restatement policy.

10. Reproducibility

- Run `python src/build_analysis.py` from the repository root to rebuild the generated audit and golden outputs.
- Run all cells in `notebooks/collections_analysis.ipynb` for the end-to-end analytical investigation and exported notebook tables.
- SQL files are PostgreSQL-style reference SQL; raw table loading and column types must be established according to the data contracts before execution.
