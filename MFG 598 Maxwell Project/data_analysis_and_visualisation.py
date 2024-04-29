# -*- coding: utf-8 -*-
"""Data analysis and visualisation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12YNLkG2fX2NBxGIHP_aTF2VMcytfMeo0
"""

import pandas as pd


data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/SCMS_Data.csv')


print("Initial columns:", data.columns)


data.drop('Project Code', axis=1, inplace=True)

# Verify the column has been removed
print("Columns after removal:", data.columns)

print("Unique values before:", data['PQ #'].unique())


data = data[data['PQ #'] != 'Pre-PQ Process']

# Verify the rows have been removed by checking unique values again
print("Unique values after:", data['PQ #'].unique())

data

print("Unique values before:", data['Vendor INCO Term'].unique())

data = data[data['Vendor INCO Term'] != 'N/A - From RDC']


print("Unique values after:", data['Vendor INCO Term'].unique())

data

# Check the unique values in the "PO Sent to Vendor Date" column before removal
print("Unique values before:", data['PO Sent to Vendor Date'].unique())

# Remove rows where "PO Sent to Vendor Date" is "Date Not Captured"
data = data[data['PO Sent to Vendor Date'] != 'Date Not Captured']

# Verify the rows have been removed by checking unique values again
print("Unique values after:", data['PO Sent to Vendor Date'].unique())

# Check the initial columns to confirm the presence of "Dosage Form" and "Dosage"
print("Initial columns:", data.columns)

# Remove the "Dosage Form" and "Dosage" columns
data.drop(['Dosage Form', 'Dosage'], axis=1, inplace=True)

# Verify the columns have been removed
print("Columns after removal:", data.columns)

data

# Check the unique values in the "Weight (Kilograms)" column before removal
print("Unique values before:", data['Weight (Kilograms)'].unique())

# Remove rows where "Weight (Kilograms)" is "Weight Captured Separately"
data = data[data['Weight (Kilograms)'] != 'Weight Captured Separately']

# Verify the rows have been removed by checking unique values again
print("Unique values after:", data['Weight (Kilograms)'].unique())

data

print("Sample values before:", data['Weight (Kilograms)'].head(20))

# Remove rows where "Weight (Kilograms)" starts with "See ASN"
data = data[~data['Weight (Kilograms)'].astype(str).str.startswith('See ASN')]

# Verify the rows have been removed by checking some examples again
print("Sample values after:", data['Weight (Kilograms)'].head(20))

data

print("Sample values before:", data['Freight Cost (USD)'].head(20))

# Remove rows where "Freight Cost (USD)" starts with "See ASN"
data = data[~data['Freight Cost (USD)'].astype(str).str.startswith('See ASN')]

# Verify the rows have been removed by checking some examples again
print("Sample values after:", data['Freight Cost (USD)'].head(20))

data

import matplotlib.pyplot as plt

data['PO Sent to Vendor Date'] = pd.to_datetime(data['PO Sent to Vendor Date'], errors='coerce')

# Filter out non-numeric 'Weight (Kilograms)' entries
data = data[pd.to_numeric(data['Weight (Kilograms)'], errors='coerce').notna()]
data['Weight (Kilograms)'] = pd.to_numeric(data['Weight (Kilograms)'], errors='coerce')

# Remove rows where either date or weight is NaN
data.dropna(subset=['PO Sent to Vendor Date', 'Weight (Kilograms)'], inplace=True)

# Extract the year from 'PO Sent to Vendor Date'
data['Year'] = data['PO Sent to Vendor Date'].dt.year

# Group by year and find the entry with the maximum weight per year
max_weights = data.loc[data.groupby('Year')['Weight (Kilograms)'].idxmax()]

# Plotting
plt.figure(figsize=(12, 8))
plt.plot(max_weights['PO Sent to Vendor Date'], max_weights['Weight (Kilograms)'], marker='o', linestyle='-')

# Annotate the PO Number on each point
for _, row in max_weights.iterrows():
    plt.annotate(row['PQ #'], (row['PO Sent to Vendor Date'], row['Weight (Kilograms)']),
                 textcoords="offset points", xytext=(0,5), ha='center')
    plt.annotate(f"{row['Weight (Kilograms)']} kg", (row['PO Sent to Vendor Date'], row['Weight (Kilograms)']),
                 textcoords="offset points", xytext=(5,-20), ha='center')

