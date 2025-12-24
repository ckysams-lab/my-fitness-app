import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("🔐 體育組管理後台")

sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

st.header("📢 發佈新動態")
with st.form("news_form"):
    new_title = st.text_input("標題")
    new_type = st.selectbox("類型", ["消息", "賽事"])
    new_date = st.date_input("日期")
    new_content = st.text_area("內容")
    
    if st.form_submit_button("確認發佈"):
        st.success("公告已排程更新 (請手動更新 Google Sheets)")

st.divider()
st.header("📊 數據總覽")
df_news = conn.read(spreadsheet=sheet_url, worksheet="news")
st.dataframe(df_news)
