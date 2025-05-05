import dash
from dash import dcc, html, Input, Output
import numpy as np
import plotly.graph_objects as go

# Dash app setup
app = dash.Dash(__name__)
server = app.server  # needed for deployment

# Time and baseline cumulative hazard (CH0)
time_points = np.array([1, 3, 5])
baseline_cumhaz = np.array([0.75, 0.78, 0.80])

# Beta coefficients
betas = {
    'age': -0.2,
    'ethnicity_black': -0.4,
    'ethnicity_white': -0.1,
    'ethnicity_asian': -0.6,
    'bmi': 1.0,
    'ses': 0.5
}

# Layout
app.layout = html.Div([
    html.H2("Interactive Cumulative Incidence Curve"),
    
    html.Label("Age:"),
    dcc.Input(id='input-age', type='number', value=50),
    
    html.Label("BMI:"),
    dcc.Input(id='input-bmi', type='number', value=25),
    
    html.Label("SES:"),
    dcc.Input(id='input-ses', type='number', value=2),
    
    html.Label("Ethnicity:"),
    dcc.Dropdown(
        id='input-ethnicity',
        options=[
            {'label': 'Black', 'value': 'black'},
            {'label': 'White', 'value': 'white'},
            {'label': 'Asian', 'value': 'asian'}
        ],
        value='white'
    ),
    
    dcc.Graph(id='cic-graph')
])

# Callback
@app.callback(
    Output('cic-graph', 'figure'),
    Input('input-age', 'value'),
    Input('input-bmi', 'value'),
    Input('input-ses', 'value'),
    Input('input-ethnicity', 'value')
)
def update_graph(age, bmi, ses, ethnicity):
    # Construct covariate vector
    covariates = {
        'age': age,
        'ethnicity_black': 1 if ethnicity == 'black' else 0,
        'ethnicity_white': 1 if ethnicity == 'white' else 0,
        'ethnicity_asian': 1 if ethnicity == 'asian' else 0,
        'bmi': bmi,
        'ses': ses
    }

    # Compute linear predictor and hazard ratio
    lp = sum(covariates[k] * betas[k] for k in betas)
    hr = np.exp(lp)

    # Calculate individual cumulative hazard and incidence
    cum_hazard = baseline_cumhaz * hr
    cum_incidence = 1 - np.exp(-cum_hazard)

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_points,
        y=cum_incidence,
        mode='lines+markers',
        line=dict(color='blue'),
        name='CIC'
    ))
    fig.update_layout(
        title='Cumulative Incidence Curve',
        xaxis_title='Time (Years)',
        yaxis_title='Cumulative Incidence',
        template='plotly_white',
        yaxis=dict(range=[0, 1])
    )
    return fig

# Run
if __name__ == '__main__':
    app.run_server(debug=True)

