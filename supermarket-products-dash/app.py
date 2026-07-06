import base64
import io
import pandas as pd 
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from PIL import Image
import matplotlib                                # pip install matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import dash_ag_grid as dag  
import dash_bootstrap_components as dbc



# 1. Sample Base64 encoded string (A small blue square)
#SAMPLE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAAnUlEQVR42u3RAQ0AAAgDoMv8OasId5g9KAs6uYwYgghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCcAtD0r8fAnv0XAAAAABJRU5ErkJggg=="
df = pd.read_csv("data/combined.csv")
categories=df['category'].unique()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
        dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive="sm")
        ],
        style = {'margin-right':'90px','margin-left':'90px'})


# Layout
app.layout = dbc.Container([
    html.H1("Interactive Matplotlib with Dash", className='mb-2', style={'textAlign':'center'}),

    # Dropdown
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='category',
                value='cheeses',
                clearable=False,
                options=categories)
        ], width=4)
    ]),
    
    # Bar graph plotly
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-plotly', figure={})
        ], width=12, md=12)
    ]),
    
    

    # Table
    dbc.Row([
        dbc.Col([
            dag.AgGrid(
                id='grid',
                rowData=df.to_dict("records"),
                columnDefs=[{"field": i} for i in df.columns],
                columnSize="sizeToFit",
            )
        ], width=12, md=12),
    ]),

])

@app.callback(
    Output(component_id='bar-graph-plotly',component_property= 'figure'),
    Output(component_id='grid', component_property='defaultColDef'),
    Input('category', 'value'),
)

def plot_data(selected_yaxis):
    # Build the Plotly figure
    fig_bar_plotly = px.bar(df, x='category_id', y=selected_yaxis).update_xaxes(tickangle=330)

    my_cellStyle = {
            "styleConditions": [
                {
                    "condition": f"params.colDef.field == '{selected_yaxis}'",
                    "style": {"backgroundColor": "#d3d3d3"},
                },
                {   "condition": f"params.colDef.field != '{selected_yaxis}'",
                    "style": {"color": "black"}
                },
            ]
        }
    return fig_bar_plotly, {'cellStyle': my_cellStyle}

if __name__ == '__main__':
    app.run(debug=True)