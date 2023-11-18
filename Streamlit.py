import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# Load the Excel file into a DataFrame
excel_file = "/Users/shetty21/Downloads/Streamlit.xlsx"
df = pd.read_excel(excel_file, sheet_name='Sheet1')
df['FICE'] = pd.to_numeric(df['FICE'], errors='coerce')

# Function to create a download link for a DataFrame as a CSV file
def csv_download_button(dataframe, button_text):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to bytes
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">{button_text}</a>'
    st.markdown(href, unsafe_allow_html=True)

# Home page
def home():
    st.title("Welcome to the Home Page")
    st.write("This is the main page of the application.")

# Product category page
def product_category_distribution():
    st.title("Product Category Distribution Page")

    # Sidebar filters
    selected_parent_categories = st.sidebar.multiselect("Select Parent Category", ['All'] + list(df["Parent Category"].unique()))
    selected_product_categories = st.sidebar.multiselect("Select Product Category", ['All'] + list(df["Product Category"].unique()))
    selected_enrollment_ranges = st.sidebar.multiselect("Select Enrollment Range", ['All'] + list(df["FICE - Enrollment Range Rolled Up Current Year"].unique()))
    selected_institution_types = st.sidebar.multiselect("Select Institution Type", ['All'] + list(df["FICE - Institution Type Rolled Up Current Year"].unique()))
    selected_carnegie_classifications = st.sidebar.multiselect("Select Carnegie Classification", ['All'] + list(df["FICE - Carnegie Classification 2021:Basic (HD 2021)"].unique()))

    # Show button
    show_button = st.sidebar.button("Show")

    # Filter the DataFrame based on the selected categories only when the button is clicked
    if show_button:
        # Apply filter logic based on the selected categories
        filtered_df = df[
            (df["Parent Category"].isin(selected_parent_categories) | ('All' in selected_parent_categories)) &
            (df["Product Category"].isin(selected_product_categories) | ('All' in selected_product_categories)) &
            (df["FICE - Enrollment Range Rolled Up Current Year"].isin(selected_enrollment_ranges) | ('All' in selected_enrollment_ranges)) &
            (df["FICE - Institution Type Rolled Up Current Year"].isin(selected_institution_types) | ('All' in selected_institution_types)) &
            (df["FICE - Carnegie Classification 2021:Basic (HD 2021)"].isin(selected_carnegie_classifications) | ('All' in selected_carnegie_classifications))
        ]

        # Display the filtered data in a table
        st.write("Showing data for selected categories:")
        st.write(filtered_df[["Parent Category", "Product Category", "Vendor & Product Name",
                               "FICE - Enrollment Range Rolled Up Current Year",
                               "FICE - Institution Type Rolled Up Current Year",
                               "FICE - Carnegie Classification 2021:Basic (HD 2021)"]])

        # Calculate the count of products for each category
        category_counts = filtered_df.groupby(["Parent Category", "Product Category"])["Vendor & Product Name"].count().reset_index()

        # Display the line chart using Plotly Express
        fig = px.bar(category_counts, x="Parent Category", y="Vendor & Product Name", color="Product Category",
                      labels={"x": "Parent Category", "y": "Count"}, title="Product Category Distribution")

        # Display the chart
        st.plotly_chart(fig)

        # Download CSV button
        csv_download_button(filtered_df, "Download Filtered Data")

# Trend of Product Purchases (Yearwise) page
def trend_of_product_purchases():
    st.title("Trend of Product Purchases (Yearwise) Page")

    # Sidebar filters
    selected_years = st.sidebar.multiselect("Select Year", ['All'] + sorted(df["Year Purchased"].unique()))
    selected_parent_categories = st.sidebar.multiselect("Select Parent Category", ['All'] + list(df["Parent Category"].unique()))

    # Show button
    show_button = st.sidebar.button("Show")

    # Filter the DataFrame based on the selected categories only when the button is clicked
    if show_button:
        # Apply filter logic based on the selected categories
        filtered_df = df[
            (df["Year Purchased"].isin(selected_years) | ('All' in selected_years)) &
            (df["Parent Category"].isin(selected_parent_categories) | ('All' in selected_parent_categories))
        ]

        # Display the filtered data in a table
        st.write("Showing data for selected categories:")
        st.write(filtered_df[["Year Purchased", "Parent Category", "Product Category", "Vendor & Product Name"]])

        # Calculate the count of products for each year
        year_counts = filtered_df.groupby(["Year Purchased", "Parent Category"])["Vendor & Product Name"].count().reset_index()

        # Display the line chart using Plotly Express
        fig = px.line(year_counts, x="Year Purchased", y="Vendor & Product Name", color="Parent Category",
                      labels={"x": "Year Purchased", "y": "Count"}, title="Trend of Product Purchases (Yearwise)")

        # Display the chart
        st.plotly_chart(fig)

        # Download CSV button
        csv_download_button(filtered_df[["Year Purchased", "Parent Category", "Vendor & Product Name"]], "Download Filtered Data")
# New page for Top Vendors purchased by Institutions
def top_vendors_by_institutions():
    st.title("Top Vendors Purchased by Institutions Page")

    # Sidebar filters
    selected_vendors = st.sidebar.multiselect("Select Vendor", ['All'] + list(df["Vendor Coded"].unique()))
    selected_years = st.sidebar.multiselect("Select Year", ['All'] + sorted(df["Year Purchased"].unique()))
    selected_parent_categories = st.sidebar.multiselect("Select Parent Category", ['All'] + list(df["Parent Category"].unique()))

    # Show button
    show_button = st.sidebar.button("Show")

    # Filter the DataFrame based on the selected categories only when the button is clicked
    if show_button:
        # Apply filter logic based on the selected categories
        filtered_df = df[
            (df["Vendor Coded"].isin(selected_vendors) | ('All' in selected_vendors)) &
            (df["Year Purchased"].isin(selected_years) | ('All' in selected_years)) &
            (df["Parent Category"].isin(selected_parent_categories) | ('All' in selected_parent_categories))
        ]

        # Display the filtered data in a table
        st.write("Showing data for selected categories:")
        st.write(filtered_df[["Vendor Coded", "Year Purchased", "Parent Category"]])

        # Calculate the count of institutions for each vendor
        vendor_counts = filtered_df.groupby("Vendor Coded")["FICE"].nunique().reset_index()

        # Display the bar chart using Plotly Express
        fig = px.bar(vendor_counts, x="FICE", y="Vendor Coded", orientation='h',
                     labels={"x": "Count of Institutions", "y": "Vendor & Product Name"},
                     title="Top Vendors Purchased by Institutions")

        # Display the chart
        st.plotly_chart(fig)

        # Download CSV button
        csv_download_button(filtered_df[["Vendor Coded", "Year Purchased", "Parent Category", "FICE"]], "Download Filtered Data")

# Main app
def main():
    st.sidebar.title("Menu")
    selected_page = st.sidebar.radio("Select a Page", ["Home", "Product Category Distribution", "Trend of Product Purchases (Yearwise)", "Top Vendors Purchased by Institutions"])

    if selected_page == "Home":
        home()
    elif selected_page == "Product Category Distribution":
        product_category_distribution()
    elif selected_page == "Trend of Product Purchases (Yearwise)":
        trend_of_product_purchases()
    elif selected_page == "Top Vendors Purchased by Institutions":
        top_vendors_by_institutions()

# Run the app
if __name__ == "__main__":
    main()
