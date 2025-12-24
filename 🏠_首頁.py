import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import os

# --- 1. 核心配置 (務必第一行) ---
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# --- 2. 定義完整的首頁內容 (絕無簡化) ---
def show_home():
    st.title("🌟 正覺體育人：資訊與動態")
    st.markdown("---")

    # 設定 Google Sheet 連接
    sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # --- 第一部分：最新動態 ---
        st.header("📢 體育組最新動態")
        df_news = conn.read(spreadsheet=sheet_url, worksheet="news", ttl="0s")
        
        if not df_news.dropna(how='all').empty:
            c1, c2 = st.columns([1, 1.5])
            with c1:
                st.subheader("⏳ 賽事倒數")
                df_news['日期'] = pd.to_datetime(df_news['日期'])
                events = df_news[df_news['類型'] == '賽事']
                for _, row in events.iterrows():
                    target = row['日期'].date()
                    diff = (target - datetime.now().date()).days
                    if diff >= 0:
                        st.metric(row['標題'], f"{diff} 天")
            
            with c2:
                st.subheader("🗞️ 消息公告")
                notices = df_news[df_news['類型'] == '消息'].sort_index(ascending=False)
                for _, row in notices.head(3).iterrows():
                    with st.expander(f"📌 {row['標題']} ({row['日期'].strftime('%Y-%m-%d')})"):
                        st.write(row['內容'])
    except Exception as e:
        st.info("💡 公告系統同步中，請稍候...")

    st.divider()

    # --- 第二部分：影片區 ---
    st.header("🎬 精彩瞬間")
    cv1, cv2 = st.columns(2)
    with cv1:
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    with cv2:
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    st.divider()

    # --- 第三部分：壁球排名榜 ---
    st.header("🏆 壁球隊排名榜 (Top 8)")
    try:
        df_all = conn.read(spreadsheet=sheet_url, worksheet="ranking", ttl="0s")
        col_rank = [c for c in df_all.columns if '排名' in c][0]
        col_name = [c for c in df_all.columns if '姓名' in c][0]
        col_score = [c for c in df_all.columns if '積分' in c][0]
        
        df_rank = df_all[[col_rank, col_name, col_score]].copy()
        df_rank.columns = ['排名', '姓名', '積分']
        df_rank['積分'] = pd.to_numeric(df_rank['積分'], errors='coerce').fillna(0).astype(int)
        df_rank = df_rank.sort_values(by="積分", ascending=False).head(8).reset_index(drop=True)
        
        def add_medal(i):
            if i == 0: return "🥇 1"
            if i == 1: return "🥈 2"
            if i == 2: return "🥉 3"
            return str(i+1)
        df_rank['顯示排名'] = [add_medal(i) for i in range(len(df_rank))]
        
        st.table(df_rank[['顯示排名', '姓名', '積分']].rename(columns={'顯示排名':'排名'}).set_index('排名'))
    except:
        st.warning("⚠️ 排名榜數據讀取中...")

# --- 3. 導覽結構 (使用穩定路徑，自定義顯示標題) ---
# 只有當檔案存在時才顯示分頁，防止報錯
pages_to_show = [st.Page(show_home, title="首頁", icon="🏠")]

if os.path.exists("pages/fitness_test.py"):
    pages_to_show.append(st.Page("pages/fitness_test.py", title="體適能評測", icon="📊"))
if os.path.exists("pages/stars.py"):
    pages_to_show.append(st.Page("pages/stars.py", title="體育之星", icon="⭐"))
if os.path.exists("pages/admin.py"):
    pages_to_show.append(st.Page("pages/admin.py", title="老師管理後台", icon="🔐"))
if os.path.exists("pages/equipment.py"):
    pages_to_show.append(st.Page("pages/equipment.py", title="器材管理", icon="🏸"))

pg = st.navigation(pages_to_show)
pg.run()










