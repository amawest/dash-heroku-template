# ==================================================================================================================
# Created November 29th, 2020
# Homework assignment for Practice & Applications under Professor Jonathon Kropko at UVA.
# Worked with lab group to complete, then re-edited with Haizhu Hong to get successfully deployed to Heroku.
# Corresponding link to Heroku: https://applied-ds-dashboard.herokuapp.com/
# ==================================================================================================================
# Import Libraries
# ==================================================================================================================

### General Libraries
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

### Dash Libraries
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

### Style Sheet
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']

# ==================================================================================================================
# Data Cleaning
# ==================================================================================================================
 
### Data
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

### Rename Columns
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

# ==================================================================================================================
# Generate Information (Text, Tables) 
# ==================================================================================================================

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

### Primary Table
table = ff.create_table(gss_bar)
bar = gss_clean.groupby(['sex', 'male_breadwinner']).size()
bar = bar.reset_index()
bar = bar.rename({0:'Count'}, axis=1)


### Figure 1
gss_bar = gss_clean.groupby(['sex', 'male_breadwinner']).size().reset_index().rename({0:'count'}, axis=1)
fig_1 = px.bar(bar, x='male_breadwinner', y='Count', color='sex',
            labels={'male_breadwinner':'Preference for a Male Breadwinner', 'Count':'Count'},
            color_discrete_sequence=["#cf72ca", "blue"],
            #hover_data = ['votes', 'Biden thermometer', 'Trump thermometer'],
            #text='coltext',
            barmode = 'group')
fig_1.update_layout(showlegend=True)
fig_1.layout.template = 'seaborn'
fig_1.update(layout=dict(title=dict(x=0.5)))


### Figure 2
fig_2 = px.scatter(gss_clean, x='job_prestige', y='income', 
                 color = 'sex', 
                 color_discrete_sequence=["blue", "#cf72ca", "green", "goldenrod"],
                 trendline = 'ols',
                 labels={'job_prestige':'Job Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig_2.layout.template = 'seaborn'
fig_2.update(layout=dict(title=dict(x=0.5)))


### Figures 3
fig_3 = px.box(gss_clean, x='sex', y = 'income', color = 'sex',
               color_discrete_sequence=["blue", "#cf72ca", "green", "goldenrod"],
               labels={'sex':'Gender', 'income':'Income'})
fig_3.update(layout=dict(title=dict(x=0.5)))
fig_3.layout.template = 'seaborn'
fig_3.update_layout(showlegend=False)

### Figure 4
fig_4 = px.box(gss_clean, x='sex', y = 'job_prestige', color = 'sex',
               color_discrete_sequence=["blue", "#cf72ca", "green", "goldenrod"],
               labels={'job_prestige':'Job Prestige', 'sex':''})
fig_4.update(layout=dict(title=dict(x=0.5)))
fig_4.layout.template = 'seaborn'
fig_4.update_layout(showlegend=False)


### Figure 5
gss_plot = gss_clean[['income', 'sex', 'job_prestige']]
gss_plot['prestige_cat'] = pd.cut(gss_plot['job_prestige'], bins=[15.50, 26.50, 37.50, 47.50, 58.50, 69.50, 80], 
                                  labels=('level1', 'level2', 'level3', 'level4', 'level5', 'level6'))
gss_plot = gss_plot.dropna()

fig_5 = px.box(gss_small, x='sex', y = 'income', color = 'sex',
             facet_col='job_prestige', facet_col_wrap=2,    
             color_discrete_sequence=["#cf72ca", "blue", "green", "goldenrod"],
             labels={'income':'Income', 'sex':'Gender'})
fig_5.update(layout=dict(title=dict(x=0.5)))
fig_5.layout.template = 'seaborn'
fig_5.update_layout(showlegend=False)

### Interactive Portion
gss_clean['education_level'] = pd.cut(gss_clean['education'], bins=[-0.50, 6, 8, 12, 16, 20], 
                                      labels=('Elementary', 'Middle School', 'High School', 'College', 'Graduate'))
y_axis = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork'] 
x_axis = ['sex', 'region', 'education_level']
gss_dropdown = gss_clean[y_axis + x_axis].dropna()

# ==================================================================================================================
# Create Dashboard
# ==================================================================================================================

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [
        html.H1("Understanding the Gender Wage Gap", style={'textAlign': 'center'}),
        
        dcc.Markdown(children = markdown_text),
        
        html.H4("Average Income, Prestige of Occupation, Socioeconomic Status and Education Achieved By Gender", ),
        
        dcc.Graph(figure=fig_1),
    
        html.H4("Comparing Relationship Between Avg. Income and Job Prestige by Gender"),
        
        dcc.Graph(figure=fig_2),
        
        html.Div([
            
            html.H4("Average Income By Gender"),
            
            dcc.Graph(figure=fig_3)
            
        ], style = {'width':'50%', 'float':'left'}),
        
        html.Div([
            
            html.H4("Job Prestige By Gender"),
            
            dcc.Graph(figure=fig_4)
            
        ], style = {'width':'50%', 'float':'right'}),
        
        html.H4("Average Income By Gender and Job Prestige Level"),
        
        dcc.Graph(figure=fig_5),
        
        html.H4("Interactive Barplot"),
        
        html.Div([
            html.H3("Dependent Variable"),
            dcc.Dropdown(id='values',
                         options=[{'label': i, 'value': i} for i in y_axis],
                         value='satjob'),

            html.H3("Independent Variable"),
            dcc.Dropdown(id='groups',
                         options=[{'label': i, 'value': i} for i in x_axis],
                         value='sex')
        ], style={'width': '25%', 'float': 'right'}),
        
        html.Div([
            dcc.Graph(id="graph")
        ], style={'width': '70%', 'float': 'left'}),
        
        ], style = {'font-family':'Arial',
                'width':'75%',
                'text-align':'center',
                'padding-left': '150px', 
                'color': '#2f3136'})

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
        color_discrete_sequence=["#cf72ca", "blue"],
        text='count',
        barmode='group'
)


### Run
if __name__ == '__main__':
    app.run_server(debug=True)
    
# ==================================================================================================================
# Finis
# ==================================================================================================================

