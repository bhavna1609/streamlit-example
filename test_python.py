import streamlit as st
import time



st.set_page_config(page_title='User', page_icon=':wave:')
# Initialize connection.
conn = st.experimental_connection('snowpark')
#status elements
#st.snow()
#st.balloons()
#Title
st.title('First :blue[Streamlit] web app :sunglasses:')
st.text("")
st.text("")

st.sidebar.success('Welcome to Home Page :tada:')
#Code block
  #code = '''st.title('First :blue[Streamlit] web app :sunglasses:')'''
  #st.code(code, language='python')

with st.chat_message("user"):
    st.write("Hello 👋")
# Perform query.
df = conn.query('SELECT top 10 * from SNOWFLAKE.ACCOUNT_USAGE.USERS;', ttl=600)
st.map(df)

