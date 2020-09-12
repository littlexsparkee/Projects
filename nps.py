import pandas as pd
import os
import glob
import pathlib
from bokeh.plotting import ColumnDataSource, figure, show, output_file

def calc_nps(score):
    return 100*((score>=9).sum()-(score<=6).sum())/score.count()

cwd = os.getcwd()
filepath = list(pathlib.Path(cwd).rglob('*.csv'))
df = pd.read_csv(filepath[0], parse_dates=['created_at'])
df['created_at'] = pd.to_datetime(df['created_at'],utc=True).dt.tz_localize(None)
df.set_index('created_at', inplace=True)

total = df.resample('D', on='created_at')['score'].apply(lambda x: calc_nps(x))
admin = df[df['is_admin']==1].resample('D', on='created_at')['score'].apply(lambda x: calc_nps(x))
reg_user = df[df['is_admin']==0].resample('D', on='created_at')['score'].apply(lambda x: calc_nps(x))

output_file("NPS.html")

xyvalues = pd.DataFrame(data=dict(
        Date=total.index,
        Total=total,
        Regular_User=reg_user,
        Admins=admin,
    ))

p = figure(title="NPS", x_axis_label="Date", y_axis_label="Score", x_axis_type="datetime")
p.line('Date','Total',source=xyvalues, legend="Overall", color='red')
p.line('Date','Regular_User',source=xyvalues, legend="Regular Users", color='blue')
p.line('Date','Admins',source=xyvalues, legend="Admin", color='gold')
p.legend.click_policy="hide"
show(p)
