import base64
import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output

# 1. Setup Mock Data using Raw Binary Bytes (b"...")
# These are identical 1x1 pixel mock image byte streams (one blue, one red)
BLUE_SQUARE_BINARY = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x00\x01\x00\x00\xff\x00\x01\x00\x01q\x0c\x8e\x00\x00\x00\x00IEND\xaeB`\x82'
RED_SQUARE_BINARY  = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x03\x01\x01\x00\x18\xdd\x8d\xb0\x00\x00\x00\x00IEND\xaeB`\x82'

data = {
    'id': [1, 2, 3, 4],
    'category': ['Electronics', 'Clothing', 'Electronics', 'Clothing'],
    'image_blob': [BLUE_SQUARE_BINARY, RED_SQUARE_BINARY, BLUE_SQUARE_BINARY, RED_SQUARE_BINARY], # Raw binary columns
    'width': [100, 120, 100, 120],
    'height': [100, 120, 100, 120]
}
MASTER_DF = pd.DataFrame(data)

# 2. App Layout
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Dynamic Table using Raw Binary DB Blobs", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Filter by Category:"),
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': cat, 'value': cat} for cat in MASTER_DF['category'].unique()],
            multi=True,
            placeholder="Select categories..."
        )
    ], style={'width': '40%', 'marginBottom': '20px'}),
    
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
        page_size=2,  # Process only 2 images at a time for maximum speed
        page_action='custom',
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
    filtered_df = MASTER_DF.copy()
    
    if selected_categories:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
    
    total_pages = max(1, -(-len(filtered_df) // page_size))
    
    # Slice rows strictly for the active page
    start_idx = page_current * page_size
    end_idx = start_idx + page_size
    paginated_df = filtered_df.iloc[start_idx:end_idx].copy()
    
    # Core Change: Convert raw binary bytes to Base64 text string inside the lambda loop
    def binary_to_html_img(binary_data):
        if not binary_data:
            return ""
        # 1. Encode binary bytes to base64 bytes, then decode to a UTF-8 string
        b64_str = base64.b64encode(binary_data).decode('utf-8')
        # 2. Return standard HTML tag scaled to 400x400
        return f'<img src="data:image/png;base64,{b64_str}" width="400" height="400" />'

    # Apply the conversion exclusively to the sliced page view
    paginated_df['image_rendered'] = paginated_df['image_blob'].apply(binary_to_html_img)
    
    return paginated_df.to_dict('records'), total_pages

if __name__ == '__main__':
    app.run_server(debug=True)