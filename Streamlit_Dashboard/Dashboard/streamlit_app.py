import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session


st.set_page_config(
    page_title="Real Estate Analytics",
    page_icon="🏠",
    layout="wide"
)



session = get_active_session()


st.title("🏠 Real Estate Analytics")
st.caption("Real Estate Analytics Platform")



# LOAD DATA FROM SNOWFLAKE

query = """
SELECT
    d.DATE_VALUE,

    c.CITY_NAME,
    c.REGION,
    c.CITY_CLASS,

    dev.DEVELOPER_ID,
    dev.DEVELOPER_NAME,
    dev.DEVELOPER_TIER,

    p.PROPERTY_ID,
    p.PROPERTY_TYPE,
    p.SEGMENT,
    p.BHK,
    p.AREA_SQFT,
    p.POSSESSION_YEAR,
    p.STATUS AS PROJECT_STATUS,

    f.CHANNEL,
    f.TXN_STATUS,
    f.SALE_PRICE,
    f.DISCOUNT_PCT

FROM REAL_ESTATE_ANALYTICS.DW.FACT_TRANSACTION AS f

JOIN REAL_ESTATE_ANALYTICS.DW.DIM_DATE AS d
    ON f.SK_TXN_DATE = d.SK_DATE

JOIN REAL_ESTATE_ANALYTICS.DW.DIM_CITY AS c
    ON f.SK_CITY = c.SK_CITY

JOIN REAL_ESTATE_ANALYTICS.DW.DIM_DEVELOPER AS dev
    ON f.SK_DEVELOPER = dev.SK_DEVELOPER

JOIN REAL_ESTATE_ANALYTICS.DW.DIM_PROPERTY AS p
    ON f.SK_PROPERTY = p.SK_PROPERTY
"""

df = session.sql(query).to_pandas()


# PREPARE DATE COLUMN

df["DATE_VALUE"] = pd.to_datetime(df["DATE_VALUE"])



# SIDEBAR

st.sidebar.title("🔎 Filters")



# DASHBOARD PAGE

page = st.sidebar.radio(
    "Dashboard Page",
    [
        "Executive Summary",
        "City Insights",
        "Developer Performance",
        "Property Explorer"
    ]
)



# DATE FILTER

min_date = df["DATE_VALUE"].min().date()
max_date = df["DATE_VALUE"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)



# CITY FILTER

cities = ["All"] + sorted(
    df["CITY_NAME"].dropna().unique().tolist()
)

selected_city = st.sidebar.selectbox(
    "City",
    cities
)



# REGION FILTER

regions = ["All"] + sorted(
    df["REGION"].dropna().unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Region",
    regions
)



# CITY CLASS FILTER

city_classes = ["All"] + sorted(
    df["CITY_CLASS"].dropna().unique().tolist()
)

selected_city_class = st.sidebar.selectbox(
    "City Class",
    city_classes
)



# DEVELOPER FILTER

developers = ["All"] + sorted(
    df["DEVELOPER_NAME"].dropna().unique().tolist()
)

selected_developer = st.sidebar.selectbox(
    "Developer",
    developers
)



# SEGMENT FILTER

segments = ["All"] + sorted(
    df["SEGMENT"].dropna().unique().tolist()
)

selected_segment = st.sidebar.selectbox(
    "Segment",
    segments
)



# PROPERTY TYPE FILTER

property_types = ["All"] + sorted(
    df["PROPERTY_TYPE"].dropna().unique().tolist()
)

selected_property_type = st.sidebar.selectbox(
    "Property Type",
    property_types
)



# PROJECT STATUS FILTER

project_statuses = ["All"] + sorted(
    df["PROJECT_STATUS"].dropna().unique().tolist()
)

selected_project_status = st.sidebar.selectbox(
    "Project Status",
    project_statuses
)



# CHANNEL FILTER

channels = ["All"] + sorted(
    df["CHANNEL"].dropna().unique().tolist()
)

selected_channel = st.sidebar.selectbox(
    "Channel",
    channels
)



# TRANSACTION STATUS FILTER

transaction_statuses = ["All"] + sorted(
    df["TXN_STATUS"].dropna().unique().tolist()
)

selected_transaction_status = st.sidebar.selectbox(
    "Transaction Status",
    transaction_statuses
)



# APPLY FILTERS

filtered_df = df.copy()



# DATE

if len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["DATE_VALUE"].dt.date >= start_date)
        & (filtered_df["DATE_VALUE"].dt.date <= end_date)
    ]



# CITY

