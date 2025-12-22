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
sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # 讀取整張表
    df_all = conn.read(spreadsheet=sheet_url)
    
    # 【核心修正】不靠欄位名稱，靠位置來抓前三欄
    # iloc[:, :3] 代表抓取所有行，以及第 0, 1, 2 欄
    df_rank = df_all.iloc[:, :3].copy()
    
    # 強制重新命名這三欄，確保後續代碼不會出錯
    df_rank.columns = ['排名', '姓名', '積分']
    
    # 確保積分是數字格式 (防止 Google Sheets 把它讀成文字)
    df_rank['積分'] = pd.to_numeric(df_rank['積分'], errors='coerce')
    
    # 排序並取前 8 名
    df_rank = df_rank.sort_values(by="積分", ascending=False).head(8).reset_index(drop=True)
    
    # 加入獎牌圖示
    def add_medal(i):
        if i == 0: return "🥇 1"
        if i == 1: return "🥈 2"
        if i == 2: return "🥉 3"
        return str(i+1)
    
    df_rank['顯示排名'] = [add_medal(i) for i in range(len(df_rank))]
    
    # 顯示表格
    col_table, col_note = st.columns([1.5, 1])
    with col_table:
        # 最終顯示：只取我們定義好的欄位
        display_df = df_rank[['顯示排名', '姓名', '積分']].rename(columns={'顯示排名': '排名'})
        st.table(display_df.set_index('排名'))
        
except Exception as e:
    st.error("⚠️ 無法載入排名數據，請檢查 Google Sheets 格式。")
    # st.write(f"除錯資訊: {e}") # 如果想看具體報錯可取消註解

st.divider()

# --- 第三部分：快速入口卡片 ---
st.header("📌 快速功能導覽")
c1, c2 = st.columns(2)
c1.info("👉 請點選左側選單進入 **[📊 體適能評測]**")
c2.warning("👉 老師請點選左側 **[🔐 老師管理後台]**")















































