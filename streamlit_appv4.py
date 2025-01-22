import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Sidebar for file upload
st.sidebar.title("📂 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Main Title
st.title("📊 Interactive Analytics Dashboard")
st.markdown("Upload your CSV file to generate professional insights and visualizations.")

if uploaded_file:
    # Load and display the CSV file
    data = pd.read_csv(uploaded_file)
    st.markdown("### Data Preview")
    st.dataframe(data.head(10))  # Show the first 10 rows of the data
    
    # Automatically detect columns
    year_col = 'year' if 'year' in data.columns else None
    product_col = 'product' if 'product' in data.columns or 'product_name' in data.columns else None
    price_col = 'price' if 'price' in data.columns else None
    quantity_col = 'quantity' if 'quantity' in data.columns or 'Quantity' in data.columns else None
    brand_col = 'brand' if 'brand' in data.columns or 'brand_name' in data.columns else None
    color_col = 'color' if 'color' in data.columns else ('primary_color' if 'primary_color' in data.columns else None)
    complaints_col = 'complaints' if 'complaints' in data.columns else None
    month_col = 'month' if 'month' in data.columns else None
    material_col = 'material' if 'material' in data.columns else ('primary_material' if 'primary_material' in data.columns else None)
    category_col = 'type_or_category' if 'type_or_category' in data.columns else ('category' if 'category' in data.columns else None)
    
    # Display detected columns
    with st.sidebar.expander("Detected Columns", expanded=True):
        st.write(f"Year: {year_col}, Product: {product_col}, Price: {price_col}, Quantity: {quantity_col}")
        st.write(f"Brand: {brand_col}, Color: {color_col}, Complaints: {complaints_col}")
        st.write(f"Month: {month_col}, Material: {material_col}, Category: {category_col}")

    # Create Expander Sections for Analysis
    with st.expander("📈 Yearly Trends", expanded=True):
        st.subheader("Yearly Analysis")
        col1, col2 = st.columns(2)

        if year_col and quantity_col:
            yearly_sales = data.groupby(year_col)[quantity_col].sum().reset_index()
            fig = px.line(yearly_sales, x=year_col, y=quantity_col, title="Year vs Total Sales")
            col1.plotly_chart(fig, use_container_width=True)

        if year_col and price_col:
            year_price = data.groupby(year_col)[price_col].mean().reset_index()
            fig = px.line(year_price, x=year_col, y=price_col, title="Year vs Average Product Price")
            col2.plotly_chart(fig, use_container_width=True)

    with st.expander("📅 Monthly Trends", expanded=False):
        st.subheader("Monthly Analysis")
        col1, col2 = st.columns(2)

        if month_col and quantity_col:
            monthly_sales = data.groupby(month_col)[quantity_col].sum().reset_index()
            fig = px.line(monthly_sales, x=month_col, y=quantity_col, title="Month vs Product Sales")
            col1.plotly_chart(fig, use_container_width=True)

        if month_col and product_col and quantity_col:
            top_monthly_sales = data.groupby([month_col, product_col])[quantity_col].sum().reset_index()
            top_monthly_sales = top_monthly_sales.sort_values(by=quantity_col, ascending=False).head(10)
            fig = px.bar(top_monthly_sales, x=product_col, y=quantity_col, color=product_col,
                         title="Top Selling Products by Month", labels={product_col: 'Product'})
            col2.plotly_chart(fig, use_container_width=True)

    with st.expander("🏷️ Brand Insights", expanded=False):
        st.subheader("Brand Analysis")
        col1, col2 = st.columns(2)

        if brand_col and price_col:
            brand_price = data.groupby(brand_col)[price_col].mean().reset_index()
            fig = px.bar(brand_price, x=brand_col, y=price_col, title="Brand vs Average Price")
            col1.plotly_chart(fig, use_container_width=True)

        if brand_col and quantity_col:
            brand_quantity = data.groupby(brand_col)[quantity_col].sum().reset_index()
            fig = px.bar(brand_quantity, x=brand_col, y=quantity_col, title="Brand vs Total Quantity Sold",
                         color=brand_quantity[quantity_col])
            col2.plotly_chart(fig, use_container_width=True)

    with st.expander("🎨 Product Categories", expanded=False):
        st.subheader("Category Analysis")
        if category_col and quantity_col:
            category_sales = data.groupby(category_col)[quantity_col].sum().reset_index()
            fig = px.pie(category_sales, names=category_col, values=quantity_col,
                         title="Total Sales by Category")
            st.plotly_chart(fig, use_container_width=True)

        if category_col and brand_col and quantity_col:
            unique_categories = data[category_col].unique()
            for category in unique_categories:
                category_data = data[data[category_col] == category]
                brand_sales = category_data.groupby(brand_col)[quantity_col].sum().reset_index()
                fig = px.pie(brand_sales, names=brand_col, values=quantity_col,
                             title=f"Brand Distribution in {category}")
                st.plotly_chart(fig, use_container_width=True)

else:
    st.write("### Please upload a CSV file to start analyzing.")
