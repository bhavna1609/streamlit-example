import streamlit as st
import time
import datetime




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
st.title('blue[Monitoring Dashboard] web app :sunglasses:')
st.text("")
st.text("")
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

with st.chat_message("user"):
    st.write("Hello 👋")
# Perform query.
df = conn.query('SELECT   NAME as USERS ,EMAIL FROM SNOWFLAKE.ACCOUNT_USAGE.USERS WHERE deleted_on is null ;', ttl=600)
st.bar_chart(df)

