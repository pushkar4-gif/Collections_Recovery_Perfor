from pathlib import Path
import pandas as pd, numpy as np, json, textwrap, os
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw'; G=ROOT/'data/golden'; R=ROOT/'reports'; SQL=ROOT/'sql'; NB=ROOT/'notebooks'
G.mkdir(exist_ok=True); R.mkdir(exist_ok=True); SQL.mkdir(exist_ok=True)
files={p.stem:pd.read_csv(p) for p in RAW.glob('*.csv')}
# robust timestamp parsing: preserve source values and create UTC only when offset-aware; naive times stay naive
# Audit per source
audit=[]
for name,d in files.items():
    dup=int(d.duplicated().sum())
    missing=int(d.isna().sum().sum())
    audit.append({'dataset':name,'rows':len(d),'columns':len(d.columns),'exact_duplicate_rows':dup,'missing_cells':missing,'missing_pct':round(missing/(len(d)*len(d.columns))*100,3) if len(d) else 0})
pd.DataFrame(audit).to_csv(G/'dataset_quality_profile.csv',index=False)
# date ranges for timestamp-like cols
ranges=[]
for name,d in files.items():
 for c in d.columns:
  if any(x in c.lower() for x in ['_at','_date']):
   x=pd.to_datetime(d[c],errors='coerce',utc=True)
   if x.notna().any(): ranges.append({'dataset':name,'column':c,'valid_timestamps':int(x.notna().sum()),'min_utc':str(x.min()),'max_utc':str(x.max()),'invalid_or_missing':int(x.isna().sum())})
pd.DataFrame(ranges).to_csv(G/'timestamp_coverage.csv',index=False)
# Generic exact duplicate audit by all datasets
# Account master and event reconciliation
acc=files['accounts'].copy(); acc['account_id']=acc.account_id.astype(str)
identity=[]
for name,d in files.items():
 if 'account_id' in d and 'borrower_id' in d:
  j=d[['account_id','borrower_id']].copy(); j['account_id']=j.account_id.astype(str)
  m=j.merge(acc[['account_id','borrower_id']].rename(columns={'borrower_id':'master_borrower_id'}),on='account_id',how='left')
  valid=m.master_borrower_id.notna(); mismatch=valid & m.borrower_id.notna() & (m.borrower_id.astype(str)!=m.master_borrower_id.astype(str))
  identity.append({'dataset':name,'rows':len(d),'matched_account_rows':int(valid.sum()),'orphan_account_rows':int((~valid).sum()),'borrower_id_mismatch_rows':int(mismatch.sum()),'mismatch_pct_of_matched_nonnull':round(mismatch.sum()/max(1,(valid&m.borrower_id.notna()).sum())*100,2)})
pd.DataFrame(identity).to_csv(G/'identity_reconciliation.csv',index=False)
# payments exact dedup
pay=files['payments'].copy(); pay['event_at_parsed']=pd.to_datetime(pay.event_at,errors='coerce',utc=True)
pay_clean=pay.drop_duplicates().copy(); pay_clean['month']=pay_clean.event_at_parsed.dt.tz_convert(None).dt.to_period('M').astype(str)
pay_clean.to_csv(G/'payments_deduplicated_exact.csv',index=False)
# Monthly account snapshot denominator, gross successes/reversals separate
months=sorted(pay_clean.month.dropna().unique())
rows=[]
for m in months:
 p=pay_clean[pay_clean.month.eq(m)]; s=p[p.payment_status.astype(str).str.upper().eq('SUCCESS')]; rev=p[p.payment_status.astype(str).str.upper().eq('REVERSED')]
 rows.append({'month':m,'portfolio_accounts_snapshot':acc.account_id.nunique(),'successful_payment_rows':len(s),'successful_payment_ids_nunique':s.payment_id.nunique(),'paying_accounts':s.account_id.nunique(),'gross_success_inr':pd.to_numeric(s.amount,errors='coerce').sum(),'reversed_rows':len(rev),'reversed_amount_inr':pd.to_numeric(rev.amount,errors='coerce').sum(),'payer_rate_snapshot':s.account_id.nunique()/max(1,acc.account_id.nunique()),'gross_recovery_per_snapshot_account':pd.to_numeric(s.amount,errors='coerce').sum()/max(1,acc.account_id.nunique())})
