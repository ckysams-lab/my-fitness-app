import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. 頁面設定
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# 2. 側邊欄樣式與功能控制 (CSS)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] a { font-size: 22px !important; margin-bottom: 10px; }
        [data-testid="stSidebar"] h3 { font-size: 28px !important; font-weight: bold; color: #FFD700; text-align: center; }
        hr { margin-top: 1rem; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.2); }
        .stTable { font-size: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. 側邊欄內容
with st.sidebar:
    st.markdown("### 正覺蓮社學校\n### 體育組")
    st.divider()
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    st.page_link("pages/1_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_admin.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_equipment.py", label="器材管理", icon="🏸")

# 4. 主頁面標題
st.title("🌟 正覺體育人：資訊與動態")
st.markdown("---")

# --- 第一部分：最新公告與賽事倒數 (新整合) ---
st.header("📢 體育組最新動態")

# 共用同一個 GSheets Connection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # 讀取 news 工作表 (請確保試算表中有一個分頁叫 news)
    # 若暫時沒有 news 分頁，此部分會跳到 except 顯示「整理中」
    news_url = "https://docs.google.com/spreadsheets/d/1AcO-acwC1Or1p_tKsy_JWx1furOaugpSoVkV15OZDcE/edit?usp=sharing"
    df_news = conn.read(spreadsheet=news_url, worksheet="news", ttl="0s")
    
    col_news1, col_news2 = st.columns([1, 1.5])
    
    with col_news1:
        st.subheader("⏳ 賽事倒數")
        events = df_news[df_news['類型'] == '賽事']
        for _, row in events.iterrows():
            target_date = pd.to_datetime(row['日期']).date()
            days_diff = (target_date - datetime.now().date()).days
            if days_diff > 0:
                st.metric(label=row['標題'], value=f"{days_diff} 天")
            elif days_diff == 0:
                st.success(f"🎉 {row['標題']} 就在今天！")

    with col_news2:
        st.subheader("🗞️ 消息公告")
        notices = df_news[df_news['類型'] == '消息'].sort_index(ascending=False)
        for _, row in notices.head(3).iterrows():
            with st.expander(f"📌 {row['標題']} ({row['日期']})"):
                st.write(row['內容'])
except:
    st.info("💡





















