if selected_city != "All":

    filtered_df = filtered_df[
        filtered_df["CITY_NAME"] == selected_city
    ]



# REGION

if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["REGION"] == selected_region
    ]


# CITY CLASS

if selected_city_class != "All":

    filtered_df = filtered_df[
        filtered_df["CITY_CLASS"] == selected_city_class
    ]



# DEVELOPER

if selected_developer != "All":

    filtered_df = filtered_df[
        filtered_df["DEVELOPER_NAME"] == selected_developer
    ]



# SEGMENT

if selected_segment != "All":

    filtered_df = filtered_df[
        filtered_df["SEGMENT"] == selected_segment
    ]



# PROPERTY TYPE

if selected_property_type != "All":

    filtered_df = filtered_df[
        filtered_df["PROPERTY_TYPE"] == selected_property_type
    ]



# PROJECT STATUS

if selected_project_status != "All":

    filtered_df = filtered_df[
        filtered_df["PROJECT_STATUS"] == selected_project_status
    ]


# ---------------------------------------------------------
# CHANNEL
# ---------------------------------------------------------
if selected_channel != "All":

    filtered_df = filtered_df[
        filtered_df["CHANNEL"] == selected_channel
    ]


# ---------------------------------------------------------
# TRANSACTION STATUS
# ---------------------------------------------------------
if selected_transaction_status != "All":

    filtered_df = filtered_df[
        filtered_df["TXN_STATUS"] == selected_transaction_status
    ]


# =========================================================
# EXECUTIVE SUMMARY
# =========================================================
if page == "Executive Summary":

    st.header("Executive Summary")

    # -----------------------------------------------------
    # KPI CALCULATIONS
    # -----------------------------------------------------
    total_transactions = len(filtered_df)

    total_sales = filtered_df["SALE_PRICE"].sum()

    if total_transactions > 0:

        avg_sale_price = filtered_df["SALE_PRICE"].mean()

        avg_discount = filtered_df["DISCOUNT_PCT"].mean()

        cancellation_rate = (
            (filtered_df["TXN_STATUS"] == "CANCELLED").sum()
            / total_transactions
        ) * 100

    else:

        avg_sale_price = 0
        avg_discount = 0
        cancellation_rate = 0


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Transactions",
            f"{total_transactions:,}"
        )

    with col2:
        st.metric(
            "Total Sales (Lakhs)",
            f"{total_sales:,.2f}"
        )

    with col3:
        st.metric(
            "Average Sale Price",
            f"{avg_sale_price:,.2f}"
        )

    with col4:
        st.metric(
            "Average Discount %",
            f"{avg_discount:.2f}%"
        )

    with col5:
        st.metric(
            "Cancellation Rate",
            f"{cancellation_rate:.2f}%"
        )


    st.divider()


    # -----------------------------------------------------
    # SALES TREND
    # -----------------------------------------------------
    st.subheader("Sales Trend")

    sales_trend = (
        filtered_df
        .groupby("DATE_VALUE", as_index=False)["SALE_PRICE"]
        .sum()
        .sort_values("DATE_VALUE")
    )

    if not sales_trend.empty:

        st.line_chart(
            sales_trend.set_index("DATE_VALUE")["SALE_PRICE"]
        )

    else:

        st.info(
            "No sales data available for the selected filters."
        )


    # -----------------------------------------------------
    # TRANSACTION STATUS
    # -----------------------------------------------------
    st.subheader("Transaction Status")

    status_df = (
        filtered_df
        .groupby("TXN_STATUS")
        .size()
        .reset_index(name="TRANSACTION_COUNT")
    )

    if not status_df.empty:

        st.bar_chart(
            status_df.set_index("TXN_STATUS")[
                "TRANSACTION_COUNT"
            ]
        )

    else:

        st.info(
            "No transaction data available for the selected filters."
        )


