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
                html.Img(
                    src="/assets/msft.png",
                    style={"width": "6rem"}
                ),
                html.Div([
                    html.Div([
                        html.Div([
                            html.P("Change (1D)")
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
                    ]),
                    html.Div([
                        html.Div([
                            html.Button('SELL')
                        ]),
                        html.Div([
                            html.Button('BUY')
                        ])
                    ]),
                    html.Div([
                        html.Div([
                            html.Label(id='low-price', children='12.237')
                        ]),
                        html.Div([
                            html.Label(id='high-price', children='13.418')
                        ])
                    ]),
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




@app.callback(
    Output('high-price', 'children'),
    Output('high-price', 'className'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    if timer ==0:
        dff_filtered = dff.iloc[[21,22]]
        print(dff_filtered)
    elif timer == 1:
        dff_filtered = dff.iloc[[20,21]]
        print(dff_filtered)
    elif timer == 2:
        dff_filtered = dff.iloc[[19,20]]
        print(dff_filtered)
    elif timer == 3:
        dff_filtered = dff.iloc[[18,19]]
        print(dff_filtered)
    elif timer == 4:
        dff_filtered = dff.iloc[[17,18]]
        print(dff_filtered)
    elif timer == 5:
        dff_filtered = dff.iloc[[16,17]]
        print(dff_filtered)
    elif timer > 5:
        return dash.no_update

    recent_high = dff_filtered['rate'].iloc[0]
    older_high = dff_filtered['rate'].iloc[1]


    if recent_high > older_high:
        return recent_high, "mt-2 bg-success text-white p-1 border border-primary border-top-0"
    elif recent_high == older_high:
        return recent_high, "mt-2 bg-white p-1 border border-primary border-top-0"
    elif recent_high < older_high:
        return recent_high, "mt-2 bg-danger text-white p-1 border border-primary border-top-0"


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