plt.title('Maximum Weight by Year with PO Number Annotation')
plt.xlabel('PO Sent to Vendor Date')
plt.ylabel('Weight (Kilograms)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Convert 'PO Sent to Vendor Date' to datetime
data['PO Sent to Vendor Date'] = pd.to_datetime(data['PO Sent to Vendor Date'], errors='coerce')

# Ensure numeric data for 'Weight (Kilograms)' and 'Freight Cost (USD)'
data['Weight (Kilograms)'] = pd.to_numeric(data['Weight (Kilograms)'], errors='coerce')
data['Freight Cost (USD)'] = pd.to_numeric(data['Freight Cost (USD)'].str.replace('[^0-9.]', '', regex=True), errors='coerce')

# Drop rows with NaN values in necessary columns
data.dropna(subset=['PO Sent to Vendor Date', 'Weight (Kilograms)', 'Freight Cost (USD)'], inplace=True)

# Extract the year from the date
data['Year'] = data['PO Sent to Vendor Date'].dt.year

# Find the PO with the highest weight each year
max_weight_data = data.loc[data.groupby('Year')['Weight (Kilograms)'].idxmax()]

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Bar positions
indices = range(len(max_weight_data))
width = 0.35  # Width of the bars

# Plotting two bars for each year side by side
bar1 = ax.bar(indices, max_weight_data['Weight (Kilograms)'], width, label='Weight (Kilograms)')
bar2 = ax.bar([i + width for i in indices], max_weight_data['Freight Cost (USD)'], width, label='Freight Cost (USD)')

ax.set_xlabel('Year')
ax.set_ylabel('Values')
ax.set_title('Highest Weight and Freight Cost by Year')
ax.set_xticks([i + width / 2 for i in indices])
ax.set_xticklabels(max_weight_data['Year'])
ax.legend()

plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Assuming 'data' is already loaded and preprocessed
# Here's how you can include a toggle for the legend.

# Define a handler for the button click event
def toggle_legend(event):
    leg = ax.get_legend()
    if leg.get_visible():
        leg.set_visible(False)
    else:
        leg.set_visible(True)
    plt.draw()

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))
line = ax.plot(max_weights['PO Sent to Vendor Date'], max_weights['Weight (Kilograms)'], marker='o', linestyle='-', label='Max Weight')
ax.legend()

# Add button for toggling the legend
ax_button = plt.axes([0.8, 0.0, 0.1, 0.05])  # Adjust the position and size as needed
button = Button(ax_button, 'Toggle Legend')
button.on_clicked(toggle_legend)

# Annotate the PO Number on each point
for _, row in max_weights.iterrows():
    ax.annotate(row['PQ #'], (row['PO Sent to Vendor Date'], row['Weight (Kilograms)']),
                textcoords="offset points", xytext=(0,5), ha='center')
    ax.annotate(f"{row['Weight (Kilograms)']} kg", (row['PO Sent to Vendor Date'], row['Weight (Kilograms)']),
                textcoords="offset points", xytext=(5,-20), ha='center')

ax.set_title('Maximum Weight by Year with PO Number Annotation')
ax.set_xlabel('PO Sent to Vendor Date')
ax.set_ylabel('Weight (Kilograms)')
ax.grid(True)
plt.tight_layout()
plt.show()

import pandas as pd


# Part 1: Descriptive statistics for numerical columns
def numerical_descriptive_statistics(data):
    return data.describe()

# Part 2: Count of unique values for categorical columns
def categorical_unique_counts(data):
    categorical_columns = data.select_dtypes(include=['object']).columns
    return {col: data[col].nunique() for col in categorical_columns}

# Part 3: Basic statistics for each country focusing on 'Line Item Value' and 'Line Item Quantity'
def country_specific_stats_corrected(data):
    # This makes sure we are using the correct column names, especially focusing on 'Country'
    if 'Country' in data.columns:
        return data.groupby('Country')[['Line Item Value', 'Line Item Quantity']].agg(['mean', 'sum', 'std'])
    else:
        return "Column 'Country' does not exist in the dataset"

