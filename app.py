import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']


### Data preparation 
#%%capture
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

### Generate table
table = gss_clean.groupby('sex').agg({'income': 'mean', 'job_prestige':'mean', 'socioeconomic_index':'mean', 'education':'mean'}).round(2)
fig = ff.create_table(table)


### Barplot
gss_bar = gss_clean.groupby(['sex', 'male_breadwinner']).size().reset_index().rename({0:'count'}, axis=1)
fig_1 = px.bar(gss_bar, x='male_breadwinner', y='count', color='sex',
            labels={'male_breadwinner': 'agree/disagree: male is the bread winner', 'count':'number of responses'},
            text='count',
            barmode='group')
fig_1.update_layout(showlegend=True)

### Scatterplot
fig_2 = px.scatter(gss_clean, x='job_prestige', y='income',
                 color = 'sex',
                 trendline='ols',
                 labels={'income':'annual income', 
                        'job_prestige':'occupational prestige score'},
                 hover_data=['education', 'socioeconomic_index'])

### Boxplots for income and job prestige side-by-side
fig_3 = px.box(gss_clean, x='sex', y = 'income', color = 'sex',
                   labels={'income':'personal annual income', 'sex':''})
fig_3.update_layout(showlegend=False)

fig_4 = px.box(gss_clean, x='sex', y = 'job_prestige', color = 'sex',
                   labels={'job_prestige':'occupational prestige score', 'sex':''})
fig_4.update_layout(showlegend=False)


### Boxplots
gss_plot = gss_clean[['income', 'sex', 'job_prestige']]
gss_plot['prestige_cat'] = pd.cut(gss_plot['job_prestige'], bins=[15.99, 26.66, 37.33, 47.99, 58.66, 69.33, 80], 
                                  labels=('level1', 'level2', 'level3', 'level4', 'level5', 'level6'))
gss_plot = gss_plot.dropna()

fig_5 = px.box(gss_plot, x='sex', y = 'income', color = 'sex', 
             facet_col='prestige_cat', facet_col_wrap = 2,
             labels={'prestige_cat':'occupational prestige Level', 'income':'annual income', 'sex':''},
             color_discrete_map = {'male':'blue', 'female':'red'})
fig_5.update_layout(showlegend=True)

gss_clean['education_level'] = pd.cut(gss_clean['education'], bins=[-0.01, 6, 8, 12, 16, 20], 
                                      labels=('Elementary', 'Middle School', 'High School', 'College', 'Graduate'))
value_columns = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork'] 
group_columns = ['sex', 'region', 'education_level']
gss_dropdown = gss_clean[value_columns + group_columns].dropna()

### Create app
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [
        html.H1("Exploring the Gender Wage Gap with GSS", style={'textAlign': 'center'}),
        
        dcc.Markdown(children = markdown_text),
        
        html.H4("Comparing Mean Income, Occupational Prestige, Socioeconomic Status and Education Level By Gender", ),
        
        dcc.Graph(figure=fig),
    
        html.H4("Comparing the Relationship Between Annual Income and Occupational Prestige By Gender"),
        
        dcc.Graph(figure=fig_2),
        
        html.Div([
            
            html.H4("Boxplot For Annual Income By Gender"),
            
            dcc.Graph(figure=fig_3)
            
        ], style = {'backgroundColor':'#111111', 'color':'#7FDBFF', 'width':'50%', 'float':'left'}),
        
        html.Div([
            
            html.H4("Boxplot For Occupational Prestige By Gender"),
            
            dcc.Graph(figure=fig_4)
            
        ], style = {'backgroundColor':'#111111', 'color':'#7FDBFF', 'width':'50%', 'float':'right'}),
        
        html.H4("Boxplot For Annual Income By Gender and Occupational Prestige Level"),
        
        dcc.Graph(figure=fig_5),
        
        html.H4("Barplots with Dropdown Menu"),
        
        html.Div([
            html.H3("y-axis features"),
            dcc.Dropdown(id='values',
                         options=[{'label': i, 'value': i} for i in value_columns],
                         value='satjob'),

            html.H3("x-axis features"),
            dcc.Dropdown(id='groups',
                         options=[{'label': i, 'value': i} for i in group_columns],
                         value='sex')
        ], style={'width': '25%', 'float': 'right'}),
        
        html.Div([
            dcc.Graph(id="graph")
        ], style={'width': '70%', 'float': 'left'}),
        
    ], style = {'width':'75%', 'text-align':'center', 'padding-left': '150px'})

@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='values',component_property="value"),
                   Input(component_id='groups',component_property="value")])

def make_figure(x,y):
    gss_bar = gss_dropdown.groupby([x, y]).size().reset_index().rename({0:'count'}, axis=1)
    return px.bar(
        gss_bar,
        x=x,
        y='count',
        color=y,
        text='count',
        barmode='group'
)


if __name__ == '__main__':
    app.run_server(debug=True)
