import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("🎈 My new app")
st.write("Upload a CSV file and draw graphs!")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    data=data = pd.read_csv(uploaded_file)


    # Column detection
    year_col = 'year' if 'year' in data.columns else None
    month_col = 'month' if 'month' in data.columns else None
    product_col = 'product' if 'product' in data.columns or 'product_name' in data.columns else None
    price_col = 'price' if 'price' in data.columns else None
    quantity_col = 'quantity' if 'quantity' in data.columns or 'Quantity' in data.columns else None
    brand_col = 'brand' if 'brand' in data.columns or 'brand_name' in data.columns else None
    color_col = 'color' if 'color' in data.columns else None
    if color_col is None:
        color_col = 'primary_color' if 'primary_color' in data.columns else None
    complaints_col = 'complaints' if 'complaints' in data.columns else None
    material_col = 'material' if 'material' in data.columns else None
    if material_col is None:
        material_col = 'primary_material' if 'primary_material' in data.columns else None
    category_col = 'type_or_category' if 'type_or_category' in data.columns else None
    if category_col is None:
        category_col = 'category' if 'category' in data.columns else None

    # Dashboard Title
    st.title("Product Analytics Dashboard")
    st.markdown("A comprehensive overview of sales, trends, and performance metrics.")

    # Key Metrics
    st.header("Key Metrics")
    if quantity_col and price_col:
        total_sold = data[quantity_col].sum()
        total_revenue = (data[quantity_col] * data[price_col]).sum()
        most_popular_product = data.groupby(product_col)[quantity_col].sum().idxmax()
        top_selling_brand = data.groupby(brand_col)[quantity_col].sum().idxmax()

        st.metric("Total Products Sold", total_sold)
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
        st.metric("Most Popular Product", most_popular_product)
        st.metric("Top Selling Brand", top_selling_brand)

    # Sales Trends
    if year_col and quantity_col:
        st.header("Sales Trends")
        yearly_sales = data.groupby(year_col)[quantity_col].sum().reset_index()
        fig = px.line(yearly_sales, x=year_col, y=quantity_col, title="Yearly Sales Trends")
        st.plotly_chart(fig)

    if month_col and quantity_col:
        monthly_sales = data.groupby(month_col)[quantity_col].sum().reset_index()
        fig = px.bar(monthly_sales, x=month_col, y=quantity_col, title="Monthly Sales Trends")
        st.plotly_chart(fig)

    # Brand and Color Analysis
    if brand_col and color_col and quantity_col:
        st.header("Brand and Color Analysis")
        brand_colors = data.groupby([brand_col, color_col])[quantity_col].sum().reset_index()
        for brand in data[brand_col].unique():
            brand_data = brand_colors[brand_colors[brand_col] == brand]
            fig = px.pie(brand_data, names=color_col, values=quantity_col, title=f"Color Distribution for {brand}")
            st.plotly_chart(fig)

    # Product Performance
    if product_col and quantity_col:
        st.header("Product Performance")
        top_products = data.groupby(product_col)[quantity_col].sum().nlargest(10).reset_index()
        fig = px.bar(top_products, x=quantity_col, y=product_col, orientation='h', title="Top 10 Products by Quantity Sold")
        st.plotly_chart(fig)

    # Material Analysis
    if material_col and quantity_col:
        st.header("Material Analysis")
        material_distribution = data.groupby(material_col)[quantity_col].sum().reset_index()
        fig = px.pie(material_distribution, names=material_col, values=quantity_col, title="Material Distribution")
        st.plotly_chart(fig)

    # Complaints Insights
    if complaints_col and brand_col and product_col:
        st.header("Complaints Insights")
        complaint_data = data.groupby([brand_col, product_col])[complaints_col].sum().unstack(fill_value=0)
        fig = px.imshow(complaint_data, title="Complaints by Brand and Product", labels=dict(x="Brand", y="Product"))
        st.plotly_chart(fig)

    # Category Analysis
    if category_col and quantity_col and price_col:
        st.header("Category Analysis")
        category_data = data.groupby(category_col).apply(lambda x: (x[quantity_col] * x[price_col]).sum()).reset_index()
        category_data.columns = [category_col, 'revenue']
        fig = px.treemap(category_data, path=[category_col], values='revenue', title="Revenue Distribution by Category")
        st.plotly_chart(fig)

else:
    st.write("Please upload a CSV file to proceed.")
