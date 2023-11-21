import dash
from dash import dcc, html, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ... [Your data loading and processing code here] ...

dff = pd.read_csv("data.csv")
dff = dff[dff.indicator.isin(['high'])]

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.P("Total Value")
                        ]),
                        html.Div([
                            dcc.Graph(id='indicator-graph', figure={},
                                      config={'displayModeBar': False})
                        ])
                    ]),
                    html.Div([
                        html.Div([
                            dcc.Graph(id='daily-line', figure={},
                                      config={'displayModeBar': False})
                        ])
                    ])
                   
                ])
            ], style={'width': '24rem', 'marginTop': '1rem'})
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
                                             showticklabels=False
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
    
    fig.update_traces(delta_font={'size':12})
    fig.update_layout(height=30, width=70)

    if day_end >= day_start:
        fig.update_traces(delta_decreasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_increasing_color='red')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
