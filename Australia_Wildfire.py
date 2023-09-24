import dash
from dash import dcc 
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

#Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

app = dash.Dash(__name__)
#Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[html.H1('Australia Wildfire Dashboard',style= {'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                html.Br(),
                                # html.Div([
                    
                                    html.Div([
                                        html.H2('Select Region: ', style= {'margin-right': '2em'}),
                                        dcc.RadioItems([{"label": "New South Wales", "value": "NSW"},
                                                        {"label": "Northern Territory", "value": "NT"},
                                                        {"label": "Queensland", "value": "QL"},
                                                        {"label": "South Australia", "value": "SA"},
                                                        {"label": "Tasmania", "value": "TA"},
                                                        {"label": "Victoria", "value": "VI"},
                                                        {"label": "Western Australia", "value": "WA"},

                                        ], value = "NSW", id = 'input-region', inline = True),
                                    ]),
                                    html.Div([
                                        html.H2('Select Year: ', style={'margin-right': '2em'}),
                                        dcc.Dropdown(df.Year.unique(),id = 'input-year', value = '2005'
                                        ),
                                ]),
                                # ]),
                                html.Br(),
                                html.Br(),
                                html.Div([
                                    html.Div([], id='plot1'),
                                    html.Div([], id='plot2')
                                ], style = {'display': 'flex'}),

])

@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children')],
               [Input(component_id='input-region', component_property='value'),
                Input(component_id='input-year', component_property='value')]
        )

def reg_year_display(input_region, input_year):
    
    #data
    region_data = df[df['Region']==input_region]
    y_r_data = region_data[region_data['Year']==input_year]

    #Plot one - Monthly Average Estimated Fire Area
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data, values= 'Estimated_fire_area', names= 'Month', 
                  title= "{}: Monthly Average Estimated Fire Area in year {}".format(input_region, input_year))

    #Plot two - Month Average Count of Pixels for Presumed Vegetation Fires
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data, x= 'Month', y = 'Count',
                  title= "{}: Average Count of Pixels for Presumed Vegetation Fires in year {}".format(input_region, input_year))
    
    return [dcc.Graph(figure = fig1),
            dcc.Graph(figure = fig2)]

if __name__ == "__main__":
    app.run_server()
    


