import dash
from dash import dcc, html, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ... [Your data loading and processing code here] ...

dff = pd.read_csv("data.csv")
dff = dff[dff.indicator.isin(['high'])]

# Create the Dash app
app = dash.Dash(__name__)
app.server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Define the layout of the app
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                # First Row: Title
                html.Div([
                    html.P("Closing Value", style={'textAlign': 'Left', 'marginBottom': '-20px', 'color': '#AAAAAA', 'fontSize': '24px', 'fontWeight': 'bold'})
                ]),
                # Second Row: Indicator Graph and Closing Value
                html.Div([
                    # Closing Value (Left)
                    html.Div([
                        html.P(id='closing-value', children='$0.00', style={'color': 'black', 'fontSize': '35px'})
                    ],className='six columns', style={'marginTop': '1x'}),
                    # Indicator Graph (Right)
                    html.Div([
                        dcc.Graph(id='indicator-graph', figure={},
                                  config={'displayModeBar': False})
                    ],className='six columns', style={'marginTop': '35px'}),
                ], style={'justifyContent': 'space-between', 'display': 'flex'}),
                # Third Row: Daily Line Graph
                html.Div([
                    dcc.Graph(id='daily-line', figure={},
                              config={'displayModeBar': False},
                               className='line-chart')
                ])
            ], style={'width': '24rem', 'marginTop': '10px'})
        ], style={'width': '50%', 'margin': '0 auto'})
    ]),
    dcc.Interval(id='update', n_intervals=0, interval=1000*5)
])

# ... [Your callback functions here] ...
@app.callback(
    Output('daily-line', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    dff_rv = dff.iloc[::-1]
    fig = px.line(dff_rv, x='date', y='rate',
                   range_y=[dff_rv['rate'].min(), dff_rv['rate'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                             paper_bgcolor='rgba(0,0,0,0)',
                                             plot_bgcolor='rgba(0,0,0,0)',
                                             yaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ),
                                             xaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False,
                                             
                                             ))

    day_start = dff_rv[dff_rv['date'] == dff_rv['date'].min()]['rate'].values[0]
    day_end = dff_rv[dff_rv['date'] == dff_rv['date'].max()]['rate'].values[0]

    if day_end >= day_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        return fig.update_traces(fill='tozeroy',
                                 
                             line={'color': 'red'})


@app.callback(
        Output('indicator-graph', 'figure'),
        Input('update', 'n_intervals')
)

def update_graph(timer):
    dff_rv = dff.iloc[::-1]
    day_start = dff_rv[dff_rv['date'] == dff_rv['date'].min()]['rate'].values[0]
    day_end = dff_rv[dff_rv['date'] == dff_rv['date'].max()]['rate'].values[0]
    
    fig = go.Figure(go.Indicator(
        mode='delta',
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat': '.2%'}))
    
    fig.update_traces(delta_font={'size':16})
    fig.update_layout(height=40, width=100)

    if day_end >= day_start:
        fig.update_traces(delta_decreasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_increasing_color='red')

    return fig

# Callback function to update the closing value
@app.callback(
    Output('closing-value', 'children'),
    Input('update', 'n_intervals')
)
def update_closing_value(timer):
    # Extract the latest closing value from your data
    latest_close = dff['rate'].iloc[-1]  # Assuming 'rate' is the closing value
    return f"${latest_close:.2f}"


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
