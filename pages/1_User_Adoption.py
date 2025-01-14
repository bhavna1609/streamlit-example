import streamlit as st
import time
import datetime
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import sum, col
import altair as alt
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(layout="wide")

# Get current session
session = get_active_session()

# prepare dataset
def get_data(date_from):
    # Load CO2 emissions data
    snow_users = session.table("SNOWFLAKE.ACCOUNT_USAGE.USERS").filter(col('CREATED_ON') >= date_from)
    snow_login_history = session.table("SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY").filter(col('EVENT_TIMESTAMP') >= date_from)
    return snow_users.to_pandas(), snow_login_history.to_pandas()


# date selector function
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
    
df_users, df_login_history = get_data(date_from)


st.title("User Adoption")
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
#st.subheader('Active Users')
# Perform query.
#df = conn.query('SELECT  NAME as ACTIVE_USERS FROM SNOWFLAKE.ACCOUNT_USAGE.USERS WHERE deleted_on is null ;', ttl=600)
#st.bar_chart(df)

df = df_login_history.groupby(["FIRST_AUTHENTICATION_FACTOR","EVENT_TIMESTAMP"],as_index=False).agg(
    {"USER_NAME": pd.Series.nunique})

st.text("")
st.text("")
st.subheader('User Login Method')
st.bar_chart(
    df,
    x='EVENT_TIMESTAMP',
    y='USER_NAME',
    color='FIRST_AUTHENTICATION_FACTOR'
)
st.text("")
st.text("")
st.subheader('User Statistics')
df_users
st.bar_chart(
    df_users,
    x='CREATED_ON',
    y='LOGIN_NAME',
    color='LOGIN_NAME'
)
