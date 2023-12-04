import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import urllib.request

# Download the CSV data
url = "https://raw.githubusercontent.com/msoreng/dash-visualization-px-data/main/patient_data2.csv"
response = urllib.request.urlopen(url)
data = pd.read_csv(response)

# Get unique patient IDs for dropdown options
patient_options = [{'label': 'All Patients', 'value': 'all'}] + \
                  [{'label': str(patient_id), 'value': patient_id} for patient_id in data['Patient ID'].unique()]

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Patient Data Scatter Plot"),

    dcc.Dropdown(
        id='patient-dropdown',
        options=patient_options,
        value='all',  # Default value is 'all' to show data for all patients
        multi=False,
        style={'width': '50%'}
    ),

    dcc.Graph(
        id='scatter-plot',
        style={'height': '80vh'}  # Adjust the height as needed, '80vh' means 80% of the viewport height
    )
])


# Define callback to update scatter plot based on selected patient ID
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('patient-dropdown', 'value')]
)
def update_scatter_plot(selected_patient):
    if selected_patient == 'all':
        filtered_data = data
        title = 'Relationship between Resting BP and Cholesterol (All Patients)'
    else:
        filtered_data = data[data['Patient ID'] == int(selected_patient)]
        title = f'Relationship between Resting BP and Cholesterol (Patient ID: {selected_patient})'

    fig = px.scatter(
        filtered_data,
        x='Resting BP (mm Hg)',
        y='Cholesterol mg/dL',
        color='Patient ID',
        title=title
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
