import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import os

# --- 1. 核心配置 (必須是第一行，唔准加任何隱藏 Sidebar 嘅 CSS) ---
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# --- 2. 定義首頁功能 (確保數據顯示唔會被過濾) ---
def show_home():
    st.title("🌟 正覺體育人：資訊與動態")
    st.markdown("---")

    # 設定 Google Sheet 連結
    sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # --- 📢 消息公告 ---
        st.header("📢 體育組最新動態")
        df_news = conn.read(spreadsheet=sheet_url, worksheet="news", ttl="0s")
        if not df_news.empty:
            st.dataframe(df_news, hide_index=True, use_container_width=True)
        else:
            st.write("目前無最新消息。")

        st.divider()

        # --- 🏆 核心：壁球排名榜 (暴力顯示版) ---
        st.header("🏆 壁球隊排名榜")
        try:
            # 直接讀取名為 'ranking' 的 Worksheet
            df_rank = conn.read(spreadsheet=sheet_url, worksheet="ranking", ttl="0s")
            if not df_rank.empty:
                # 唔做篩選住，直接 table 出嚟，確保你見到數據先
                st.table(df_rank)
            else:
                st.info("Google Sheets 內 'ranking' 分頁目前係空的。")
        except Exception as e:
            st.error(f"❌ 排名榜讀取失敗！請檢查 Sheets 入面分頁名係咪叫 'ranking'。錯誤：{e}")

        st.divider()

        # --- 🎬 影片區 ---
        st.header("🎬 精彩瞬間")
        cv1, cv2 = st.columns(2)
        with cv1: st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
        with cv2: st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    except Exception as e:
        st.error(f"⚠️ 系統連線發生問題：{e}")

# --- 3. 導航系統 (對準你最後改好嗰四個檔名) ---
# 唔再用 try-except 包住，直接寫出嚟，邊一頁檔案唔見咗 Streamlit 會自己報錯，方便我哋 Debug
pg = st.navigation([
    st.Page(show_home, title="首頁", icon="🏠"),
    st.Page("pages/fitness_test.py", title="體適能評測", icon="📊"),
    st.Page("pages/stars.py", title="體育之星", icon="⭐"),
    st.Page("pages/admin.py", title="管理後台", icon="🔐"),
    st.Page("pages/equipment.py", title="器材管理", icon="🏸")
])

pg.run()











