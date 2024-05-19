import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import base64
import io

# Create Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div(id='dashboard-content')
])

# Parse uploaded data and generate dashboard
def parse_data(contents, filename):
    content_type, content_string = contents.split(',')
    
    # Decode the base64 encoded data
    decoded = base64.b64decode(content_string)
    
    try:
        # Assume that the user uploaded a CSV file
        if 'csv' in filename:
            # Read the CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        # Add other formats if needed
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    # Create dashboard content based on the data
    dashboard_content = html.Div([
        html.H3('Uploaded Dataset'),
        html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in df.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(df.iloc[i][col]) for col in df.columns
                ]) for i in range(min(len(df), 10))
            ])
        ]),
        html.Hr(),
        html.H3('Data Visualization'),
        dcc.Graph(
            id='scatter-plot',
            figure=px.scatter(df, x=df.columns[0], y=df.columns[1], title='Scatter Plot')
        ),
        dcc.Graph(
            id='bar-graph',
            figure=px.bar(df, x=df.columns[0], y=df.columns[1], title='Bar Graph')
        ),
        dcc.Graph(
            id='stacked-bar-chart',
            figure=px.bar(df, x=df.columns[0], y=[df.columns[1], df.columns[2]], title='Stacked Bar Chart')
        ),
        dcc.Graph(
            id='pie-chart',
            figure=px.pie(df, values=df.columns[1], names=df.columns[0], title='Pie Chart')
        ),
        dcc.Graph(
            id='donut-chart',
            figure=px.pie(df, values=df.columns[1], names=df.columns[0], title='Donut Chart', hole=0.3)
        ),
        html.Hr(),
        html.H3('Data Table'),
        html.Div([
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in df.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(df.iloc[i][col]) for col in df.columns
                    ]) for i in range(min(len(df), 10))
                ])
            ])
        ])
    ])
    
    return dashboard_content

# Callback to update dashboard content
@app.callback(Output('dashboard-content', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_dashboard(contents, filename):
    if contents is not None:
        children = parse_data(contents[0], filename[0])
        return children

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