# Example function calls (comment these out when providing the file to the user)
print(numerical_descriptive_statistics(data))
print(categorical_unique_counts(data))
print(country_specific_stats_corrected(data))

data.to_csv('/content/drive/MyDrive/newdata.csv')

import matplotlib.pyplot as plt
import seaborn as sns

# Set the aesthetics for the plots
sns.set(style="whitegrid")

# Function to create histograms for specified columns
def plot_histograms(data, columns, bins=30):
    fig, axes = plt.subplots(len(columns), 1, figsize=(10, 5 * len(columns)))
    if len(columns) == 1:
        axes = [axes]  # Make it iterable if there's only one plot
    for col, ax in zip(columns, axes):
        sns.histplot(data[col], bins=bins, kde=True, ax=ax)
        ax.set_title(f'Histogram of {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
    plt.tight_layout()
    plt.show()

# Function to create box plots for a specified column grouped by a category
def plot_boxplots(data, value_column, category_column):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x=category_column, y=value_column, data=data)
    plt.xticks(rotation=45)
    plt.title(f'Box Plot of {value_column} by {category_column}')
    plt.xlabel(category_column)
    plt.ylabel(value_column)
    plt.show()

# Function to create scatter plots to explore relationships between two variables
def plot_scatter(data, x_col, y_col):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x_col, y=y_col, data=data)
    plt.title(f'Scatter Plot of {x_col} vs. {y_col}')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.show()

# Example function calls (comment these out when providing the file to the user)
plot_histograms(data, ['Line Item Quantity', 'Line Item Value', 'Freight Cost (USD)'])
plot_boxplots(data, 'Line Item Value', 'Country')
plot_scatter(data, 'Line Item Quantity', 'Line Item Value')

import subprocess
import sys

# Install required packages
def install_packages():
    try:
        import pycountry
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'pycountry'])
        import pycountry  # Import after installation

install_packages()

# Now, you can safely import other modules and use pycountry
import pandas as pd
import plotly.express as px

# Assume further script continues...

import pandas as pd
import plotly.express as px
import pycountry

# Function to convert country names to ISO Alpha-3 country codes
def convert_countries_to_codes(country_names):
    codes = []
    for name in country_names:
        try:
            code = pycountry.countries.lookup(name).alpha_3
        except:
            # If a country does not match, add a None
            code = None
        codes.append(code)
    return codes



# Compute the maximum 'Line Item Value' for each country
max_line_item_by_country = data.groupby('Country')['Line Item Value'].max().reset_index()

# Adding ISO Alpha-3 codes to the DataFrame
max_line_item_by_country['Country Code'] = convert_countries_to_codes(max_line_item_by_country['Country'])

# Remove rows with None country codes if any
max_line_item_by_country = max_line_item_by_country.dropna(subset=['Country Code'])

# Create a choropleth map
def plot_choropleth_map(data):
    fig = px.choropleth(data,
                        locations='Country Code',
                        color='Line Item Value',
                        hover_name='Country',
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title='Maximum Line Item Value by Country')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

# Example function call (comment this out when providing the file to the user)
plot_choropleth_map(max_line_item_by_country)

import pandas as pd
import plotly.express as px
import pycountry
import subprocess
import sys

# Function to install required packages
def install_packages():
    try:
        import pycountry
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'pycountry'])
        global pycountry
        import pycountry  # Import after installation

install_packages()

# Function to convert country names to ISO Alpha-3 country codes
def convert_countries_to_codes(country_names):
    codes = []
    for name in country_names:
        try:
            code = pycountry.countries.lookup(name).alpha_3
        except:
            # If a country does not match, add a None
            code = None
        codes.append(code)
    return codes



# Compute the maximum 'Line Item Value' for each country
max_line_item_by_country = data.groupby('Country')['Line Item Value'].max().reset_index()

# Adding ISO Alpha-3 codes to the DataFrame
max_line_item_by_country['Country Code'] = convert_countries_to_codes(max_line_item_by_country['Country'])

# Remove rows with None country codes if any
max_line_item_by_country = max_line_item_by_country.dropna(subset=['Country Code'])

