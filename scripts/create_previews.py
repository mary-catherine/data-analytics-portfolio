"""Recreate portfolio preview charts from the accompanying CSV files.

These are exploratory graphics, not screenshots of the Power BI reports.
Run from any working directory: python scripts/create_previews.py
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
NAVY = "#102F55"
BLUE = "#2773B9"
TEAL = "#20A79C"
AMBER = "#D89232"
INK = "#1C334D"
MUTED = "#60758A"
GRID = "#E5EBF0"
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10, "axes.spines.top":False,
                     "axes.spines.right":False, "axes.edgecolor":GRID, "axes.labelcolor":MUTED,
                     "xtick.color":MUTED, "ytick.color":MUTED, "text.color":INK,
                     "axes.titleweight":"bold", "savefig.facecolor":"white"})

def setup(title, subtitle):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.9), gridspec_kw={"wspace": 0.27})
    fig.patch.set_facecolor("white")
    fig.text(.055,.944, title, fontsize=20, weight="bold", color=NAVY, va="top")
    fig.text(.055,.875,subtitle,fontsize=10.5,color=MUTED,va="top")
    fig.subplots_adjust(left=.075,right=.97,top=.75,bottom=.17)
    for ax in axes:
        ax.set_axisbelow(True)
        ax.grid(axis="y",color=GRID,linewidth=.8)
    return fig,axes

def foot(fig, text):
    fig.text(.055,.045,text,fontsize=9,color=MUTED)

def retail():
    d=pd.read_csv(PROJECTS / 'retail-sales' / 'retail_sales_dataset.csv', parse_dates=['Order_Date'])
    monthly=d.set_index('Order_Date').resample('MS')['Sales_Revenue_INR'].sum()
    cats=d.groupby('Product_Category')[['Sales_Revenue_INR','Profit_INR']].sum().sort_values('Sales_Revenue_INR',ascending=True)
    f,(a,b)=setup('Retail sales | business performance','1,800 orders  •  2023–2024  •  INR  •  exploratory chart from source data')
    a.set_position([.075,.17,.36,.58]); b.set_position([.645,.17,.325,.58])
    a.plot(monthly.index,monthly.values/100000,color=BLUE,lw=2.7)
    a.fill_between(monthly.index,monthly.values/100000,alpha=.12,color=BLUE)
    a.set_title('Monthly revenue',loc='left',pad=14,color=NAVY,fontsize=13)
    a.set_ylabel('Revenue (₹ lakh)')
    a.xaxis.set_major_locator(matplotlib.dates.MonthLocator(interval=6))
    a.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%b %Y'))
    a.tick_params(axis='x',labelrotation=0)
    y=range(len(cats)); b.barh(y,cats.Sales_Revenue_INR/100000,color=BLUE,height=.7,label='Revenue')
    b.barh(y,cats.Profit_INR/100000,color=TEAL,height=.34,label='Profit')
    labels=[x.replace('Beauty & Personal Care','Beauty & personal care').replace('Sports & Outdoors','Sports & outdoors') for x in cats.index]
    b.set_yticks(list(y),labels,fontsize=9);b.grid(axis='y',visible=False);b.grid(axis='x',color=GRID)
    b.set_title('Revenue and profit by category',loc='left',pad=14,color=NAVY,fontsize=13)
    b.set_xlabel('₹ lakh');b.legend(frameon=False,loc='lower right',fontsize=9)
    foot(f,'Source: retail_sales_dataset.csv  |  1 lakh = ₹100,000  |  This is a data preview, not a Power BI screenshot.')
    f.savefig(PROJECTS/'retail-sales'/'retail_preview.png',dpi=160);plt.close(f)

def customer():
    d=pd.read_csv(PROJECTS/'customer-interaction'/'customer_interaction_synthetic.csv',keep_default_na=False,parse_dates=['Interaction_Date'])
    weekly=d.set_index('Interaction_Date').resample('W-MON',label='left',closed='left').size()
    gaps=d.loc[d.Quality_Gap.ne('None') & d.Quality_Gap.ne(''),'Quality_Gap'].value_counts().sort_values()
    f,(a,b)=setup('Customer interaction | quality monitoring','Synthetic dataset  •  3,000 interactions  •  January–December 2025')
    a.set_position([.075,.17,.36,.58]); b.set_position([.645,.17,.325,.58])
    a.bar(weekly.index,weekly.values,width=5,color=BLUE)
    a.set_title('Weekly interaction volume',loc='left',pad=14,color=NAVY,fontsize=13)
    a.set_ylabel('Interactions');a.xaxis.set_major_locator(matplotlib.dates.MonthLocator(interval=3));a.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%b %Y'))
    b.barh(gaps.index,gaps.values,color=TEAL);b.set_title('Recorded quality gaps',loc='left',pad=14,color=NAVY,fontsize=13)
    b.set_xlabel('Interactions');b.grid(axis='y',visible=False);b.grid(axis='x',color=GRID);b.tick_params(axis='y',labelsize=9)
    b.set_xlim(0,max(gaps.values)*1.16)
    for i,v in enumerate(gaps.values):b.text(v+4,i,str(v),va='center',fontsize=9,color=INK)
    foot(f,'Source: customer_interaction_synthetic.csv  |  “None” excluded  |  First and last weeks are partial  |  Data preview.')
    f.savefig(PROJECTS/'customer-interaction'/'customer_preview.png',dpi=160);plt.close(f)

def screening():
    d=pd.read_csv(PROJECTS/'screening-case-operations'/'screening_cases_synthetic.csv',parse_dates=['Created_Date'])
    monthly=d.set_index('Created_Date').resample('MS').size()
    cats=d.Case_Status.value_counts().reindex(['Closed','Open']).fillna(0)
    f,(a,b)=setup('Case operations | workload overview','Synthetic dataset  •  3,000 cases  •  January–December 2025')
    a.bar(monthly.index,monthly.values,width=20,color=BLUE)
    a.set_title('Cases created by month',loc='left',pad=14,color=NAVY,fontsize=13)
    a.set_ylabel('Cases created');a.xaxis.set_major_locator(matplotlib.dates.MonthLocator(interval=2));a.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%b'))
    b.barh(cats.index[::-1],cats.values[::-1],color=[AMBER,TEAL],height=.45)
    b.set_title('Status in the dataset',loc='left',pad=14,color=NAVY,fontsize=13)
    b.set_xlabel('Cases');b.grid(axis='y',visible=False);b.grid(axis='x',color=GRID);b.set_xlim(0,max(cats)*1.16)
    for i,v in enumerate(cats.values[::-1]):b.text(v+35,i,f'{v:,}',va='center',color=INK,fontsize=11)
    foot(f,'Source: screening_cases_synthetic.csv  |  Counts reflect recorded status; this is not a historical backlog trend.')
    f.savefig(PROJECTS/'screening-case-operations'/'screening_preview.png',dpi=160);plt.close(f)

if __name__=='__main__':
    retail();customer();screening()
    print('Created three exploratory data previews.')
