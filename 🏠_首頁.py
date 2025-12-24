import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. 核心配置 (第一行，絕不隱藏 Sidebar)
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# 2. 定義首頁內容 (還原公告、倒數、影片、排名榜)
def show_home():
    st.title("🌟 正覺體育人：資訊與動態")
    st.markdown("---")
    
    sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # --- 🏆 核心：壁球隊排名榜 ---
        st.header("🏆 壁球隊排名榜")
        df_rank = conn.read(spreadsheet=sheet_url, worksheet="ranking", ttl="0s")
        if not df_rank.empty:
            # 顯示頭 8 名
            st.table(df_rank.iloc[:, :3].head(8))
        else:
            st.info("數據載入中...")

        st.divider()

        # --- 📢 最新公告與倒數 ---
        st.header("📢 體育組最新動態")
        df_news = conn.read(spreadsheet=sheet_url, worksheet="news", ttl="0s")
        if not df_news.empty:
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

        st.divider()

        # --- 🎬 影片區 ---
        st.header("🎬 精彩瞬間")
        cv1, cv2 = st.columns(2)
        with cv1: st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
        with cv2: st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    except Exception as e:
        st.error(f"數據讀取失敗：{e}")

# 3. 導航系統 (必須精準對應 pages/ 入面的新檔名)
pg = st.navigation([
    st.Page(show_home, title="首頁", icon="🏠"),
    st.Page("pages/1_📊_體適能評測.py", title="體適能評測", icon="📊"),
    st.Page("pages/02_🔐_管理後台.py", title="管理後台", icon="🔐"),
    st.Page("pages/03_🏸_器材管理.py", title="器材管理", icon="🏸"),
    st.Page("pages/04_⭐_體育之星.py", title="體育之星", icon="⭐")
])

pg.run()



