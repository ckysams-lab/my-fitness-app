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
    st.page_link("pages/03_equipment.py", label="器材管理", icon="🏸")

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

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_all = conn.read(spreadsheet= "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing", ttl="0s")
    
    # 1. 抓取前三欄並重新命名
    df_rank = df_all.iloc[:, :3].copy()
    df_rank.columns = ['排名', '姓名', '積分']
    
    # 2. 核心修正：轉換為數字，處理掉無效值，然後轉為整數
    df_rank['積分'] = pd.to_numeric(df_rank['積分'], errors='coerce').fillna(0)
    df_rank['積分'] = df_rank['積分'].astype(int)  # <-- 這行會強制去掉小數點
    
    # 3. 排序並取前 8 名
    df_rank = df_rank.sort_values(by="積分", ascending=False).head(8).reset_index(drop=True)
    
    # 4. 加入獎牌圖示
    def add_medal(i):
        if i == 0: return "🥇 1"
        if i == 1: return "🥈 2"
        if i == 2: return "🥉 3"
        return str(i+1)
    df_rank['顯示排名'] = [add_medal(i) for i in range(len(df_rank))]
    
    # 5. 顯示表格
    col_t, col_n = st.columns([1.5, 1])
    with col_t:
        # 選擇要顯示的欄位
        display_df = df_rank[['顯示排名', '姓名', '積分']].rename(columns={'顯示排名': '排名'})
        st.table(display_df.set_index('排名'))
    with col_n:
        st.info("💡 排名根據最新校內賽及公開賽積分自動更新。")
        st.success("🔥 努力訓練，進入前八強！")

except Exception as e:
    st.warning("⚠️ 排名榜數據暫時無法載入，請確認 Google Sheets 格式。")

st.divider()

# --- 第三部分：快速入口卡片 ---
st.header("📌 快速功能導覽")
c1, c2 = st.columns(2)
c1.info("👉 請點選左側選單進入 **[📊 體適能評測]**")
c2.warning("👉 老師請點選左側 **[🔐 老師管理後台]**")





















































