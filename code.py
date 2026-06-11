#first upload data set using -
from google.colab import files
uploaded = files.upload()

#dataset - Bank churn from kaggle 


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

df = pd.read_csv("archive (1).csv")
df.columns = df.columns.str.strip()

df['Spending_Segment'] = pd.qcut(df['Total_Spend'], 3, labels=['Low', 'Medium', 'High'])

sns.set_style("whitegrid")

coordinates = widgets.Dropdown(
    options=[
        "Select Coordinates",
        "Account Type vs Total Spend",
        "Logins vs Total Spend",
        "Transactions vs Total Spend",
        "Account Balance vs Total Spend",
        "Spending Segment vs Total Spend"
    ],
    value="Select Coordinates",
    description="Data:"
)

graph_type = widgets.Dropdown(
    options=["Scatter", "Bar", "Histogram", "Boxplot", "Countplot"],
    value="Scatter",
    description="Graph:"
)

color_picker = widgets.Dropdown(
    options=["blue", "green", "red", "purple", "orange", "black", "pink", "brown"],
    value="blue",
    description="Color:"
)

size_picker = widgets.Dropdown(
    options=["Small", "Medium", "Large"],
    value="Medium",
    description="Size:"
)

button = widgets.Button(description="Generate Graph", button_style="success")
output = widgets.Output()

def plot(btn):
    with output:
        clear_output()

        if coordinates.value == "Select Coordinates":
            print("Select data relationship")
            return

        size_map = {"Small": (6,4), "Medium": (8,5), "Large": (12,7)}
        plt.figure(figsize=size_map[size_picker.value])

        if coordinates.value == "Account Type vs Total Spend":
            x, y = "Account_Type", "Total_Spend"
        elif coordinates.value == "Logins vs Total Spend":
            x, y = "Logins", "Total_Spend"
        elif coordinates.value == "Transactions vs Total Spend":
            x, y = "Transactions", "Total_Spend"
        elif coordinates.value == "Account Balance vs Total Spend":
            x, y = "Account_Balance", "Total_Spend"
        elif coordinates.value == "Spending Segment vs Total Spend":
            x, y = "Spending_Segment", "Total_Spend"

        if graph_type.value == "Scatter":
            sns.scatterplot(x=df[x], y=df[y], color=color_picker.value, alpha=0.6)
        elif graph_type.value == "Bar":
            sns.barplot(x=df[x], y=df[y], color=color_picker.value, ci=None)
        elif graph_type.value == "Histogram":
            sns.histplot(df[y], kde=True, color=color_picker.value)
        elif graph_type.value == "Boxplot":
            sns.boxplot(x=df[x], color=color_picker.value)
        elif graph_type.value == "Countplot":
            sns.countplot(x=df[x], color=color_picker.value)

        plt.show()

button.on_click(plot)

display(coordinates, graph_type, color_picker, size_picker, button, output)
