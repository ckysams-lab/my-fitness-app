import streamlit as st

# 1. 頁面設定
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# 2. 隱藏系統預設的側邊欄導航 (避免它出現在標題上方)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# 3. 手動構建側邊欄：標題置頂，選單在下
with st.sidebar:
    st.markdown("### 正覺蓮社學校 體育組")
    st.markdown("🏆")  # 獎盃 Emoji
    st.divider()      # 分隔線
    
    # 這裡手動放上您的頁面連結，因為是純英文路徑，保證不會報錯
    st.page_link("app.py", label="首頁", icon="🏠")
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































