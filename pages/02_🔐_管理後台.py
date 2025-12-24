import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="管理後台", layout="wide")

st.title("🔐 老師管理後台")

sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

tab1, tab2 = st.tabs(["📊 數據總覽", "⚙️ 系統設定"])

with tab1:
    st.subheader("學生評測數據紀錄")
    try:
        df = conn.read(spreadsheet=sheet_url, worksheet="data", ttl="0s")
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="下載完整數據 CSV",
            data=csv,
            file_name="fitness_data.csv",
            mime="text/csv",
        )
    except:
        st.info("暫時未有數據紀錄。")

with tab2:
    st.subheader("權限管理")
    st.write("此處僅供體育組老師使用。")