# =========================================================
# CITY INSIGHTS
# =========================================================
elif page == "City Insights":

    st.header("City Insights")

    st.caption(
        "Sales analysis by city, region, city class, and segment"
    )


    # -----------------------------------------------------
    # SALES BY CITY
    # -----------------------------------------------------
    st.subheader("Sales by City")

    city_sales = (
        filtered_df
        .groupby("CITY_NAME", as_index=False)
        .agg(
            TOTAL_SALES=("SALE_PRICE", "sum"),
            TRANSACTION_COUNT=("SALE_PRICE", "count")
        )
        .sort_values(
            "TOTAL_SALES",
            ascending=False
        )
    )

    if not city_sales.empty:

        st.bar_chart(
            city_sales.set_index("CITY_NAME")[
                "TOTAL_SALES"
            ]
        )

        st.dataframe(
            city_sales,
            width="stretch"
        )

    else:

        st.info(
            "No city data available for the selected filters."
        )


    st.divider()


    # -----------------------------------------------------
    # SALES BY REGION
    # -----------------------------------------------------
    st.subheader("Sales by Region")

    region_sales = (
        filtered_df
        .groupby("REGION", as_index=False)
        .agg(
            TOTAL_SALES=("SALE_PRICE", "sum"),
            TRANSACTION_COUNT=("SALE_PRICE", "count")
        )
        .sort_values(
            "TOTAL_SALES",
            ascending=False
        )
    )

    if not region_sales.empty:

        st.bar_chart(
            region_sales.set_index("REGION")[
                "TOTAL_SALES"
            ]
        )

    else:

        st.info(
            "No region data available."
        )


    # -----------------------------------------------------
    # SALES BY CITY CLASS
    # -----------------------------------------------------
    st.subheader("Sales by City Class")

    city_class_sales = (
        filtered_df
        .groupby("CITY_CLASS", as_index=False)
        .agg(
            TOTAL_SALES=("SALE_PRICE", "sum"),
            TRANSACTION_COUNT=("SALE_PRICE", "count")
        )
        .sort_values(
            "TOTAL_SALES",
            ascending=False
        )
    )

    if not city_class_sales.empty:

        st.bar_chart(
            city_class_sales.set_index("CITY_CLASS")[
                "TOTAL_SALES"
            ]
        )

    else:

        st.info(
            "No city-class data available."
        )


    st.divider()


    # -----------------------------------------------------
    # SEGMENT MIX
    # -----------------------------------------------------
    st.subheader("Segment Mix")

    segment_mix = (
        filtered_df
        .groupby("SEGMENT", as_index=False)
        .agg(
            TOTAL_SALES=("SALE_PRICE", "sum"),
            TRANSACTION_COUNT=("SALE_PRICE", "count")
        )
        .sort_values(
            "TOTAL_SALES",
            ascending=False
        )
    )

    if not segment_mix.empty:

        st.bar_chart(
            segment_mix.set_index("SEGMENT")[
                "TOTAL_SALES"
            ]
        )

        st.dataframe(
            segment_mix,
            width="stretch"
        )

    else:

        st.info(
            "No segment data available."
        )


# =========================================================
# DEVELOPER PERFORMANCE
# =========================================================
elif page == "Developer Performance":

    st.header("Developer Performance")

    st.caption(
        "Developer sales, transaction volume, and project status analysis"
    )


    # -----------------------------------------------------
    # TOP DEVELOPERS BY SALES VALUE
    # -----------------------------------------------------
    st.subheader("Top Developers by Sales Value")

    developer_sales = (
        filtered_df
        .groupby(
            ["DEVELOPER_NAME", "DEVELOPER_TIER"],
            as_index=False
        )
        .agg(
            TOTAL_SALES=("SALE_PRICE", "sum"),
            TRANSACTION_COUNT=("SALE_PRICE", "count")
        )
        .sort_values(
            "TOTAL_SALES",
            ascending=False
        )
    )

    if not developer_sales.empty:

        st.bar_chart(
            developer_sales
            .set_index("DEVELOPER_NAME")[
                "TOTAL_SALES"
            ]
        )

        st.dataframe(
            developer_sales,
            width="stretch"
        )

    else:

        st.info(
            "No developer data available for the selected filters."
        )


    st.divider()


    # -----------------------------------------------------
    # TOP DEVELOPERS BY TRANSACTION VOLUME
    # -----------------------------------------------------
    st.subheader("Top Developers by Transaction Volume")

    developer_volume = (
        filtered_df
        .groupby(
            "DEVELOPER_NAME",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "TRANSACTION_COUNT"
            }
        )
        .sort_values(
            "TRANSACTION_COUNT",
            ascending=False
        )
    )

    if not developer_volume.empty:

        st.bar_chart(
            developer_volume
            .set_index("DEVELOPER_NAME")[
                "TRANSACTION_COUNT"
            ]
        )

    else:

        st.info(
            "No transaction data available for the selected filters."
        )


    st.divider()


    # -----------------------------------------------------
    # PROJECT STATUS MIX
    # -----------------------------------------------------
    st.subheader("Project Status Mix")

    project_status_mix = (
        filtered_df
        .groupby(
            "PROJECT_STATUS",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "PROPERTY_COUNT"
            }
        )
        .sort_values(
            "PROPERTY_COUNT",
            ascending=False
        )
    )

    if not project_status_mix.empty:

        st.bar_chart(
            project_status_mix
            .set_index("PROJECT_STATUS")[
                "PROPERTY_COUNT"
            ]
        )

        st.dataframe(
            project_status_mix,
            width="stretch"
        )

    else:

        st.info(
            "No project status data available for the selected filters."
        )


