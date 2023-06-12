import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, ColumnDataSource
from bokeh.plotting import figure
import seaborn as sns
import numpy as np

# Load the Titanic dataset
df_titanic = sns.load_dataset("titanic")

# Exclude NaN values from the 'embark_town' column
embarked_options = ['All'] + list(df_titanic['embark_town'].dropna().unique())

# Create a Select widget for selecting the class
select_class = Select(title='Class', options=['All'] + list(df_titanic['class'].unique()))

# Create a Select widget for selecting the embarked location
select_embarked = Select(title='Embarked', options=embarked_options)

# Create a figure for displaying the histogram
histogram_fig = figure(plot_width=500, plot_height=400, title='Age Distribution')
histogram_fig.xaxis.axis_label = 'Age'
histogram_fig.yaxis.axis_label = 'Count'


# Define a callback function for the Select widgets
def update_histogram():
    # Filter the dataframe based on the selected class and embarked location
    selected_class = select_class.value
    selected_embarked = select_embarked.value

    filtered_df = df_titanic.copy()
    if selected_class != 'All':
        filtered_df = filtered_df[filtered_df['class'] == selected_class]
    if selected_embarked != 'All':
        filtered_df = filtered_df[filtered_df['embark_town'] == selected_embarked]

    # Update the histogram based on the filtered dataframe
    histogram_fig.title.text = f'Age Distribution ({selected_class}, {selected_embarked})'

    # Calculate the histogram bins and heights
    hist, edges = np.histogram(filtered_df['age'], bins=20)
    hist_source.data = dict(top=hist, left=edges[:-1], right=edges[1:])

    # Update the histogram data source
    hist_source.data = dict(top=hist, left=edges[:-1], right=edges[1:])


# Attach the callback function to the Select widgets' value attributes
select_class.on_change('value', lambda attr, old, new: update_histogram())
select_embarked.on_change('value', lambda attr, old, new: update_histogram())

# Create a ColumnDataSource for the histogram
hist_source = ColumnDataSource(data=dict(top=[], left=[], right=[]))

# Add the histogram to the figure
histogram_fig.quad(top='top', bottom=0, left='left', right='right', fill_color='dodgerblue', line_color='white',
                   source=hist_source)

# Arrange the widgets and figure in a layout
controls = column(select_class, select_embarked)
layout = row(controls, histogram_fig)

# Update the histogram initially
update_histogram()

# Add the layout to the current document
curdoc().add_root(layout)
