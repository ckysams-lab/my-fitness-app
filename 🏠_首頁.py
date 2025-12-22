import streamlit as st

# 1. 頁面設定
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# 2. 隱藏預設選單，確保「正覺體育組」在最上方
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# 3. 側邊欄設定 (請確保這裡的縮排完全整齊)
with st.sidebar:
    st.markdown("### 正覺蓮社學校 體育組")
    st.markdown("🏆")
    st.divider()
    
    # 手動放置頁面選單 (請確保 GitHub 上的 pages 裡面檔案叫 01_fitness.py)
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    st.page_link("pages/01_fitness.py", label="體適能評測", icon="📊")

# 4. 主頁面內容
st.title("🌟 正覺體育人：精彩瞬間")
st.markdown("---")

# 精彩影片區
st.header("🎬 學生運動亮點")
col_v1, col_v2 = st.columns(2)
with col_v1:
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    st.subheader("🏃‍♂️ 9分鐘耐力跑精選")
with col_v2:
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    st.subheader("⚽ 校隊訓練花絮")

st.divider()

# 快速入口卡片
st.header("📌 快速功能導覽")
c1, c2 = st.columns(2)
c1.info("👉 請點選左側選單進入 **[📊 體適能評測]**")
c2.warning("👉 老師請點選左側 **[🔐 老師管理後台]**")

































