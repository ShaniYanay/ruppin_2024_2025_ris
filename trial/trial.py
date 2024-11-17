import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

data_file_dir = os.getcwd().replace("trial", "data_files")
data_file_path = os.path.join(data_file_dir, "mall_sales_data.csv")


def generate_normalized_sales_heatmap(csv_path):
    """
    Generates a heatmap showing normalized sales for different store types across months.

    Parameters:
    csv_path (str): Path to the CSV file containing mall sales data.
    """
    # Load the data
    df = pd.read_csv(csv_path)

    # Extract the month from the 'date' column with the correct format
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    df['month'] = df['date'].dt.month

    # Group by month and calculate average sales for each store type across all malls
    avg_sales = df.groupby('month')[
        ['sales_clothing', 'sales_restaurants', 'sales_cosmetics', 'sales_electronics']
    ].mean().reset_index()

    # Normalize sales data by dividing each category by its maximum value
    normalized_sales = avg_sales.copy()
    normalized_sales.iloc[:, 1:] = avg_sales.iloc[:, 1:].div(avg_sales.iloc[:, 1:].max())

    # Reshape data for heatmap
    # Reshape data for heatmap
    normalized_sales_melted = normalized_sales.melt(id_vars='month', var_name='store_type',
                                                    value_name='normalized_sales')
    heatmap_data = normalized_sales_melted.pivot(index="store_type", columns="month", values="normalized_sales")

    # Generate the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt=".2f", linewidths=0.5)
    plt.title('Normalized Sales by Store Type and Month')
    plt.xlabel('Month')
    plt.ylabel('Store Type')
    plt.xticks(ticks=range(12), labels=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
    plt.tight_layout()
    plt.show()


# Generate the heatmap with normalized sales data
generate_normalized_sales_heatmap(csv_path=data_file_path)
