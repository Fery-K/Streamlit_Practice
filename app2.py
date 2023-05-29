import streamlit as st
import pandas as pd
import altair as alt
# from numerize import numerize

st.set_page_config(page_title=
                   "Belajar Streamlit Lagi", layout="wide")

st.title("Dashboard Superstore Orders")

df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQMqC_6fkaH6oZweJDIIYFDdE9o3P3G1hB0OKLzkGGf0pB-"
                 "FjWJoAMoYca2iXV2ID5dE7hoklCSx6hE/pub?gid=0&single=true&output=csv")
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

df['order_year'] = df['order_date'].dt.year
CURR_YEAR = df['order_year'].max()
PREV_YEAR = CURR_YEAR - 1

data = pd.pivot_table(
    data=df,
    index="order_year",
    aggfunc={
        'sales': 'sum',
        'profit': 'sum',
        'order_id': pd.Series.nunique,
        'customer_id': pd.Series.nunique
    }
).reset_index()

data['gpm'] = 100 * data['profit'] / data['sales']

mx_sales, mx_order, mx_customer, mx_gpm = st.columns(4)
with mx_sales:
    curr_sales = data.loc[data['order_year'] == CURR_YEAR, 'sales'].values[0]
    prev_sales = data.loc[data['order_year'] == PREV_YEAR, 'sales'].values[0]
    sales_diff_pct = 100 * (curr_sales - prev_sales) / prev_sales

    st.metric(label="Sales",
              value=curr_sales,
              delta=f'{sales_diff_pct:.2f}%')

with mx_order:
    curr_order = data.loc[data['order_year'] == CURR_YEAR, 'order_id'].values[0]
    prev_order = data.loc[data['order_year'] == PREV_YEAR, 'order_id'].values[0]
    order_diff_pct = 100 * (curr_order - prev_order) / prev_order

    st.metric(label="Number of Order",
              value=curr_order,
              delta=f'{order_diff_pct:.2f}%')

with mx_customer:
    curr_customer = data.loc[data['order_year'] == CURR_YEAR, 'customer_id'].values[0]
    prev_customer = data.loc[data['order_year'] == PREV_YEAR, 'customer_id'].values[0]
    customer_diff_pct = 100 * (curr_customer - prev_customer) / prev_customer

    st.metric(label="Number of Customer",
              value=curr_customer,
              delta=f'{customer_diff_pct:.2f}%')

with mx_gpm:
    curr_gpm = data.loc[data['order_year'] == CURR_YEAR, 'gpm'].values[0]
    prev_gpm = data.loc[data['order_year'] == PREV_YEAR, 'gpm'].values[0]
    gpm_diff_pct = 100 * (curr_gpm - prev_gpm) / prev_gpm

    st.metric(label="Gross Profit Margin",
              value=f'{curr_gpm:.2f}%',
              delta=f'{gpm_diff_pct:.2f}%')

with st.sidebar:
    st.title("Select Argument")
    freq_select = st.selectbox("Time Unit", ['Harian', 'Bulanan'])
    agg_select = st.selectbox("Aggregate", ['Jumlah', 'Rata-Rata'])

time_unit = {
    'Harian': 'yearmonthdate',
    'Bulanan': 'yearmonth'
}

agg_opt = {
    'Jumlah': 'sum',
    'Rata-Rata': 'mean'
}

st.header("Sales Trend")
sales_line = alt.Chart(df[df['order_year'] == CURR_YEAR]).mark_line().encode(
    alt.X('order_date', title='Order Date', timeUnit=time_unit[freq_select]),
    alt.Y('sales', title='Revenue', aggregate=agg_opt[agg_select])
)

st.altair_chart(sales_line, use_container_width=True)

st.header("Bar Graph")
sales_bar = alt.Chart(df[df['order_year'] == CURR_YEAR]).mark_bar().encode(
    alt.X('order_date', title='Order Date', timeUnit=time_unit[freq_select]),
    alt.Y('sales', title='Revenue', aggregate=agg_opt[agg_select])
)

st.altair_chart(sales_bar, use_container_width=True)

# st.dataframe(df)
# st.dataframe(data, use_container_width=True)
