import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🏸 器材管理系統")

sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df_equip = conn.read(spreadsheet=sheet_url, worksheet="equipment")
    st.dataframe(df_equip, use_container_width=True)
except:
    st.info("器材清單讀取中...")

st.button("📦 登記借用")
