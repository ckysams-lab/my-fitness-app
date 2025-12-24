import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import os

# 1. 核心配置 (必須喺第一行，絕對唔准加 display:none)
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# 強制顯示 Sidebar 的 CSS (以防萬一)
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            visibility: visible !important;
            width: 250px !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. 定義首頁內容 (還原公告、影片同排名榜)
def show_home():
    st.title("🌟 正覺體育人：資訊與動態")
    sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # --- 🏆 核心：壁球排名榜 ---
        st.header("🏆 壁球隊排名榜")
        df_rank = conn.read(spreadsheet=sheet_url, worksheet="ranking", ttl="0s")
        if not df_rank.empty:
            st.table(df_rank.head(8))
        else:
            st.info("排名數據載入中...")

        st.divider()

        # --- 📢 最新公告 ---
        st.header("📢 體育組最新動態")
        df_news = conn.read(spreadsheet=sheet_url, worksheet="news", ttl="0s")
        if not df_news.empty:
            st.dataframe(df_news, use_container_width=True, hide_index=True)

        st.divider()
        st.header("🎬 精彩瞬間")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 

    except Exception as e:
        st.error(f"連線失敗：{e}")

# 3. 重新建立導航 (對準你最後改好嗰四個檔名)
# 只要執行 pg.run()，Sidebar 就一定會出嚟
try:
    pg = st.navigation([
        st.Page(show_home, title="首頁", icon="🏠"),
        st.Page("pages/fitness_test.py", title="體適能評測", icon="📊"),
        st.Page("pages/stars.py", title="體育之星", icon="⭐"),
        st.Page("pages/admin.py", title="管理後台", icon="🔐"),
        st.Page("pages/equipment.py", title="器材管理", icon="🏸")
    ])
    pg.run()
except Exception as e:
    st.error(f"導航出錯，請檢查檔案：{e}")