# Create a choropleth map with enhanced hover data
def plot_choropleth_map(data):
    title_text = 'Heat Map of Maximum Line Item Value by Country in USD'
    fig = px.choropleth(data,
                        locations='Country Code',
                        color='Line Item Value',
                        hover_name='Country',
                        hover_data={'Line Item Value': ':,.2f USD'},  # Formatting the hover data
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title='Maximum Line Item Value by Country')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

# Example function call
plot_choropleth_map(max_line_item_by_country)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming 'data' is your DataFrame loaded from a CSV or other source

# Step 1: Aggregate the maximum 'Line Item Value' for each country
max_line_item_by_country = data.groupby('Country')['Line Item Value'].max().reset_index()

# Step 2: Sort the data by 'Line Item Value' and select the top ten countries
top_countries = max_line_item_by_country.sort_values(by='Line Item Value', ascending=False).head(10)

# Step 3: Create the heatmap for only the top ten countries
def plot_top_countries_heatmap(max_values):
    # Reshape data
    values_array = max_values['Line Item Value'].values.reshape(-1, 1)
    formatted_values = [[f"{x:,.0f} USD"] for x in max_values['Line Item Value'].values]

    plt.figure(figsize=(10, 8))  # Adjust size based on the number of countries
    sns.heatmap(values_array, annot=formatted_values, fmt="", cmap='viridis',
                yticklabels=max_values['Country'].values, xticklabels=['Max Line Item Value'])
    plt.title('Heatmap of Maximum Line Item Value by Top 10 Countries')
    plt.show()

# Call the function with top country data
plot_top_countries_heatmap(top_countries)

import pandas as pd


# Calculate the average Unit Price for each Vendor INCO Term
average_prices = data.groupby('Vendor INCO Term')['Unit Price'].mean()

# Find the Vendor INCO Term with the lowest average Unit Price
best_term = average_prices.idxmin()
best_price = average_prices.min()

print(f"The best Vendor INCO Term based on lowest average Unit Price is: {best_term} with an average price of {best_price:.2f}")

import pandas as pd
import matplotlib.pyplot as plt


# Convert the date column to datetime and extract the year
data['PO Sent to Vendor Date'] = pd.to_datetime(data['PO Sent to Vendor Date'])
data['Year'] = data['PO Sent to Vendor Date'].dt.year

# Calculate the average Unit Price for each Vendor INCO Term per year
average_prices_by_year = data.groupby(['Vendor INCO Term', 'Year'])['Unit Price'].mean().unstack()

# Plotting the results
average_prices_by_year.plot(kind='bar', figsize=(14, 7))
plt.title('Average Unit Price by Vendor INCO Term Per Year')
plt.ylabel('Average Unit Price')
plt.xlabel('Vendor INCO Term')
plt.xticks(rotation=45)
plt.legend(title='Year')
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming 'data' is your DataFrame loaded from a CSV or other source
# data = pd.read_csv('path_to_your_data.csv')  # Uncomment and adjust the path as necessary

# Group data by 'Vendor' and sum the 'Line Item Value'
vendor_totals = data.groupby('Vendor')['Line Item Value'].sum()

# Sort the totals in descending order and select the top ten
top_ten_vendors = vendor_totals.sort_values(ascending=False).head(10)

# Plotting the results using a pie chart
plt.figure(figsize=(10, 8))
top_ten_vendors.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
plt.title('Top Ten Suppliers Based on Total Buying Value')
plt.ylabel('')  # Hide the 'Total Buying Value (USD)' label as it's redundant in pie charts
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Assuming 'data' is your DataFrame loaded from a CSV or other source
# data = pd.read_csv('path_to_your_data.csv')  # Uncomment and adjust the path as necessary

# Simplify 'Vendor' names to only the first name
data['Vendor First Name'] = data['Vendor'].apply(lambda x: x.split()[0] if pd.notnull(x) else x)

# Group data by the simplified 'Vendor' names and sum the 'Line Item Value'
vendor_totals = data.groupby('Vendor First Name')['Line Item Value'].sum()

# Sort the totals in descending order and select the top ten
top_ten_vendors = vendor_totals.sort_values(ascending=False).head(10)

