import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🎈 My new app")
st.write("Upload a CSV file and draw graphs!")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV into a Pandas DataFrame
    data = pd.read_csv(uploaded_file)

    st.write("Preview of the data:")
    st.write(data.head())  # Display the first 5 rows of the data

    # Select columns for plotting
    st.write("Choose columns for the X and Y axes:")
    columns = data.columns.tolist()
    
    x_axis = st.selectbox("X-axis", options=columns)
    y_axis = st.selectbox("Y-axis", options=columns)

    # Select graph type
    graph_type = st.selectbox(
        "Choose the type of graph to plot:",
        options=["Line", "Bar", "Scatter"]
    )

    if st.button("Generate Graph"):
        # Create a matplotlib figure
        fig, ax = plt.subplots()

        # Plot based on the selected graph type
        if graph_type == "Line":
            ax.plot(data[x_axis], data[y_axis], marker='o')
        elif graph_type == "Bar":
            ax.bar(data[x_axis], data[y_axis])
        elif graph_type == "Scatter":
            ax.scatter(data[x_axis], data[y_axis])

        # Customize the plot
        ax.set_title(f"{y_axis} vs {x_axis} ({graph_type} Plot)")
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)

        # Display the plot
        st.pyplot(fig)
else:
    st.write("Please upload a CSV file to proceed.")
