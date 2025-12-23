import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. 頁面設定
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# 2. 側邊欄與樣式
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] a { font-size: 20px !important; }
        .sidebar-title { font-size: 24px !important; font-weight: bold; color: #FFD700; text-align: center; }
        .stTable { font-size: 18px !important; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<p class="sidebar-title">正覺蓮社學校<br>體育組</p>', unsafe_allow_html=True)
    st.divider()
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    st.page_link("pages/1_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_admin.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_equipment.py", label="器材管理", icon="🏸")

# 3. 主標題
st.title("🌟 正覺體育人：資訊與動態")
st.divider()

# --- 第一部分：最新動態 ---
st.header("📢 體育組最新動態")
sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_news = conn.read(spreadsheet=sheet_url, worksheet="news", ttl="0s")
    
    if not df_news.empty:
        c1, c2 = st.columns([1, 1.5])
        with c1:
            st.subheader("⏳ 賽事倒數")
            events = df_news[df_news['類型'] == '賽事']
            for _, row in events.iterrows():
                target = pd.to_datetime(row['日期']).date()
                days = (target - datetime.now().date()).days
                if days >= 0: st.metric(row['標題'], f"{days} 天")
        with c2:
            st.subheader("🗞️ 消息公告")
            notices = df_news[df_news['類型'] == '消息']
            for _, row in notices.head(3).iterrows():
                with st.expander(f"📌 {row['標題']} ({row['日期']})"):
                    st.write(row['內容'])
    else:
        st.info("💡 最新賽事倒數與公告整理中...")
except:
    st.info("💡 歡迎關注！最新賽事與消息公告將在此同步更新。")

st.divider()

# --- 第二部分：影片區 ---
st.header("🎬 精彩瞬間")
v1, v2 = st.columns(2)
with v1:
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    st.caption("🏃‍♂️ 體適能測試精選")
with v2:
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    st.caption("⚽ 校隊訓練花絮")

st.divider()

# --- 第三部分：排行榜 ---
st.header("🏆 壁球隊排名榜 (Top 8)")
try:
    # 讀取預設的第一個分頁
    df_rank_raw = conn.read(spreadsheet=sheet_url, ttl="0s")
    
    if not df_rank_raw.empty:
        # 清理數據
        df_rank = df_rank_raw.iloc[:, :3].copy()
        df_rank.columns = ['排名', '姓名', '積分']
        df_rank['積分'] = pd.to_numeric(df_rank['積分'], errors='coerce').fillna(0).astype(int)
        df_rank = df_rank.sort_values(by="積分", ascending=False).head(8).reset_index(drop=True)
        
        # 增加獎牌
        df_rank['排名'] = [f"🥇 1" if i==0 else f"🥈 2" if i==1 else f"🥉 3" if i==2 else str(i+1) for i in range(len(df_rank))]
        
        rt, rn = st.columns([1.5, 1])
        with rt:
            st.table(df_rank.set_index('排名'))
        with rn:
            st.info("💡 排名根據最新校內賽積分自動更新。")
            st.success("🔥 努力訓練，進入前八強！")
    else:
        st.warning("排名榜數據更新中...")
except:
    st.warning("⚠️ 數據載入失敗，請確認試算表內容。")

st.divider()

# --- 第四部分：導覽 ---
st.header("📌 快速功能導覽")
f1, f2 = st.columns(2)
f1.info("👉 學生：進入 **[📊 體適能評測]**")
f2.warning("👉 老師：進入 **[🔐 老師管理後台]**")

























