monthly=pd.DataFrame(rows); monthly.to_csv(G/'monthly_metrics.csv',index=False)
# account-month dataset with observed payment months and targeting; explicit static snapshot attributes
acc_cols=['account_id','borrower_id','dpd','risk_segment','loan_type','outstanding_amount','principal_amount','status','timezone']
base=acc[[c for c in acc_cols if c in acc]].copy(); base['_k']=1
cal=pd.DataFrame({'month':months,'_k':1}); gold=base.merge(cal,on='_k').drop(columns='_k')
tgt=files['daily_targeting'].copy(); tgt['target_date_parsed']=pd.to_datetime(tgt.target_date,errors='coerce',utc=True); tgt['month']=tgt.target_date_parsed.dt.tz_convert(None).dt.to_period('M').astype(str)
tgagg=tgt.groupby(['account_id','month'],dropna=False).agg(target_records=('target_id','nunique'),campaigns_touched=('campaign_id','nunique'),max_priority=('priority','max'),recommended_channels=('recommended_channel','nunique')).reset_index()
pagg=pay_clean[pay_clean.payment_status.astype(str).str.upper().eq('SUCCESS')].groupby(['account_id','month']).agg(gross_recovery_inr=('amount','sum'),successful_payment_rows=('payment_id','size'),payment_ids=('payment_id','nunique')).reset_index()
gold=gold.merge(tgagg,on=['account_id','month'],how='left').merge(pagg,on=['account_id','month'],how='left')
for c in ['target_records','campaigns_touched','max_priority','recommended_channels','gross_recovery_inr','successful_payment_rows','payment_ids']: gold[c]=gold[c].fillna(0)
gold['targeted_flag']=(gold.target_records>0).astype(int); gold['payer_flag']=(gold.gross_recovery_inr>0).astype(int)
gold.to_csv(G/'account_month_golden.csv',index=False)
# reusable event summaries across channels
channel_specs=[('calls','call_status','calls'),('sms_events','event_type','sms'),('whatsapp_events','event_type','whatsapp'),('field_visits','outcome','field_visits'),('promises_to_pay','status','ptp'),('account_status_history','status','status_history'),('complaints','status','complaints')]
for name,col,prefix in channel_specs:
 d=files[name].copy(); ts=next((c for c in ['event_at','target_date','login_at'] if c in d),None)
 if ts:
  dt=pd.to_datetime(d[ts],errors='coerce',utc=True); d['month']=dt.dt.tz_convert(None).dt.to_period('M').astype(str)
 if col in d:
  tab=d.groupby([c for c in ['month',col] if c in d],dropna=False).size().rename('events').reset_index()
  tab.to_csv(G/f'{prefix}_event_mix.csv',index=False)
# Segment and DPD metrics: current snapshot associations only, not causal historical effects
seg=gold.groupby(['risk_segment','month']).agg(accounts=('account_id','nunique'),targeted_accounts=('targeted_flag','sum'),payers=('payer_flag','sum'),gross_recovery_inr=('gross_recovery_inr','sum')).reset_index(); seg['payer_rate_snapshot']=seg.payers/seg.accounts.replace(0,np.nan); seg.to_csv(G/'risk_segment_metrics.csv',index=False)
dpd=gold.copy(); dpd['dpd_band']=pd.cut(pd.to_numeric(dpd.dpd,errors='coerce'),[-1,0,30,60,90,180,365,100000],labels=['Current','1-30','31-60','61-90','91-180','181-365','365+'])
dpm=dpd.groupby(['dpd_band','month'],observed=False).agg(accounts=('account_id','nunique'),payers=('payer_flag','sum'),gross_recovery_inr=('gross_recovery_inr','sum')).reset_index(); dpm['payer_rate_snapshot']=dpm.payers/dpm.accounts.replace(0,np.nan); dpm.to_csv(G/'dpd_metrics.csv',index=False)
# PTP kept rates and amount totals
ptp=files['promises_to_pay'].copy(); ptp['promised_amount']=pd.to_numeric(ptp.promised_amount,errors='coerce'); ptp['event_dt']=pd.to_datetime(ptp.event_at,errors='coerce',utc=True); ptp['month']=ptp.event_dt.dt.tz_convert(None).dt.to_period('M').astype(str)
ptpm=ptp.groupby(['month','status'],dropna=False).agg(ptp_records=('ptp_id','nunique'),promised_amount=('promised_amount','sum')).reset_index(); ptpm.to_csv(G/'ptp_monthly_status.csv',index=False)
# Calls outcomes and call attempt funnel
calls=files['calls'].copy(); calls['event_dt']=pd.to_datetime(calls.event_at,errors='coerce',utc=True); calls['month']=calls.event_dt.dt.tz_convert(None).dt.to_period('M').astype(str)
callm=calls.groupby(['month','call_status'],dropna=False).agg(call_rows=('call_id','size'),unique_call_ids=('call_id','nunique'),accounts=('account_id','nunique'),duration_sec=('duration_sec','sum')).reset_index(); callm.to_csv(G/'call_monthly_outcomes.csv',index=False)
at=files['call_attempts'].copy(); at['event_dt']=pd.to_datetime(at.event_at,errors='coerce',utc=True); at['month']=at.event_dt.dt.tz_convert(None).dt.to_period('M').astype(str)
at.groupby(['month','attempt_status'],dropna=False).size().rename('attempts').reset_index().to_csv(G/'call_attempt_monthly_outcomes.csv',index=False)
# digital funnel event mixes
for name in ['sms_events','whatsapp_events']:
 d=files[name].copy(); d['event_dt']=pd.to_datetime(d.event_at,errors='coerce',utc=True); d['month']=d.event_dt.dt.tz_convert(None).dt.to_period('M').astype(str)
 d.groupby(['month','event_type'],dropna=False).agg(events=(d.columns[0],'size'),accounts=('account_id','nunique')).reset_index().to_csv(G/f'{name}_monthly_funnel.csv',index=False)
