import streamlit as st
import matplotlib.pyplot as plt
import time
import datetime
import plotly.express as px
import pandas as pd
import numpy as np
import altair as alt




st.set_page_config(
    page_title="Monitoring Dashboard", page_icon="🔹", layout="centered"
)

def date_selector() -> tuple[datetime.date, datetime.date]:
    """Adds a date selector with a few different options."""

    DATE_RANGE_OPTIONS = [
        "Last 7 days",
        "Last 28 days",
        "Last 3 months",
        "Last 6 months",
        "Last 12 months",
        "All time",
        "Custom",
    ]

    if "date_range" in st.session_state:
        index = DATE_RANGE_OPTIONS.index(st.session_state.date_range)
    else:
        index = 0

    date_range = st.selectbox(
        "Date range",
        options=[
            "Last 7 days",
            "Last 28 days",
            "Last 3 months",
            "Last 6 months",
            "Last 12 months",
            "All time",
            "Custom",
        ],
        index=index,
        key="date_range",
    )

    if date_range != "Custom":
        date_to = datetime.date.today()
        if date_range == "Last 7 days":
            date_from = date_to - datetime.timedelta(days=7)
        elif date_range == "Last 28 days":
            date_from = date_to - datetime.timedelta(days=28)
        elif date_range == "Last 3 months":
            date_from = date_to - datetime.timedelta(weeks=12)
        elif date_range == "Last 6 months":
            date_from = date_to - datetime.timedelta(weeks=24)
        elif date_range == "Last 12 months":
            date_from = date_to - datetime.timedelta(days=365)
        else:
            date_from = datetime.date(year=2016, month=1, day=1)

    if "custom" in st.session_state:
        value = st.session_state.custom
    else:
        value = (
            date_to - datetime.timedelta(days=7),
            date_to,
        )

    if date_range == "Custom":
        date_from, date_to = st.date_input(
            "Choose start and end date",
            value=value,
            key="custom",
        )

    st.caption(f"Your selection is from **{date_from}** to **{date_to}**")

    return date_from, date_to
# Date selector widget
with st.sidebar:
    date_from, date_to = date_selector()

    # Header
#st.title("Welcome to the Monitoring Dashboard app!")
#st.title(':blue[Monitoring Dashboard] :sunglasses:')
#st.text("")
#st.text("")
st.title("Performance Monitoring Dashboard")
# Initialize connection.
conn = st.experimental_connection('snowpark')
#status elements
#st.snow()
#st.balloons()
#Title


#st.sidebar.success('Welcome to Home Page :tada:')
#Code block
  #code = '''st.title('First :blue[Streamlit] web app :sunglasses:')'''
  #st.code(code, language='python')
#with st.chat_message("user"):
    #st.write("Hello 👋")
st.subheader('Top 10 Slow Running Queries')
# Perform query.
df = conn.query('select to_number((execution_time / 1000)) as exec_time_in_seconds,query_text from SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY where  execution_status = \'SUCCESS\' order by     execution_time desc limit     10;;', ttl=600)
#df


#df=px.data.tips()
fig=px.bar(df,y='EXEC_TIME_IN_SECONDS', orientation='h')
st.write(fig)

#st.pyplot(df.plot.barh(stacked=True).figure)
st.text("")
st.text("")
st.subheader('Warehouse Usage over time')
df = conn.query('SELECT SUM(CREDITS_USED) CREDITS_USED,TO_DATE(START_TIME) START_DATE,WAREHOUSE_NAME FROM  SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY  GROUP BY  START_DATE,WAREHOUSE_NAME;', ttl=600)
df

st.line_chart(
    df,
    x = 'START_DATE',
    y = 'CREDITS_USED',
    color = 'WAREHOUSE_NAME',
    use_container_width=True
)
