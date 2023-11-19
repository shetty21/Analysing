import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# Load the Excel file into a DataFrame
excel_file = "Streamlit.xlsx"
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
        st.write(filtered_df[["Institution","Parent Category", "Product Category", "Vendor & Product Name",
                               "FICE - Enrollment Range Rolled Up Current Year",
                               "FICE - Institution Type Rolled Up Current Year",
                               "FICE - Carnegie Classification 2021:Basic (HD 2021)"]])

        # Calculate the count of FICE institutions for each vendor
        vendor_counts = filtered_df.groupby(["Vendor & Product Name"])["FICE"].nunique().reset_index()

        # Display the bar chart using Plotly Express
        fig = px.bar(vendor_counts, x="Vendor & Product Name", y="FICE",
                      labels={"x": "Vendor & Product Name", "y": "Count of FICE Institutions"},
                      title="Vendors Purchased by Institutions")

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
        st.write(filtered_df[["Institution","Year Purchased", "Parent Category", "Product Category", "Vendor & Product Name"]])

        # Calculate the count of products for each year
        year_counts = filtered_df.groupby(["Year Purchased", "Parent Category"])["Vendor & Product Name"].count().reset_index()

        # Display the line chart using Plotly Express
        fig = px.line(year_counts, x="Year Purchased", y="Vendor & Product Name", color="Parent Category",
                      labels={"x": "Year Purchased", "y": "Count"}, title="Trend of Product Purchases (Yearwise)")

        # Display the chart
        st.plotly_chart(fig)

        # Download CSV button
        csv_download_button(filtered_df[["Institution","Year Purchased", "Parent Category", "Vendor & Product Name"]], "Download Filtered Data")

# Vendors Purchased by Institutions page
def top_vendors_by_institutions():
    st.title("Vendors Purchased by Institutions Page")

    # Sidebar filters
    selected_parent_categories = st.sidebar.multiselect("Select Parent Category", ['All'] + list(df["Parent Category"].unique()))
    selected_years = st.sidebar.multiselect("Select Year", ['All'] + sorted(df["Year Purchased"].unique()))
    selected_vendors = st.sidebar.multiselect("Select Vendor", ['All'] + sorted(df["Vendor Coded"].unique()))

    # Show button
    show_button = st.sidebar.button("Show")

    # Filter the DataFrame based on the selected categories only when the button is clicked
    if show_button:
        # Apply filter logic based on the selected categories
        filtered_df = df[
            (df["Parent Category"].isin(selected_parent_categories) | ('All' in selected_parent_categories)) &
            (df["Year Purchased"].isin(selected_years) | ('All' in selected_years)) &
            (df["Vendor Coded"].isin(selected_vendors) | ('All' in selected_vendors))
        ]

        # Display the filtered data in a table
        st.write("Showing data for selected categories:")
        st.write(filtered_df[["Institution","Parent Category", "Year Purchased", "Vendor Coded"]])

        # Calculate the count of FICE institutions for each vendor and parent category
        vendor_category_counts = filtered_df.groupby(["Vendor Coded", "Parent Category"])["FICE"].nunique().reset_index()

        # Display the bar chart using Plotly Express
        fig = px.bar(vendor_category_counts, x="Vendor Coded", y="FICE", color="Parent Category",
                      labels={"x": "Vendor Coded", "y": "Count of FICE Institutions"},
                      title="Distribution of Institutions Using Vendors")

        # Display the chart
        st.plotly_chart(fig)

        # Download CSV button
        csv_download_button(filtered_df, "Download Filtered Data")

