import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import os

# --- 1. 核心配置 ---
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# --- A. 首頁內容函式 ---
def show_home():
    st.title("🌟 正覺體育人：資訊與動態")
    st.markdown("---")
    
    sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # 消息公告
        st.header("📢 體育組最新動態")
        df_news = conn.read(spreadsheet=sheet_url, worksheet="news", ttl="0s")
        if not df_news.dropna(how='all').empty:
            st.success("最新消息已加載")
    except:
        st.info("💡 消息整理中...")

    st.divider()
    st.header("🎬 精彩瞬間")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# --- B. 動態導覽 (關鍵修復邏輯) ---
# 先放一定會有的首頁
pages = [st.Page(show_home, title="首頁", icon="🏠")]

# 檢查檔案是否存在，存在才加進去，避免 StreamlitAPIException
if os.path.exists("pages/fitness_test.py"):
    pages.append(st.Page("pages/fitness_test.py", title="體適能評測", icon="📊"))

if os.path.exists("pages/stars.py"):
    pages.append(st.Page("pages/stars.py", title="體育之星", icon="⭐"))

if os.path.exists("pages/admin.py"):
    pages.append(st.Page("pages/admin.py", title="老師管理後台", icon="🔐"))

if os.path.exists("pages/equipment.py"):
    pages.append(st.Page("pages/equipment.py", title="器材管理", icon="🏸"))

# 啟動導覽
pg = st.navigation(pages)
pg.run()