# =========================================================
# PROPERTY EXPLORER
# =========================================================
elif page == "Property Explorer":

    st.header("Property Explorer")

    st.caption(
        "Explore properties by type, segment, BHK, area, possession year, and project status"
    )


    # -----------------------------------------------------
    # PROPERTY SUMMARY
    # -----------------------------------------------------
    property_count = filtered_df["PROPERTY_ID"].nunique()

    property_type_count = (
        filtered_df["PROPERTY_TYPE"].nunique()
    )

    segment_count = (
        filtered_df["SEGMENT"].nunique()
    )

    avg_area = (
        filtered_df["AREA_SQFT"].mean()
        if not filtered_df.empty
        else 0
    )


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Properties in Selection",
            f"{property_count:,}"
        )

    with col2:
        st.metric(
            "Property Types",
            f"{property_type_count:,}"
        )

    with col3:
        st.metric(
            "Segments",
            f"{segment_count:,}"
        )

    with col4:
        st.metric(
            "Average Area (Sq Ft)",
            f"{avg_area:,.2f}"
        )


    st.divider()


    # -----------------------------------------------------
    # PROPERTY TYPE
    # -----------------------------------------------------
    st.subheader("Properties by Type")

    property_type_df = (
        filtered_df
        .groupby(
            "PROPERTY_TYPE",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "PROPERTY_COUNT"
            }
        )
        .sort_values(
            "PROPERTY_COUNT",
            ascending=False
        )
    )

    if not property_type_df.empty:

        st.bar_chart(
            property_type_df
            .set_index("PROPERTY_TYPE")[
                "PROPERTY_COUNT"
            ]
        )

    else:

        st.info(
            "No property type data available."
        )


    # -----------------------------------------------------
    # SEGMENT
    # -----------------------------------------------------
    st.subheader("Properties by Segment")

    property_segment_df = (
        filtered_df
        .groupby(
            "SEGMENT",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "PROPERTY_COUNT"
            }
        )
        .sort_values(
            "PROPERTY_COUNT",
            ascending=False
        )
    )

    if not property_segment_df.empty:

        st.bar_chart(
            property_segment_df
            .set_index("SEGMENT")[
                "PROPERTY_COUNT"
            ]
        )

    else:

        st.info(
            "No segment data available."
        )


    # -----------------------------------------------------
    # BHK
    # -----------------------------------------------------
    st.subheader("Properties by BHK")

    bhk_df = (
        filtered_df
        .groupby(
            "BHK",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "PROPERTY_COUNT"
            }
        )
        .sort_values(
            "BHK"
        )
    )

    if not bhk_df.empty:

        st.bar_chart(
            bhk_df
            .set_index("BHK")[
                "PROPERTY_COUNT"
            ]
        )

    else:

        st.info(
            "No BHK data available."
        )


    # -----------------------------------------------------
    # POSSESSION YEAR
    # -----------------------------------------------------
    st.subheader("Properties by Possession Year")

    possession_df = (
        filtered_df
        .groupby(
            "POSSESSION_YEAR",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "PROPERTY_COUNT"
            }
        )
        .sort_values(
            "POSSESSION_YEAR"
        )
    )

    if not possession_df.empty:

        st.bar_chart(
            possession_df
            .set_index("POSSESSION_YEAR")[
                "PROPERTY_COUNT"
            ]
        )

    else:

        st.info(
            "No possession-year data available."
        )


    st.divider()


    # -----------------------------------------------------
    # PROPERTY DETAILS
    # -----------------------------------------------------
    st.subheader("Property Details")

    property_details = (
        filtered_df[
            [
                "PROPERTY_ID",
                "PROPERTY_TYPE",
                "SEGMENT",
                "BHK",
                "AREA_SQFT",
                "POSSESSION_YEAR",
                "CITY_NAME",
                "DEVELOPER_NAME",
                "PROJECT_STATUS"
            ]
        ]
        .drop_duplicates()
        .sort_values("PROPERTY_ID")
    )

    if not property_details.empty:

        st.dataframe(
            property_details,
            width="stretch"
        )

    else:

        st.info(
            "No properties available for the selected filters."
        )