# targeting/campaign/vendor mix
for name,cols in [('daily_targeting',['recommended_channel','status','priority']),('campaigns',['channel','strategy_version','target_definition']),('calls',['vendor_id','call_status']),('agent_sessions',['channel'])]:
 d=files[name].copy(); d.to_csv(G/f'{name}_source_extract.csv',index=False) if name=='campaigns' else None
# agent ID audit
ag=files['agents']; ag.groupby('agent_id').agg(rows=('agent_id','size'),employee_codes=('employee_code','nunique'),names=('agent_name','nunique'),vendors=('vendor_id','nunique'),teams=('team','nunique')).reset_index().to_csv(G/'agent_identity_audit.csv',index=False)
# campaign join quality
camp=files['campaigns']; target_campaign=tgt.merge(camp[['campaign_id','channel','strategy_version','target_definition']],on='campaign_id',how='left',suffixes=('_target','_campaign'))
target_campaign.groupby(['recommended_channel','channel'],dropna=False).size().rename('target_rows').reset_index().to_csv(G/'campaign_channel_crosswalk.csv',index=False)
# complaint severity/status & resolution latency
co=files['complaints'].copy(); co['event_dt']=pd.to_datetime(co.event_at,errors='coerce',utc=True); co['resolution_dt']=pd.to_datetime(co.resolution_at,errors='coerce',utc=True); co['resolution_hours']=(co.resolution_dt-co.event_dt).dt.total_seconds()/3600
co.groupby(['complaint_type','severity','status'],dropna=False).agg(complaints=('complaint_id','nunique'),median_resolution_hours=('resolution_hours','median')).reset_index().to_csv(G/'complaint_analysis.csv',index=False)
# field visit outcomes
fv=files['field_visits']; fv.groupby(['visit_type','outcome'],dropna=False).agg(visits=('visit_id','nunique'),accounts=('account_id','nunique')).reset_index().to_csv(G/'field_visit_outcomes.csv',index=False)
# vendor performance descriptive only
v=files['vendor_telephony']; calls_v=calls.merge(v[['vendor_id','vendor_name','schema_version']],on='vendor_id',how='left')
calls_v.groupby(['vendor_name','schema_version','call_status'],dropna=False).agg(call_rows=('call_id','size'),unique_calls=('call_id','nunique'),accounts=('account_id','nunique')).reset_index().to_csv(G/'vendor_call_outcomes.csv',index=False)
# summary stats helpers
summary={}
summary['rows']={k:len(v) for k,v in files.items()}
summary['exact_duplicates']={k:int(v.duplicated().sum()) for k,v in files.items()}
summary['monthly_metrics']=monthly.to_dict('records')
summary['date_ranges']=pd.DataFrame(ranges).to_dict('records')
summary['identity_reconciliation']=identity
summary['agent_id_unique']=int(ag.agent_id.nunique()); summary['agent_employee_code_unique']=int(ag.employee_code.nunique())
summary['payment_exact_dup_rows']=int(pay.duplicated().sum()); summary['payment_exact_dup_success_amount']=float(pd.to_numeric(pay[pay.duplicated(keep=False)].loc[pay[pay.duplicated(keep=False)].payment_status.eq('SUCCESS'),'amount'],errors='coerce').sum())
(G/'analysis_summary.json').write_text(json.dumps(summary,indent=2,default=str))
print('generated',len(list(G.glob('*'))),'gold outputs')
