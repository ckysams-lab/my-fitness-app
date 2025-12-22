import streamlit as st
import pandas as pd

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

# --- 第二部分：壁球隊排名榜 (新加入) ---
st.header("🏆 壁球隊成員排名榜 (Top 8)")

# 模擬數據 (老師以後可以從 CSV 或 Database 讀取)
squash_data = {
    "排名": ["🥇 1", "🥈 2", "🥉 3", "4", "5", "6", "7", "8"],
    "隊員姓名": ["陳大文", "李小龍", "張學友", "黃金發", "周杰倫", "林俊傑", "陳奕迅", "張家輝"],
    "積分": [950, 920, 885, 850, 820, 795, 750, 710]
}
df_squash = pd.DataFrame(squash_data)

col_table, col_note = st.columns([1.5, 1])

with col_table:
    # 顯示排名表格，隱藏索引
    st.table(df_squash.set_index('排名'))

with col_note:
    st.markdown("""
    ### 📢 榜單說明
    本排名根據以下標準計算：
    1. **校內選拔賽** 積分 (60%)
    2. **出席率與訓練表現** (20%)
    3. **校際比賽** 成績 (20%)
    
    ---
    **💡 小提示：**
    前 8 名隊員將獲得代表學校參加 **下屆全港校際壁球錦標賽** 的優先資格！
    """)
    st.success("🔥 爭取進入前八強，為校爭光！")

st.divider()

# --- 第三部分：快速入口卡片 ---
st.header("📌 快速功能導覽")
c1, c2 = st.columns(2)
c1.info("👉 請點選左側選單進入 **[📊 體適能評測]**")
c2.warning("👉 老師請點選左側 **[🔐 老師管理後台]**")












































