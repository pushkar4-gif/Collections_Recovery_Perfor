COLLECTIONS PERFORMANCE REVIEW

To: Hiring Team / Leadership
From: Data Analyst Assignment
Date: 15 November 2026
Subject: Checking the reported 11% recovery improvement

SUMMARY

I checked the reported 11% month-on-month improvement using the payment records supplied with the assignment. With my definition of recovery, July is up 6.48% from June, not 11%. July is almost flat compared with January. This does not prove that the company report is wrong, because I do not have its exact KPI formula or finance reconciliation. It means I could not reproduce the 11% using the available data.

WHAT I CALCULATED

I counted positive payment amounts where payment_status is SUCCESS and removed exact full-row duplicates first. This gives around Rs 18.72 Cr for July and Rs 17.59 Cr for June. There were 25,500 payment rows in the raw file. I found 486 exact duplicate rows, including 335 successful rows with about Rs 2.50 Cr of repeated value in the extract.

I have called this gross successful payment value. I have not called it net recovery because the payment references repeat across accounts, amounts and statuses. I could not confidently connect every reversal to its original payment. The payer-rate calculation also uses the current 30,000-account master file, so it is only a rough comparison and not a historical eligible-account rate.

WHAT MAY EXPLAIN THE CHANGE

The data does not let me identify one operational reason for the July movement. Borrower IDs in event files do not agree with the account master on matched records. Agent identifiers also have conflicts. Campaign channel and recommended channel do not always match, and timestamp timezone details are incomplete. These issues make it unsafe to say that a particular agent, vendor, campaign or channel caused the increase.

There are useful descriptive tables for calls, SMS, WhatsApp, PTPs, field visits, complaints, account status and vendor outcomes in the notebook. However, event counts should not be treated as unique borrower conversions. For example, an answered call is not automatically a right-party contact, and a PTP marked kept is not proof of settled cash unless it is linked to a payment.

HOW MUCH CONFIDENCE I HAVE

I have moderate confidence in the gross successful-payment trend after removing exact duplicate rows. Confidence is low for net cash recovery, historical payer rate, borrower-level conversion, channel attribution and agent productivity. The main event data is mostly from January to 8 August 2026, with calls extending to 12 August. August is partial, so I have not used it for full-month comparisons.

WHAT I WOULD DO NEXT

I would not recommend spending the full Rs 10 Cr immediately. I would first run a small randomized targeting pilot. Accounts should be split into treatment and holdout groups, with similar DPD, risk segment, loan type and geography. Actual messages, calls and visits should be logged, and the result should be measured using incremental net settled cash over agreed 30, 60 and 90 day periods.

DND, consent, disputes and complaints should be monitored as guardrails. If the test shows a clear improvement without worsening these measures, the company can consider scaling it.

SIMPLE FINANCIAL SCENARIO

Average gross recovery from January to July is about Rs 18.13 Cr per month. If a pilot eventually produced a 1% uplift, that would be about Rs 18.13 lakh per month, or Rs 2.18 Cr over a year before ongoing costs. On an illustrative Rs 1 Cr pilot cost, simple gross payback would be around 5.5 months. At 0.5% uplift it would be around 11 months, and at zero uplift the cost would not be recovered.

These are only scenarios. The uplift has not been measured and the cost is not a vendor quote. Ongoing platform, messaging, staffing and compliance costs are not included. I would release more funding only after the pilot result is measured.

DATA NEEDED TO IMPROVE THE ANALYSIS

The most useful additions would be processor transaction IDs and reversal links, historical account balances and DPD, a reliable account-to-borrower mapping, an effective-dated agent mapping, timezone-aware event timestamps, actual channel delivery records, and channel costs and paid agent hours.
