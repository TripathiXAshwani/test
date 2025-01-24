import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import seaborn as sns



# Load and display the CSV file

def main():
    st.title("🎈My Dashboard")
    st.write("Upload a CSV file and draw graphs!")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:

        data = pd.read_csv(uploaded_file)
        with st.spinner("Reading data, Wait a sec!!"):
            st.write("Preview of the data:")
            st.dataframe(data.head())  # Display the first 5 rows of the data
            
            # Automatically detect columns (you can modify this part)
            
            created_at_col= 'created_at' if 'created_at' in data.columns else None
            if created_at_col:
                data['created_at'] = pd.to_datetime(data['created_at'], errors='coerce', utc=True)
                # Extract year and month
                data['year'] = data['created_at'].dt.year
                data['month'] = data['created_at'].dt.month
            year_col= 'year' if 'year' in data.columns else None
            month_col ='month' if 'month' in data.columns else None

            product_col = 'product' if 'product' in data.columns else None
            if product_col is None:
                product_col=  'product_name' if 'product_name' in data.columns else None
            price_col = 'price' if 'price' in data.columns else None
            quantity_col = 'quantity' if 'quantity' in data.columns or 'Quantity' in data.columns else None
            brand_col = 'brand' if 'brand' in data.columns or 'brand_name' in data.columns else None
            color_col = 'color' if 'color' in data.columns else None
            if color_col is None:
                color_col= 'primary_color' if 'primary_color' in data.columns else None
            complaints_col = 'complaints' if 'complaints' in data.columns else None
            
            material_col= 'material' if 'material' in data.columns else None
            if material_col is None:
                material_col= 'primary_material' if 'primary_material' in data.columns else None
            # category_col = 'type_or_category'
            category_col = 'type_or_category' if 'type_or_category' in data.columns else None
            if category_col is None:
               category_col = 'category' if 'category' in data.columns else None
            
            
            


            # Define your analysis logic
            st.write(f"""{category_col}, {type(category_col)}""")
            st.write(" year_col-",year_col, " month_col-",month_col," category_col-",category_col," product_col-",product_col," price_col-",price_col," quantity_col-",quantity_col)
            st.write("complaint_call-",complaints_col," month_col-",month_col)
            st.dataframe(data.head())
            total_inventory=data['quantity'].sum()

            total_product_sold=0
            unique_brand=data['brand'].count()
            total_images=0
            total_files=0
            total_invoices_generated=0
            st.write(" unique_brands-",unique_brand)
            st.write(" total_inventory", total_inventory)


            
            # Year vs Total Sale (Line plot)
            # if year_col and quantity_col:
            #     yearly_sales = data.groupby(year_col)[quantity_col].sum().reset_index()
            #     fig = px.line(yearly_sales, x=year_col, y=quantity_col, title="Year vs Total Sales", 
            #                 labels={year_col: 'Year', quantity_col: 'Total Sales'})
            #     st.plotly_chart(fig)
            if 'year' in data.columns and 'quantity' in data.columns:
                # Group by year and calculate total sales
                yearly_sales = data.groupby('year')['quantity'].sum().reset_index()
                st.write("yearly_sales ---")
                st.write(yearly_sales)
                # Create the line plot
                fig = px.line(
                    yearly_sales,
                    x='year', 
                    y='quantity',
                    title="Year vs Total Sales", 
                    labels={'year': 'Year', 'quantity': 'Total Sales'}
                )
                st.plotly_chart(fig)

            # Year vs Product Price (Line plot)
            if year_col and price_col:
                year_price = data.groupby(year_col)[price_col].mean().reset_index()
                fig = px.line(year_price, x=year_col, y=price_col, title="Year vs  Average Product Price",
                            labels={year_col: 'Year', price_col: 'Average Price'})
                fig.update_traces(line_color='red')
                st.plotly_chart(fig)

            # Month vs Product Sale (Line plot)
            if month_col and quantity_col:
                monthly_sales = data.groupby(month_col)[quantity_col].sum().reset_index()
                fig = px.line(monthly_sales, x=month_col, y=quantity_col, title="Month vs Product Sales", 
                            labels={month_col: 'Month', quantity_col: 'Total Sales'})
                st.plotly_chart(fig)

            # Month vs Top Selling Products (Bar chart)
            if month_col and product_col and quantity_col:
                top_monthly_sales = data.groupby([month_col, product_col])[quantity_col].sum().reset_index()
                top_monthly_sales = top_monthly_sales.sort_values(by=quantity_col, ascending=False).head(20)
                fig = px.bar(top_monthly_sales, x=product_col, y=quantity_col, color=product_col,
                            title="Month vs Top Selling Products", labels={product_col: 'Product', quantity_col: 'Sales'},
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig)

            # Brand vs Price (Line plot)
            if brand_col and price_col:
                brand_price = data.groupby(brand_col)[price_col].mean().reset_index()
                fig = px.line(brand_price, x=brand_col, y=price_col, title="Brand vs Price",
                            labels={brand_col: 'Brand', price_col: 'Price'})
                st.plotly_chart(fig)

            # Year vs Complaints (Line plot)
            if year_col and complaints_col:
                year_complaints = data.groupby(year_col)[complaints_col].sum().reset_index()
                fig = px.line(year_complaints, x=year_col, y=complaints_col, title="Year vs Complaints", 
                            labels={year_col: 'Year', complaints_col: 'Complaints'})
                st.plotly_chart(fig)

            # Complaints divided by Product (Pie chart)
            if complaints_col and product_col:
                product_complaints = data.groupby(product_col)[complaints_col].sum().reset_index()
                fig = px.pie(product_complaints, names=product_col, values=complaints_col, 
                            title="Complaints by Product", color=product_complaints[complaints_col],
                            color_continuous_scale='Blues')
                st.plotly_chart(fig)
            
            if brand_col and quantity_col:
                brand_quantity = data.groupby(brand_col)[quantity_col].sum().reset_index()
                fig = px.bar(brand_quantity, x=brand_col, y=quantity_col, title="Total Quantity Sold per Brand", 
                            labels={brand_col: 'Brand', quantity_col: 'Quantity Sold'},
                            color=quantity_col,
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig)
            
            if product_col and quantity_col:
                top_products = data.groupby(product_col)[quantity_col].sum().reset_index().sort_values(by=quantity_col, ascending=False).head(100)
                
                # Use a color scale for better visualization
                fig = px.bar(top_products, 
                            x=quantity_col, 
                            y=product_col, 
                            orientation='h', 
                            title="Top 100 Products by Quantity Sold", 
                            color=quantity_col,  # Apply color based on quantity
                            color_continuous_scale='Viridis')  # Choose a color scale (e.g., 'Viridis', 'Cividis', 'Plasma', etc.)
                
                st.plotly_chart(fig)

            
            if product_col and quantity_col and price_col:
                data['revenue'] = data[price_col] * data[quantity_col]
                product_performance = data.groupby(product_col).agg(
                    total_quantity=(quantity_col, 'sum'),
                    total_revenue=('revenue', 'sum')
                ).reset_index()
                fig = px.scatter(product_performance, x='total_quantity', y='total_revenue', size='total_revenue', 
                                color='total_quantity', hover_name=product_col, title="Product Performance by Revenue and Quantity")
                st.plotly_chart(fig)

            # 4. Material Analysis
            # Donut chart for share of different materials used (need to fix)
            if material_col and quantity_col:
                material_sales = data.groupby(material_col)[quantity_col].sum().reset_index()
                fig = px.pie(material_sales, names=material_col, values=quantity_col, title="Material Share", 
                            hole=0.3)
                st.plotly_chart(fig)

            # 5. Complaints Insights
            # Heatmap for number of complaints per brand and product
            if complaints_col and brand_col and product_col:
                complaints_data = data.groupby([brand_col, product_col])[complaints_col].sum().reset_index()
                complaints_data_pivot = complaints_data.pivot(index=product_col, columns=brand_col, values=complaints_col)
                fig = sns.heatmap(complaints_data_pivot, annot=True, cmap="Blues", cbar_kws={'label': 'Complaints'})
                st.pyplot(fig)

            # 6. Category Analysis
            # Tree map for revenue distribution by categories
            if category_col and quantity_col and price_col:
                data['revenue'] = data[price_col] * data[quantity_col]
                category_revenue = data.groupby(category_col)['revenue'].sum().reset_index()
                fig = px.treemap(category_revenue, path=[category_col], values='revenue', title="Revenue Distribution by Categoriess")
                st.plotly_chart(fig)

            

            # Brand vs Color (Pie chart, only non-zero sales)
            # if brand_col and color_col:
            #     brand_colors = data.groupby(brand_col)[color_col].value_counts(normalize=True).unstack(fill_value=0)

            #     for brand, colors in brand_colors.iterrows():
            #         colors = colors[colors > 0]  # Filter out zero sales
            #         if not colors.empty:
            #             fig = go.Figure(data=[go.Pie(labels=colors.index, values=colors)])
            #             fig.update_layout(title=f"Color Distribution for Brand: {brand}")
            #             st.plotly_chart(fig)
            if brand_col and color_col:
                unique_brands = list(data[brand_col].astype(str).unique())
                
                tab_layout = st.tabs(unique_brands)

                for i, brand in enumerate(unique_brands):
                    with tab_layout[i]:
                        # Filter data for the current brand
                        brand_data = data[data[brand_col] == brand]
                        brand_color_distribution = (
                            brand_data[color_col]
                            .value_counts(normalize=True)
                            .reset_index(name='percentage')
                        )

                        # Check if data is valid
                        if brand_color_distribution.empty:
                            st.warning(f"No color data found for brand: {brand}")
                            continue

                        # Create pie chart, using the index as names
                        fig = px.pie(
                            brand_color_distribution,
                            names=brand_color_distribution.index,  # Use the index directly here
                            values='percentage',
                            title=f"Color Distribution for {brand}",
                            labels={'index': 'Color'},
                        )
                        st.plotly_chart(fig)

            
            # Brand vs Quantity (Bar chart with hover and colors)
            if brand_col and quantity_col:
                brand_quantity = data.groupby(brand_col)[quantity_col].sum().reset_index()
                fig = px.bar(
                    brand_quantity,
                    x=brand_col,
                    y=quantity_col,
                    title="Total Quantity Sold per Brand",
                    labels={brand_col: 'Brand', quantity_col: 'Quantity Sold'},
                    color=brand_quantity[quantity_col],  # Color bars based on quantity
                    color_continuous_scale='Viridis',  # Choose a color scale
                    hover_data=[brand_col, quantity_col],  # Display additional data on hover
                )
                fig.update_layout(
                    xaxis_title="Brand",
                    yaxis_title="Quantity Sold",
                    xaxis_tickangle=-45,  # Rotate x-axis labels to prevent overlap
                    autosize=True,
                    showlegend=False
                )
                st.plotly_chart(fig)

            if category_col and quantity_col:
                
                category_sales = data.groupby(category_col)[quantity_col].sum().reset_index()
                
                # Generate a pie chart
                fig = px.pie(category_sales, 
                            names=category_col, 
                            values=quantity_col, 
                            title="Total Product Sold vs Product Categories",
                            color=category_col,  # You can adjust the color scale as needed
                            color_discrete_sequence=px.colors.qualitative.Set3)  # Example color scheme
                st.plotly_chart(fig)

            

            # if category_col in data.columns and brand_col in data.columns and quantity_col in data.columns:
            #     # Get unique categories
            #     unique_categories = data[category_col].unique()
                
            #     # Loop through each category and plot a separate pie chart
            #     for category in unique_categories:
            #         # Filter data for the current category
            #         category_data = data[data[category_col] == category]
                    
            #         # Group by brand and sum the quantities sold
            #         brand_sales = category_data.groupby(brand_col)[quantity_col].sum().reset_index()
                    
            #         # Create the pie chart for this category vs brand
            #         fig = px.pie(brand_sales, 
            #                     names=brand_col, 
            #                     values=quantity_col, 
            #                     title=f"Brand Distribution in Category: {category}",
            #                     color=brand_col,  # Color by brand
            #                     color_discrete_sequence=px.colors.qualitative.Set3)  # Example color scheme
                    
            #         # Show the pie chart in Streamlit
            #         st.plotly_chart(fig)
            if category_col in data.columns and brand_col in data.columns and quantity_col in data.columns:
                # Get unique categories
                unique_categories = data[category_col].unique()
                
                # Create tabs for each category
                tabs = st.tabs([f"Category: {category}" for category in unique_categories])
                
                for i, category in enumerate(unique_categories):
                    with tabs[i]:
                        
                        # Filter data for the current category
                        category_data = data[data[category_col] == category]
                        with st.spinner(f"Loading data for category: {category}..."):
                            
                            # Group by brand and sum the quantities sold
                            brand_sales = category_data.groupby(brand_col)[quantity_col].sum().reset_index()
                            
                            # Create the pie chart for this category vs brand
                            fig = px.pie(
                                brand_sales, 
                                names=brand_col, 
                                values=quantity_col, 
                                title=f"Brand Distribution in Category: {category}",
                                color=brand_col,  # Color by brand
                                color_discrete_sequence=px.colors.qualitative.Set3  # Example color scheme
                            )
                            
                            # Show the pie chart in the corresponding tab with a unique key
                            st.plotly_chart(fig, key=f"pie_chart_{i}")



    else:
        st.write("Upload a CSV file and draw graphs!")


if __name__ == "__main__":
    main()