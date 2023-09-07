import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Monitoring Dashboard! 👋")

st.sidebar.success("Select a page above.")

conn = st.experimental_connection('snowpark')
df = conn.query('SELECT ROUND(SUM(CREDITS_USED),2) AS YTD_COMPUTE_CREDITS FROM SNOWFLAKE.ORGANIZATION_USAGE.WAREHOUSE_METERING_HISTORY;', ttl=600)
compute_credit = to_numeric(df)
st.metric(label="Compute Credits", value=compute_credit)
