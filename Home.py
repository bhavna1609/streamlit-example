import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Monitoring Dashboard! 👋")

st.sidebar.success("Select a page above.")

session = st.experimental_connection('snowpark').session

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

#Budget input
#session = get_active_session()
df=session.table('ST_DEMO.SCH_ST_DEMO.ACCOUNT_INFO_TABLE')

with st.form("Budget_input_form"):
    st.caption("edit the Budget")
    edited = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    submit_button = st.form_submit_button("Submit")
if submit_button:
    try:
        #Note the quote_identifiers argument for case insensitivity
        session.write_pandas(edited, "ST_DEMO.SCH_ST_DEMO.ACCOUNT_INFO_TABLE", overwrite=True, quote_identifiers=False)
        st.toast("Table updated")
        time.sleep(5)
    except:
        st.warning("Error updating table")
    #display success message for 5 seconds and update the table to reflect what is in Snowflake
    st.experimental_rerun()


