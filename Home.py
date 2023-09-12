import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import session
from snowflake.snowpark.functions import sum, col

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Monitoring Dashboard! 👋")

st.sidebar.success("Select a page above.")

#session = st.experimental_connection('snowpark').session

#df = conn.query('SELECT ROUND(SUM(CREDITS_USED),2) AS YTD_COMPUTE_CREDITS FROM SNOWFLAKE.ORGANIZATION_USAGE.WAREHOUSE_METERING_HISTORY;', ttl=600)
#compute_credit = pd.to_numeric(df)
#st.metric(label="Compute Credits", value=compute_credit)
# create three columns
kpi1, kpi2, kpi3 = st.columns(3)

# fill in those three columns with respective metrics or KPIs
kpi1.metric(
    label="Compute_Credits",
    value="4.25"
)

kpi2.metric(
    label="Accounts",
    value="1"
)

kpi3.metric(
    label="Warehouses",
    value="1"
)
conn = st.experimental_connection('snowpark')
df = conn.query('SELECT  ACCOUNT_NAME FROM ST_DEMO.SCH_ST_DEMO.ACCOUNT_INFO_TABLE ;', ttl=600)
option = st.selectbox('Select Account Name for which you want to input the budget',df)

#st.write('You selected:', option)

session = st.experimental_connection('snowpark').session
df = session.table('ACCOUNT_INFO_TABLE').filter(col('ACCOUNT_Name').isin(option))



st.text("")

#st.dataframe(df)
with st.form("data_editor_form"):
    st.caption("Edit the budget for selected account")
    edited = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    try:
        #Note the quote_identifiers argument for case insensitivity
        session.write_pandas(edited, "ACCOUNT_INFO_TABLE",overwrite=True, quote_identifiers=False)
        st.toast("Budget updated successfully")
        time.sleep(5)
    except:
        st.warning("Error updating table")
    #display success message for 5 seconds and update the table to reflect what is in Snowflake
    st.experimental_rerun()
