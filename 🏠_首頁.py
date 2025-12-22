import streamlit as st
import pandas as pd
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
        /* 讓表格字體大一點 */
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

# 4. 主頁面內容
st.title("🌟 正覺體育人：精彩瞬間")
st.markdown("---")

# --- 第一部分：影片區 ---
st.header("🎬 學生運動亮點")
col_v1, col_v2 = st.columns(2)
with col_v1:
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    st.subheader("🏃‍♂️ 9分鐘耐力跑精選")
with col_v2:
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    st.subheader("⚽ 校隊訓練花絮")

st.divider()

# --- 讀取 Google Sheets 數據 ---
# 請將下方的網址替換成您 Google Sheets 的「共用網址」
sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # 讀取數據並只取前 8 名，按積分從高到低排序
    df_all = conn.read(spreadsheet=sheet_url)
    df_squash = df_all.sort_values(by="積分", ascending=False).head(8)
    
    # 重新整理排名顯示（加入獎牌）
    def add_medal(i):
        if i == 0: return "🥇 1"
        if i == 1: return "🥈 2"
        if i == 2: return "🥉 3"
        return str(i+1)
    
    df_squash['排名'] = [add_medal(i) for i in range(len(df_squash))]
except:
    st.error("暫時無法讀取排名榜數據")
    df_squash = pd.DataFrame() # 防止報錯

# --- 顯示排名榜 ---
st.header("🏆 壁球隊成員排名榜 (Top 8)")

if not df_squash.empty:
    col_table, col_note = st.columns([1.5, 1])
    with col_table:
        # 只顯示這三列，並隱藏索引
        st.table(df_squash[['排名', '隊員姓名', '積分']].set_index('排名'))
    with col_note:
        st.success("🔥 數據已實時更新！爭取進入前八強。")

st.divider()

# --- 第三部分：快速入口卡片 ---
st.header("📌 快速功能導覽")
c1, c2 = st.columns(2)
c1.info("👉 請點選左側選單進入 **[📊 體適能評測]**")
c2.warning("👉 老師請點選左側 **[🔐 老師管理後台]**")














































