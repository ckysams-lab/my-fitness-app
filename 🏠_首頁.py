import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. 頁面設定 (必須是第一個 Streamlit 指令)
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# 2. 側邊欄與表格樣式 (還原你最滿意的 CSS)
st.markdown("""
    <style>
        /* [data-testid="stSidebarNav"] {display: none;} */
        [data-testid="stSidebar"] a { font-size: 20px !important; margin-bottom: 8px; }
        [data-testid="stSidebar"] h3 { font-size: 26px !important; font-weight: bold; color: #FFD700; text-align: center; }
        .stTable { font-size: 18px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. 側邊欄導航 (請確保 pages/ 內的檔名與下面路徑完全一致)
with st.sidebar:
    st.markdown("### 正覺蓮社學校\n### 體育組")
    st.divider()
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    
    # 這裡的 pages/ 檔名是根據你之前的截圖設定的，如有手動改名請微調
    try:
        st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
        st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
        st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")
        st.page_link("pages/04_⭐_體育之星.py", label="體育之星", icon="⭐")
    except Exception as e:
        st.error("側邊欄部分連結失效，請檢查 pages 資料夾內的檔名。")

# 4. 主頁標題
st.title("🌟 正覺體育人：資訊與動態")
st.markdown("---")

# 設定 Google Sheets 連線
sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 第一部分：最新動態 (news 分頁) ---
st.header("📢 體育組最新動態")
try:
    df_news = conn.read(spreadsheet=sheet_url, worksheet="news", ttl="0s")
    if not df_news.dropna(how='all').empty:
        c1, c2 = st.columns([1, 1.5])
        with c1:
            st.subheader("⏳ 賽事倒數")
            # 確保日期格式正確
            df_news['日期'] = pd.to_datetime(df_news['日期'])
            events = df_news[df_news['類型'] == '賽事']
            for _, row in events.iterrows():
                diff = (row['日期'].date() - datetime.now().date()).days
                if diff >= 0: st.metric(row['標題'], f"{diff} 天")
        with c2:
            st.subheader("🗞️ 消息公告")
            notices = df_news[df_news['類型'] == '消息'].sort_index(ascending=False)
            for _, row in notices.head(3).iterrows():
                with st.expander(f"📌 {row['標題']} ({row['日期'].strftime('%Y-%m-%d')})"):
                    st.write(row['內容'])
except Exception as e:
    st.info("💡 歡迎關注！最新消息更新中...")

st.divider()

# --- 第二部分：影片區 ---
st.header("🎬 精彩瞬間")
cv1, cv2 = st.columns(2)
with cv1:
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    st.caption("🏃‍♂️ 體適能測試精選")
with cv2:
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    st.caption("⚽ 校隊訓練花絮")

st.divider()

# --- 第三部分：壁球排名榜 (還原🥇🥈🥉邏輯) ---
st.header("🏆 壁球隊排名榜 (Top 8)")
try:
    df_all = conn.read(spreadsheet=sheet_url, worksheet="ranking", ttl="0s")
    
    # 自動尋找包含「排名」、「姓名」、「積分」字眼的欄位
    col_rank = [c for c in df_all.columns if '排名' in c][0]
    col_name = [c for c in df_all.columns if '姓名' in c][0]
    col_score = [c for c in df_all.columns if '積分' in c][0]
    
    df_rank = df_all[[col_rank, col_name, col_score]].copy()
    df_rank.columns = ['排名', '姓名', '積分']
    
    # 轉換積分為數字並排序
    df_rank['積分'] = pd.to_numeric(df_rank['積分'], errors='coerce').fillna(0).astype(int)
    df_rank = df_rank.sort_values(by="積分", ascending=False).head(8).reset_index(drop=True)
    
    def add_medal(i):
        if i == 0: return "🥇 1"
        if i == 1: return "🥈 2"
        if i == 2: return "🥉 3"
        return str(i+1)
    
    df_rank['排名'] = [add_medal(i) for i in range(len(df_rank))]
    
    ct, cn = st.columns([1.5, 1])
    with ct:
        st.table(df_rank.set_index('排名'))
    with cn:
        st.info("💡 排名根據最新校內賽積分自動更新。")
        st.success("🔥 努力訓練，進入前八強！")
except Exception as e:
    st.warning("⚠️ 排名榜數據更新中...")

st.divider()

# --- 第四部分：導覽按鈕 ---
st.header("📌 快速功能導覽")
f1, f2 = st.columns(2)
f1.info("👉 學生：進入 [📊 體適能評測]")
f2.warning("👉 老師：進入 [🔐 老師管理後台]")
