import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

markdown_text = '''
The Netflix documentary, *Why Women Are Paid Less*, argues that the gender pay 
gap can best be explained with some history: after women entered the workforce,
the 50s and 60s still had other unofficial barriers to entry (lower education 
rates among women, discrimation was legal and commonplace, job culture, lower
workforce participation, so on and so forth). While many of these barriers have
lowered with time, there is still the issues correlated to women taking 
on the primary caregiver role in raising children. When a woman takes on this role,
she is now dividing her time in two between home and work, and can not take the extra
opportunities to advance like her male counterparts. So what is called the gender 
wage gap could more accurately be described as the mother wage gap, and women who work
and don't have children actually make 97% what a man does today.


The GSS is a sociology survey that's been collected since 1972 and aims to understand the sentiments of the 
contemporary American people, aiming to get a breadth of experience based on race, income, location, sex,
and other factors. Data is collected by UChicago and funded by the NSF, and can be found online at 
[this website](https://gssdataexplorer.norc.org/). Since it's inception, the survey has had 59,599 respondents. 
'''

gss_bar = gss_clean.groupby('sex', sort=False).agg({'income':'mean',
                                     'job_prestige':'mean',
                                    'socioeconomic_index':'mean',
                                                   'education': 'mean'})
gss_bar['income'] = round(gss_bar['income'],2)
gss_bar['job_prestige'] = round(gss_bar['job_prestige'],2)
gss_bar['socioeconomic_index'] = round(gss_bar['socioeconomic_index'],2)
gss_bar['education'] = round(gss_bar['education'],2)
gss_bar = gss_bar.rename({'job_prestige':'Occupational Prestige', 'income': 'Income',
                          'socioeconomic_index':'Socioeconomic Index', 'education': 'Years of Education'}, axis=1)
gss_bar = gss_bar.reset_index()
gss_bar

table = ff.create_table(gss_bar)
bar = gss_clean.groupby(['sex', 'male_breadwinner']).size()
bar = bar.reset_index()
bar = bar.rename({0:'Count'}, axis=1)
fig_1 = px.bar(bar, x='male_breadwinner', y='Count', color='sex',
            labels={'male_breadwinner':'Preference for a Male Breadwinner', 'Count':'Count'},
            #hover_data = ['votes', 'Biden thermometer', 'Trump thermometer'],
            #text='coltext',
            barmode = 'group')
fig_1.update_layout(showlegend=True)
fig_1.update(layout=dict(title=dict(x=0.5)))
fig_2 = px.scatter(gss_clean, x='job_prestige', y='income', 
                 color = 'sex', 
                 trendline = 'ols',
                 height=600, width=600,
                 labels={'job_prestige':'Job Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig_2.update(layout=dict(title=dict(x=0.5)))
fig_3 = px.box(gss_clean, x='sex', y = 'income', color = 'sex',
                   labels={'sex':'Gender', 'income':'Income'})
fig_3.update(layout=dict(title=dict(x=0.5)))
fig_3.update_layout(showlegend=False)
fig_4 = px.box(gss_clean, x='sex', y = 'job_prestige', color = 'sex',
                   labels={'job_prestige':'Job Prestige', 'sex':''})
fig_4.update(layout=dict(title=dict(x=0.5)))
fig_4.update_layout(showlegend=False)
fig_3.update(layout=dict(title=dict(x=.5)))
fig_3.update_layout(showlegend=False)


gss_small = gss_clean[['income','sex','job_prestige']]
gss_small['job_prestige'] = pd.cut(gss_small['job_prestige'], [0, 17, 34, 51, 68, 85, 100],
                                   labels=['Essential','No Collar','Blue Collar','Salary/Non-Exempt','White Collar','C Suite'])
gss_small=gss_small.dropna()

fig_5 = px.box(gss_small, x='sex', y = 'income', color = 'sex',
             facet_col='job_prestige', facet_col_wrap=2,      
             labels={'income':'Income', 'sex':'Gender'})
fig_5.update(layout=dict(title=dict(x=0.5)))
fig_5.update_layout(showlegend=False)

import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(  [
        html.H1("Understanding the Gender Wage Gap"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Metrics"),
        
        dcc.Graph(figure=table),
        
        html.H2("Preference of Male Breadwinner by Sex"),
        
        dcc.Graph(figure=fig_1),
        
        html.H2("Income vs Job Prestige by Sex"),
        
        dcc.Graph(figure=fig_2),
    
        html.H2('Distribution of Job Prestige by Sex'),
        
        dcc.Graph(figure=fig_5),
    
        html.Div([
            
            html.H2("Distribution of Income by Sex"),
            
            dcc.Graph(figure=fig_3)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("Distribution of Prestige by Sex"),
            
            dcc.Graph(figure=fig_4)
            
        ], style = {'width':'48%', 'float':'right'})
    ])
if __name__ == '__main__':
    app.run_server(debug=True)