# Vendor Purchases by Enrollment Range (Yearwise) page
def vendor_purchases_by_enrollment_range():
    st.title("Vendor Purchases by Enrollment Range Page")

    # Sidebar filters
    selected_years = st.sidebar.multiselect("Select Year", ['All'] + sorted(df["Year Purchased"].unique()))
    selected_parent_categories = st.sidebar.multiselect("Select Parent Category", ['All'] + list(df["Parent Category"].unique()))
    selected_vendors = st.sidebar.multiselect("Select Vendor", ['All'] + sorted(df["Vendor Coded"].unique()))
    selected_enrollment_ranges = st.sidebar.multiselect("Select Enrollment Range", ['All'] + list(df["FICE - Enrollment Range Rolled Up Current Year"].unique()))

    # Show button
    show_button = st.sidebar.button("Show")

    # Filter the DataFrame based on the selected categories only when the button is clicked
    if show_button:
        # Apply filter logic based on the selected categories
        filtered_df = df[
            (df["Year Purchased"].isin(selected_years) | ('All' in selected_years)) &
            (df["Parent Category"].isin(selected_parent_categories) | ('All' in selected_parent_categories)) &
            (df["Vendor Coded"].isin(selected_vendors) | ('All' in selected_vendors)) &
            (df["FICE - Enrollment Range Rolled Up Current Year"].isin(selected_enrollment_ranges) | ('All' in selected_enrollment_ranges))
        ]

        # Display the filtered data in a table
        st.write("Showing data for selected categories:")
        st.write(filtered_df[["Institution","Year Purchased", "FICE - Enrollment Range Rolled Up Current Year", "Vendor Coded"]])

        # Calculate the count of vendors for each year and enrollment range
        enrollment_range_counts = filtered_df.groupby(["Year Purchased", "FICE - Enrollment Range Rolled Up Current Year", "Vendor Coded"])["FICE"].nunique().reset_index()

        # Display the bar chart using Plotly Express
        fig = px.bar(enrollment_range_counts, x="Year Purchased", y="FICE", color="Vendor Coded",
                      facet_col="FICE - Enrollment Range Rolled Up Current Year",
                      labels={"x": "Year", "y": "Count of FICE Institutions"},
                      title="Vendor Purchases by Enrollment Range (Yearwise)",
                      height=500, width=1200)

        # Display the chart
        st.plotly_chart(fig)

        # Download CSV button
        csv_download_button(filtered_df, "Download Filtered Data")

# Vendor Purchases by Institution Type page
def vendor_purchases_by_institution_type():
    st.title("Vendor Purchases by Institution Type Page")

    # Sidebar filters
    selected_years = st.sidebar.multiselect("Select Year", ['All'] + sorted(df["Year Purchased"].unique()))
    selected_parent_categories = st.sidebar.multiselect("Select Parent Category", ['All'] + list(df["Parent Category"].unique()))
    selected_vendors = st.sidebar.multiselect("Select Vendor", ['All'] + sorted(df["Vendor Coded"].unique()))
    selected_institution_types = st.sidebar.multiselect("Select Institution Type", ['All'] + list(df["FICE - Institution Type Rolled Up Current Year"].unique()))

    # Show button
    show_button = st.sidebar.button("Show")

    # Filter the DataFrame based on the selected categories only when the button is clicked
    if show_button:
        # Apply filter logic based on the selected categories
        filtered_df = df[
            (df["Year Purchased"].isin(selected_years) | ('All' in selected_years)) &
            (df["Parent Category"].isin(selected_parent_categories) | ('All' in selected_parent_categories)) &
            (df["Vendor Coded"].isin(selected_vendors) | ('All' in selected_vendors)) &
            (df["FICE - Institution Type Rolled Up Current Year"].isin(selected_institution_types) | ('All' in selected_institution_types))
        ]

        # Display the filtered data in a table
        st.write("Showing data for selected categories:")
        st.write(filtered_df[["Institution","Year Purchased", "FICE - Institution Type Rolled Up Current Year", "Vendor Coded"]])

        # Calculate the count of vendors for each year and institution type
        institution_type_counts = filtered_df.groupby(["Year Purchased", "FICE - Institution Type Rolled Up Current Year", "Vendor Coded"])["FICE"].nunique().reset_index()

        # Display the bar chart using Plotly Express
        fig = px.bar(institution_type_counts, x="Year Purchased", y="FICE", color="Vendor Coded",
                      facet_col="FICE - Institution Type Rolled Up Current Year",
                      labels={"x": "Year", "y": "Count of FICE Institutions"},
                      title="Vendor Purchases by Institution Type",
                      height=500, width=1200)

        # Display the chart
        st.plotly_chart(fig)

        # Download CSV button
        csv_download_button(filtered_df, "Download Filtered Data")

