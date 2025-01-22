import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# App title
st.title("📊 Dynamic Data Analytics App")
st.write("Upload your CSV file, and we'll analyze it automatically!")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load CSV data
    data = pd.read_csv(uploaded_file)
    st.write("**Preview of your data:**")
    st.write(data.head())

    # Convert columns to lowercase for consistency
    data.columns = map(str.lower, data.columns)

    # Identify key columns
    year_col = next((col for col in data.columns if "year" in col), None)
    month_col = next((col for col in data.columns if "month" in col), None)
    sales_col = next((col for col in data.columns if "sale" in col), None)
    price_col = next((col for col in data.columns if "price" in col), None)
    brand_col = next((col for col in data.columns if "brand" in col), None)
    color_col = next((col for col in data.columns if "color" in col), None)
    category_col = next((col for col in data.columns if "category" in col), None)
    quantity_col = next((col for col in data.columns if "quantity" in col), None)

    sns.set_palette("viridis")

    # Generate graphs based on detected columns

    # Brand Analysis
    if brand_col:
        st.subheader(f"Brand-Based Analysis")
        col1, col2 = st.columns(2)

        # Brand vs Color (Pie chart)
        if color_col:
            brand_colors = data.groupby(brand_col)[color_col].value_counts(normalize=True).unstack(fill_value=0)

            for brand, colors in brand_colors.iterrows():
                # Filter out colors with zero percentage
                colors = colors[colors > 0]

                if not colors.empty:  # Only plot if there are valid colors
                    fig, ax = plt.subplots(figsize=(4, 4))  # Smaller figure size
                    ax.pie(
                        colors,
                        labels=colors.index,
                        autopct='%1.1f%%',
                        startangle=90,
                        colors=sns.color_palette("pastel", len(colors))
                    )
                    ax.set_title(f"Color Distribution for Brand: {brand}", fontsize=10)
                    col1.pyplot(fig)
                    plt.close(fig)  # Close the figure

        # Brand vs Quantity (Bar chart)
        if quantity_col:
            brand_quantity = data.groupby(brand_col)[quantity_col].sum().reset_index()
            fig, ax = plt.subplots(figsize=(5, 3))  # Smaller figure size
            sns.barplot(data=brand_quantity, x=brand_col, y=quantity_col, ax=ax)
            ax.set_title("Total Quantity Sold per Brand", fontsize=10)
            ax.set_xlabel("Brand", fontsize=8)
            ax.set_ylabel("Quantity Sold", fontsize=8)
            ax.tick_params(axis='x', labelsize=8)
            col2.pyplot(fig)
            plt.close(fig)  # Close the figure

    # Color Analysis
    if color_col:
        st.subheader(f"Color-Based Analysis")
        col1, col2 = st.columns(2)

        # Color Popularity (Pie chart)
        color_counts = data[color_col].value_counts(normalize=True)
        fig, ax = plt.subplots(figsize=(4, 4))  # Smaller figure size
        ax.pie(
            color_counts,
            labels=color_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=sns.color_palette("pastel", len(color_counts))
        )
        ax.set_title("Color Popularity", fontsize=10)
        col1.pyplot(fig)
        plt.close(fig)  # Close the figure

        # Color vs Quantity (Bar chart)
        if quantity_col:
            color_quantity = data.groupby(color_col)[quantity_col].sum().reset_index()
            fig, ax = plt.subplots(figsize=(5, 3))  # Smaller figure size
            sns.barplot(data=color_quantity, x=color_col, y=quantity_col, ax=ax)
            ax.set_title("Quantity Sold by Color", fontsize=10)
            ax.set_xlabel("Color", fontsize=8)
            ax.set_ylabel("Quantity Sold", fontsize=8)
            ax.tick_params(axis='x', labelsize=8)
            col2.pyplot(fig)
            plt.close(fig)  # Close the figure

    # Category Analysis
    if category_col:
        st.subheader(f"Category-Based Analysis")

        # Category vs Quantity (Bar chart)
        if quantity_col:
            category_quantity = data.groupby(category_col)[quantity_col].sum().reset_index()
            fig, ax = plt.subplots(figsize=(5, 3))  # Smaller figure size
            sns.barplot(data=category_quantity, x=category_col, y=quantity_col, ax=ax)
            ax.set_title("Quantity Sold by Category", fontsize=10)
            ax.set_xlabel("Category", fontsize=8)
            ax.set_ylabel("Quantity Sold", fontsize=8)
            ax.tick_params(axis='x', labelsize=8)
            st.pyplot(fig)
            plt.close(fig)  # Close the figure

    # Quantity Analysis
    if quantity_col:
        st.subheader(f"Quantity-Based Analysis")

        # Histogram of Quantities
        fig, ax = plt.subplots(figsize=(5, 3))  # Smaller figure size
        sns.histplot(data[quantity_col], bins=10, kde=True, ax=ax)
        ax.set_title("Distribution of Quantities Sold", fontsize=10)
        ax.set_xlabel("Quantity", fontsize=8)
        st.pyplot(fig)
        plt.close(fig)  # Close the figure

else:
    st.write("Please upload a CSV file to see the analysis.")
