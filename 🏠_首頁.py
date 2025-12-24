import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] a { font-size: 22px !important; margin-bottom: 10px; }
        [data-testid="stSidebar"] h3 { font-size: 28px !important; font-weight: bold; color: #FFD700; text-align: center; }
        .stTable { font-size: 20px !important; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 正覺蓮社學校\n### 體育組")
    st.divider()
    st.page_link(".", label="首頁", icon="🏠")
    st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")

st.title("🌟 正覺體育人：資訊與動態")
st.markdown("---")

sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# 🏆 壁球排名榜
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
    
    ct, cn = st.columns([1.5, 1])
    with ct:
        display_df = df_rank[['顯示排名', '姓名', '積分']].rename(columns={'顯示排名':'排名'}).set_index('排名')
        st.table(display_df)
    with cn:
        st.info("💡 排名根據最新校內賽積分自動更新。")
except:
    st.warning("⚠️ 排名榜數據更新中...")

# 📢 最新動態
st.divider()
st.header("📢 體育組最新動態")
try:
    df_news = conn.read(spreadsheet=sheet_url, worksheet="news", ttl="0s")
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("⏳ 賽事倒數")
        events = df_news[df_news['類型'] == '賽事']
        for _, row in events.iterrows():
            target = pd.to_datetime(row['日期']).date()
            diff = (target - datetime.now().date()).days
            if diff >= 0: st.metric(row['標題'], f"{diff} 天")
    with c2:
        st.subheader("🗞️ 消息公告")
        notices = df_news[df_news['類型'] == '消息'].sort_index(ascending=False)
        for _, row in notices.head(3).iterrows():
            with st.expander(f"📌 {row['標題']}"):
                st.write(row['內容'])
except:
    pass