import streamlit as st
import plotly.express as px

# Assuming 'df' is your DataFrame

def product_distribution():
    st.title("Product Distribution Page")

    # Sidebar filters
    selected_parent_categories = st.sidebar.multiselect("Select Parent Category", ['All'] + list(df["Parent Category"].unique()))

    # Update available vendors based on whether "All" is selected in parent category
    if 'All' in selected_parent_categories:
        available_vendors = df["Vendor Coded"].unique()
    else:
        available_vendors = df[df["Parent Category"].isin(selected_parent_categories)]["Vendor Coded"].unique()

    selected_vendors = st.sidebar.multiselect("Select Vendor", ['All'] + sorted(available_vendors))

    # Update available products based on whether "All" is selected in vendor
    if 'All' in selected_vendors:
        available_products = df["Vendor & Product Name"].unique()
    else:
        available_products = df[df["Vendor Coded"].isin(selected_vendors)]["Vendor & Product Name"].unique()

    selected_products = st.sidebar.multiselect("Select Product", ['All'] + sorted(available_products))

    selected_years = st.sidebar.multiselect("Select Year", ['All'] + sorted(df["Year Purchased"].unique()))

    # Show button
    show_button = st.sidebar.button("Show")

 # Filter the DataFrame based on the selected categories only when the button is clicked
    if show_button:
        # Apply filter logic based on the selected categories
        filtered_df = df[
            (df["Year Purchased"].isin(selected_years) | ('All' in selected_years)) &
            (df["Vendor Coded"].isin(selected_vendors) | ('All' in selected_vendors)) &
            (df["Vendor & Product Name"].isin(selected_products) | ('All' in selected_products)) &
            (df["Parent Category"].isin(selected_parent_categories) | ('All' in selected_parent_categories))
        ]

        # Display the filtered data in a table
        st.write("Showing data for selected categories:")
        st.write(filtered_df[["Institution","Vendor Coded", "Vendor & Product Name", "Parent Category"]])

        # Calculate the count of institutions for each vendor and product
        product_counts = filtered_df.groupby(["Vendor Coded", "Vendor & Product Name", "Parent Category"])["FICE"].nunique().reset_index()

        # Display the bar chart using Plotly Express
        fig = px.bar(product_counts, x="Vendor & Product Name", y="FICE", color="Parent Category",
                      labels={"x": "Product", "y": "Count of Institutions"},
                      title="Product Distribution",
                      height=700, width=1200)

        # Display the chart
        st.plotly_chart(fig)

        # Download CSV button
        csv_download_button(filtered_df, "Download Filtered Data")
# Main app
def main():
    st.sidebar.title("Menu")
    selected_page = st.sidebar.radio("Select a Page", ["Home", "Product Category Distribution", "Trend of Product Purchases (Yearwise)", "Vendor Distribution", "Vendor Purchases by Enrollment Range", "Vendor Purchases by Institution Type",
                                                        "Product Distribution"])

    if selected_page == "Home":
        home()
    elif selected_page == "Product Category Distribution":
        product_category_distribution()
    elif selected_page == "Trend of Product Purchases (Yearwise)":
        trend_of_product_purchases()
    elif selected_page == "Vendor Distribution":
        top_vendors_by_institutions()
    elif selected_page == "Vendor Purchases by Enrollment Range":
        vendor_purchases_by_enrollment_range()
    elif selected_page == "Vendor Purchases by Institution Type":
        vendor_purchases_by_institution_type()
    elif selected_page == "Product Distribution":
        product_distribution()

# Run the app
if __name__ == "__main__":
    main()

