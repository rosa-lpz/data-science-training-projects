import base64
import pandas as pd
from dash import Dash, html, dash_table

df = pd.read_csv("data/combined.csv")
# 1. Create a tiny mock Base64 string (a small blue square) for demonstration
#MOCK_B64 = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAAnUlEQVR42u3RAQ0AAAgDoMv8OasId5g9KAs6uYwYgghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCCEEIeYIIQQh5gghBCHmCcAtD0r8fAnv0XAAAAABJRU5ErkJggg=="
MOCK_B64 = df['image'][0]
# 2. Build your sample DataFrame
data = {
    'id': [1, 2],
    'category': ['Electronics', 'Clothing'],
    'image': [MOCK_B64, MOCK_B64],
    'width': [100, 120],
    'height': [100, 120]
}
df = pd.DataFrame(data)

# 3. Transform the 'image' column into an HTML image string format that Markdown accepts.
# We explicitly set width='400' and height='400' inside the HTML tag here.
df['image_rendered'] = df['image'].apply(
    lambda b64: f'<img src="data:image/jpeg;base64,{b64}" width="400" height="400" />'
)

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Data Table with 400x400px Images", style={'textAlign': 'center'}),
    
    dash_table.DataTable(
        # Convert dataframe to dictionary format required by Dash
        data=df.to_dict('records'),
        
        # Define columns, explicitly marking the image column presentation as 'markdown'
        columns=[
            {"id": "id", "name": "ID"},
            {"id": "category", "name": "Category"},
            {"id": "image_rendered", "name": "Image", "presentation": "markdown"},
            {"id": "width", "name": "Orig Width"},
            {"id": "height", "name": "Orig Height"},
        ],
        
        # CRITICAL: This allows raw HTML (like our <img> tag) to render inside Markdown
        markdown_options={"html": True},
        
        # Optional: Style the table cells so 400x400 images fit comfortably
        style_cell={
            'textAlign': 'center',
            'padding': '15px',
            'height': 'auto',  # Ensures row grows to fit the 400px height
            'whiteSpace': 'normal'
        },
        style_header={
            'fontWeight': 'bold',
            'backgroundColor': '#f4f4f2'
        }
    )
], style={'padding': '20px'})

if __name__ == '__main__':
    app.run(debug=True)