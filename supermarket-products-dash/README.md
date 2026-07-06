# Health SDG Dashboard

A Dash dashboard for visualizing data related to Solar Energy plants.
## Features



## Setup

1. Create and activate the virtual environment:
```bash
python3 -m venv supdashvenv
source supdashvenv/bin/activate  # On Linux/Mac
# or
supdashvenv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python3 app.py
```

## Data Source

Dataset used for this project: Supermarket Product Images
* https://www.kaggle.com/datasets/realalexanderwei/supermarket-product-images-thumbnails/data

## Technologies Used


### Dash: Web application framework
This installs the core web framework, which automatically includes dash_html_components (for the html.Img tags) and dash_core_components (for interactive inputs).

### Pandas: Data manipulation
Required if you are handling tabular data (like loading from a CSV or querying a relational database into a structured table).

### Pillow (PIL)
The standard Python Imaging Library. You only strictly need this if you plan to manipulate the images inside your Python code (e.g., resizing, cropping, or converting to grayscale) before rendering them.

### Plotly - Interactive visualizations
## License

MIT License


## References
* Plotly - Build a Python Dashboard with Matplotlib and Dash: https://youtu.be/dRjNfahHJRQ
* https://github.com/plotly/dash-image-processing/blob/master/dash_reusable_components.py
* table images thumbnails: https://github.com/plotly/dash-table/issues/800