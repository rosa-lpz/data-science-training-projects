import base64
import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output


MASTER_DF = pd.read_csv("data/combined.csv")
# 2. App Layout
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Dynamic Dashboard Image Table", style={'textAlign': 'center'}),
    
    # Category Dropdown Filter
    html.Div([
        html.Label("Filter by Category:"),
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': cat, 'value': cat} for cat in MASTER_DF['category'].unique()],
            multi=True,
            placeholder="Select categories..."
        )
    ], style={'width': '40%', 'marginBottom': '20px'}),
    
    # The DataTable shell (columns defined here, data filled dynamically by callback)
    dash_table.DataTable(
        id='dynamic-table',
        columns=[
            {"id": "id", "name": "ID"},
            {"id": "category", "name": "Category"},
            {"id": "image_rendered", "name": "Image (400x400)", "presentation": "markdown"},
            {"id": "width", "name": "Width"},
            {"id": "height", "name": "Height"},
        ],
        markdown_options={"html": True},
        page_current=0,
        page_size=2,  # Process only 2 images at a time for performance
        page_action='custom',  # Tells Dash we will handle pagination in the callback
        style_cell={
            'textAlign': 'center', 
            'padding': '15px',
            'height': 'auto'
        }
    )
], style={'padding': '20px'})

# 3. Dynamic Callback Logic
@app.callback(
    Output('dynamic-table', 'data'),
    Output('dynamic-table', 'page_count'),
    Input('category-filter', 'value'),
    Input('dynamic-table', 'page_current'),
    Input('dynamic-table', 'page_size')
)
def update_table(selected_categories, page_current, page_size):
    # Start with full dataframe
    filtered_df = MASTER_DF.copy()
    
    # Apply category filter if user selected anything
    if selected_categories:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
    
    # Calculate total pages for pagination navigation
    total_pages = max(1, -(-len(filtered_df) // page_size))
    
    # Slice dataframe to only current page rows (Crucial performance step!)
    start_idx = page_current * page_size
    end_idx = start_idx + page_size
    paginated_df = filtered_df.iloc[start_idx:end_idx].copy()
    
    # Dynamically inject the 400x400 image tag strictly for rows being viewed
    paginated_df['image_rendered'] = paginated_df['image'].apply(
        lambda b64: f'<img src="data:image/jpeg;base64,{b64}" width="200" height="200" />'
    )
    
    return paginated_df.to_dict('records'), total_pages

if __name__ == '__main__':
    app.run(debug=True)