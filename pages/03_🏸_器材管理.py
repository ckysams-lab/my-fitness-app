import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="器材管理", layout="wide")

st.title("🏸 體育器材管理系統")

sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

with st.expander("➕ 新增借用紀錄"):
    with st.form("borrow_form"):
        item = st.selectbox("器材名稱", ["羽毛球拍", "乒乓球拍", "足球", "籃球", "跳繩"])
        qty = st.number_input("數量", 1, 10, 1)
        borrower = st.text_input("借用人班級姓名")
        submit = st.form_submit_button("確認提交")
        if submit:
            st.success(f"已紀錄：{borrower} 借用 {qty} 件 {item}")

st.subheader("📦 現時器材庫存")
try:
    df_inv = conn.read(spreadsheet=sheet_url, worksheet="inventory", ttl="0s")
    st.table(df_inv)
except:
    st.write("庫存清單同步中...")
