import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import os

# 1. 核心配置 (一定要第一行)
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# 2. 定義首頁內容
def show_home():
    st.title("🌟 正覺體育人：資訊與動態")
    
    sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        st.header("📢 體育組最新動態")
        df_news = conn.read(spreadsheet=sheet_url, worksheet="news", ttl="0s")
        
        if not df_news.dropna(how='all').empty:
            c1, c2 = st.columns([1, 1.5])
            with c1:
                st.subheader("⏳ 賽事倒數")
                df_news['日期'] = pd.to_datetime(df_news['日期'])
                events = df_news[df_news['類型'] == '賽事']
                for _, row in events.iterrows():
                    diff = (row['日期'].date() - datetime.now().date()).days
                    if diff >= 0: st.metric(row['標題'], f"{diff} 天")
            with c2:
                st.subheader("🗞️ 消息公告")
                notices = df_news[df_news['類型'] == '消息'].sort_index(ascending=False)
                for _, row in notices.head(3).iterrows():
                    with st.expander(f"📌 {row['標題']} ({row['日期'].strftime('%m/%d')})"):
                        st.write(row['內容'])
    except:
        st.info("💡 公告系統連線中...")

    st.divider()
    st.header("🎬 精彩瞬間")
    cv1, cv2 = st.columns(2)
    with cv1: st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    with cv2: st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# 3. 導航系統 (只要無咗嗰段 display:none，呢度就會出返嚟)
pages = [
    st.Page(show_home, title="首頁", icon="🏠"),
    st.Page("pages/fitness_test.py", title="體適能評測", icon="📊"),
    st.Page("pages/stars.py", title="體育之星", icon="⭐"),
    st.Page("pages/admin.py", title="管理後台", icon="🔐"),
    st.Page("pages/equipment.py", title="器材管理", icon="🏸")
]

pg = st.navigation(pages)
pg.run()











