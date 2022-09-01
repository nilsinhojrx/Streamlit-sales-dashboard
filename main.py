import streamlit as st
from data import loadData, productline_sales, hourly_sales

st.set_page_config(page_title="Sales Dashboard",
                    page_icon=":bar_chart:",
                    layout="wide"
)

@st.cache
def get_data():
    data = loadData("supermarkt_sales.xlsx")
    return data
DATA = get_data()

# ----- Side Bar -------
city = st.sidebar.multiselect(
    "Select the City:",
    options=DATA["City"].unique(),
    default=DATA["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=DATA["Customer_type"].unique(),
    default=DATA["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=DATA["Gender"].unique(),
    default=DATA["Gender"].unique()
)
month = st.sidebar.multiselect(
    "Select the Month:",
    options=DATA["Month"].unique(),
    default=DATA["Month"].unique()
)
# ----- Data filtering -----
data_selection = DATA.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender & Month == @month"
)
# ----- Show the dataframe on the screen ----
#st.dataframe(data_selection)

# ----- Main Page -------
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#Top KPI's
left_column, middle_column, right_column = st.columns(3)

try:
    total_sales = int(data_selection["Total"].sum())
    average_rating = round(data_selection["Rating"].mean(), 1)
    average_sales_by_transaction = round(data_selection["Total"].mean(), 2)
    star_rating = ":star:" * int(round(average_rating, 0))

    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"US $ {total_sales:,}")
    with middle_column:
        st.subheader("Average Rating")
        st.subheader(f"{average_rating} {star_rating}")
    with right_column:
        st.subheader("Average Sales Per Transaction")
        st.subheader(f"US $ {average_sales_by_transaction}")
except ValueError:
    with left_column:
        st.subheader("Total Sales:")
        #st.subheader(f"US $ {total_sales:,}")
    with middle_column:
        st.subheader("Average Rating")
        #st.subheader(f"{average_rating} {star_rating}")
    with right_column:
        st.subheader("Average Sales Per Transaction")
        #st.subheader(f"US $ {average_sales_by_transaction}")


st.markdown("---")

# Sales by Product Line [Bar Chart]
sales_by_product_line = (
    data_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = productline_sales(sales_by_product_line)
fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
)

# Sales by Hour [Bar Chart]
sales_by_hour = (
    data_selection.groupby(by=["Hour"]).sum()[["Total"]].sort_values(by="Total")
)
fig_hour_sales = hourly_sales(sales_by_hour)
fig_hour_sales.update_layout(
    xaxis = dict(tickmode="linear"),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid=False)),
)

#-- Columns to display charts
left_column, right_column = st.columns(2)
#left_column.header("Sales By Hour")
left_column.plotly_chart(fig_hour_sales, use_container_width=True)
#right_column.header("Sales By Product Line")
right_column.plotly_chart(fig_product_sales, use_container_width=True)