# Plotting the results using a vertical heatmap (bar chart with colored bars)
plt.figure(figsize=(12, 8))
colors = plt.cm.viridis(np.linspace(0, 1, len(top_ten_vendors)))  # Generate a color map range
bars = plt.bar(top_ten_vendors.index, top_ten_vendors.values, color=colors)

plt.title('Top Ten Suppliers Based on Total Buying Value')
plt.xlabel('Vendor First Name')
plt.ylabel('Total Buying Value (USD)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt


# Ensure the date column is in datetime format
data['PO Sent to Vendor Date'] = pd.to_datetime(data['PO Sent to Vendor Date'])

# Filter data for the vendor "Orgenics, Ltd"
orgenics_data = data[data['Vendor'] == "Orgenics, Ltd"]

# Group by 'Product Group' and 'PO Sent to Vendor Date', and calculate the average unit price
price_trends = orgenics_data.groupby(['Product Group', 'PO Sent to Vendor Date'])['Unit Price'].mean().unstack()

# Plotting
plt.figure(figsize=(15, 10))
for product_group, values in price_trends.iterrows():
    plt.plot(values.index, values, marker='o', label=product_group)

plt.title('Change in Unit Price Over Time for Orgenics, Ltd Products')
plt.xlabel('Date')
plt.ylabel('Average Unit Price (USD)')
plt.legend(title='Product Group')
plt.grid(True)

# Annotation example (assuming some hypothetical insight around a particular date and price)
# Example: Highlighting a significant price spike in product group 'A'
if 'A' in price_trends.index:
    product_a_dates = price_trends.columns
    product_a_prices = price_trends.loc['A']
    # Hypothetically, let's say we want to annotate the highest price for product A
    highest_price_date = product_a_prices.idxmax()
    highest_price = product_a_prices.max()
    plt.annotate('Highest Price', xy=(highest_price_date, highest_price), xytext=(highest_price_date, highest_price + 5),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 horizontalalignment='center', verticalalignment='bottom')

plt.show()

import pandas as pd
import matplotlib.pyplot as plt


# Filter data for the vendor "Orgenics, Ltd"
orgenics_data = data[data['Vendor'] == "Orgenics, Ltd"]

# Group data by 'Product Group' and sum the 'Line Item Value'
total_buying = orgenics_data.groupby('Product Group')['Line Item Value'].sum()

# Plotting the results
plt.figure(figsize=(10, 6))
total_buying.plot(kind='bar', color='teal')
plt.title('Total Buying for Each Product in "Product Group" for Orgenics, Ltd')
plt.xlabel('Product Group')
plt.ylabel('Total Buying Value (USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
# data = pd.read_csv('path_to_your_file.csv')  # Uncomment this line and specify the path to your dataset.

# Convert date columns to datetime format
data['PQ First Sent to Client Date'] = pd.to_datetime(data['PQ First Sent to Client Date'])
data['Delivered to Client Date'] = pd.to_datetime(data['Delivered to Client Date'])

# Calculate the delivery time in days
data['Delivery Time (Days)'] = (data['Delivered to Client Date'] - data['PQ First Sent to Client Date']).dt.days

# Filter data for the vendor "Orgenics, Ltd" and specific shipment methods
orgenics_data = data[(data['Vendor'] == "Orgenics, Ltd") & (data['Shipment Mode'].isin(['AIR', 'Ocean']))]

# Group data by 'Shipment Mode' and calculate necessary statistics
shipment_analysis = orgenics_data.groupby('Shipment Mode').agg({
    'Line Item Value': 'sum',  # Total buying value
    'Delivery Time (Days)': 'mean',  # Average delivery time
    'Line Item Value': 'mean'  # Average cost is directly taken from 'Line Item Value'
})

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
shipment_analysis['Line Item Value'].plot(kind='bar', ax=ax, color='skyblue', title='Total Buying Value by Shipment Mode')
ax.set_xlabel('Shipment Mode')
ax.set_ylabel('Total Buying Value (USD)')
plt.xticks(rotation=0)
plt.show()

# Optional: Display additional statistics
print("Average Delivery Times by Shipment Mode:")
print(shipment_analysis['Delivery Time (Days)'])

