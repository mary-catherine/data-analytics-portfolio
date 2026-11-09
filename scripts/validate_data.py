"""Check key portfolio figures against the included CSV snapshots.

Run from any directory: python scripts/validate_data.py
These checks do not evaluate Power BI DAX, report rendering, or slicers.
"""
from pathlib import Path
import pandas as pd

P = Path(__file__).resolve().parents[1] / 'projects'
r = pd.read_csv(P/'retail-sales'/'retail_sales_dataset.csv')
c = pd.read_csv(P/'customer-interaction'/'customer_interaction_synthetic.csv', keep_default_na=False)
s = pd.read_csv(P/'screening-case-operations'/'screening_cases_synthetic.csv')

def near(actual, expected, tolerance=0.011):
    assert abs(actual-expected) <= tolerance, f'{actual} != {expected}'

# Retail: order grain, missing values, dates and cited aggregates.
assert len(r)==1800 and r.Order_ID.nunique()==1800 and r.Customer_ID.nunique()==860
assert int(r.isna().sum().sum())==0
assert str(pd.to_datetime(r.Order_Date).min().date())=='2023-01-01'
assert str(pd.to_datetime(r.Order_Date).max().date())=='2024-12-31'
near(r.Sales_Revenue_INR.sum(),8738212.45)
near(r.Profit_INR.sum(),3665122.45)
near(r.Sales_Revenue_INR.sum()/r.Order_ID.nunique(),4854.56)
near(r.loc[r.Product_Category=='Electronics','Sales_Revenue_INR'].sum(),3011109.65)
near(r.loc[r.Region=='South','Sales_Revenue_INR'].sum(),2647433.05)
assert r.groupby('Region').Sales_Revenue_INR.sum().idxmax()=='South'
near(100*(r.loc[r.Order_Year==2024,'Sales_Revenue_INR'].sum()/r.loc[r.Order_Year==2023,'Sales_Revenue_INR'].sum()-1),-3.80)
near(r.Discount_Pct.corr(r.Profit_INR/r.Sales_Revenue_INR),-.471,.001)

# Customer interactions: avoid interpreting literal "None" as missing.
assert len(c)==3000 and c.Interaction_ID.nunique()==3000
assert pd.to_datetime(c.Interaction_Date).min().date().isoformat()=='2025-01-01'
assert pd.to_datetime(c.Interaction_Date).max().date().isoformat()=='2025-12-31'
for name in ['QA_Pass','First_Contact_Resolution','Escalated','SLA_Met','CSAT_Responded']:
    assert set(pd.to_numeric(c[name]).unique()) <= {0,1}
assert (c.Quality_Gap=='Incorrect Resolution').sum()==397
assert (c.Quality_Gap=='Incomplete Documentation').sum()==363
near(pd.to_numeric(c.loc[c.Team=='Billing & Payments','QA_Score']).mean(),81.72)
assert pd.to_numeric(c.QA_Score).groupby(c.Team).mean().idxmin()=='Billing & Payments'
c['CSAT_numeric']=pd.to_numeric(c.CSAT_Score,errors='coerce')
valid=c[(c.CSAT_Responded==1)&c.CSAT_numeric.between(1,5)]
assert len(valid)==2279 and len(valid[valid.Channel=='Email'])==500
near(valid.CSAT_numeric.mean(),3.92)
near(valid.loc[valid.Channel=='Email','CSAT_numeric'].mean(),3.80)
near(100*pd.to_numeric(c.First_Contact_Resolution).mean(),58.37)
near(100*pd.to_numeric(c.Escalated).mean(),14.57)

# Case operations: closed-only metrics, case priority and creation dates.
assert len(s)==3000 and s.Case_ID.nunique()==3000
assert pd.to_datetime(s.Created_Date).min().date().isoformat()=='2025-01-01'
assert pd.to_datetime(s.Created_Date).max().date().isoformat()=='2025-12-31'
closed=s[s.Case_Status=='Closed']
assert len(closed)==2793 and (s.Case_Status=='Open').sum()==207
assert s.Case_Priority.isin(['High','Critical']).sum()==509
assert closed[['Resolution_Hours','SLA_Met']].notna().all().all()
assert not (pd.to_datetime(closed.Closed_Date)<pd.to_datetime(closed.Created_Date)).any()
near(closed.Resolution_Hours.mean(),32.65)
near(100*closed.SLA_Met.mean(),78.20)
monthly=s.groupby(pd.to_datetime(s.Created_Date).dt.to_period('M')).size()
assert str(monthly.idxmax())=='2025-03' and monthly.max()==292
print('Passed: retail, customer interaction, and case operation CSV figures and data checks.')
print('Power BI visuals, DAX, slicers, and stock-market source data were not tested.')
