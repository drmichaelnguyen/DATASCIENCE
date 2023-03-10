# Import required libraries
import pandas as pd
import dash
# import dash_html_components as html
import plotly.graph_objects as go

from dash.dependencies import Input, Output
import plotly.express as px

from dash import dcc
from dash import html

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'},
                                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                      {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}, ],
                                             value="ALL",
                                             placeholder="Launch Sites",
                                             searchable=True
                                             ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       100: '100',
                                                       2000: '2000',
                                                       5000: '5000',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
# @app.callback(Output(component_id='success-pie-chart', component_property='figure'),
#              Input(component_id='site-dropdown', component_property='value'),
#               )
@app.callback([Output(component_id='success-pie-chart', component_property='figure'),
                Output(component_id='success-payload-scatter-chart', component_property='figure')],
             [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')]
              )
def get_chart(entered_site,entered_load):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby(['class']).count().reset_index().rename(
        columns={'Booster Version': 'count'})
    filtered_all=spacex_df[(spacex_df['Payload Mass (kg)'] >= entered_load[0]) & (spacex_df['Payload Mass (kg)'] <= entered_load[1])]

    filtered=spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['Payload Mass (kg)'] <= entered_load[1])]
    if entered_site == 'ALL':
        fig1 = px.pie(spacex_df.groupby('Launch Site').count().reset_index(),
                     values='class', names='Launch Site',
                     title='All Launch Site')
        fig2 = px.scatter(x=filtered_all['Payload Mass (kg)'],
                         y=filtered_all['class'],
                          color=filtered_all['Booster Version Category'])
        fig1.update_layout(legend_title="Launch Sites")
        fig2.update_layout(title='Correlation between Payload and success rate', xaxis_title='Payload Mass',
                          yaxis_title='Class')

        return fig1,fig2
    else:
        fig1 = px.pie(filtered_df,
                     values='count',
                     names='class',
                     title=entered_site)
        fig2 = px.scatter(x=filtered['Payload Mass (kg)'],
                         y=filtered['class'],
                         color=filtered['Booster Version Category'],

                         )
        fig1.update_layout(legend_title="Success?")
        fig2.update_layout(title='Correlation between Payload and success rate', xaxis_title='Payload Mass',
                          yaxis_title='Class',legend_title='Booster Version Category')

        return fig1,fig2


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
#
# @app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
#              [Input(component_id='site-dropdown', component_property='value'),
#               Input(component_id='payload-slider', component_property='value')]
#               )
# def get_scatter_chart(entered_site,load):
#     filtered_all=spacex_df[spacex_df['Payload Mass (kg)']<=9000]
#
#     filtered=spacex_df[spacex_df['Launch Site']==entered_site]
#     if entered_site == 'ALL':
#         fig=px.scatter(x=filtered_all['Payload Mass (kg)'],
#                                   y=filtered_all['class'],
#                                   )
#         fig.update_layout(title='Correlation between Payload and success rate', xaxis_title='Payload Mass',
#                           yaxis_title='Class')
#         return fig
#     else:
#         fig = px.scatter(x=filtered['Payload Mass (kg)'],
#                          y=filtered['class'],
#                          color=spacex_df['Booster Version']
#                          )
#         fig.update_layout(title='Correlation between Payload and success rate', xaxis_title='Payload Mass',
#                           yaxis_title='Class')
#         return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
