import streamlit as st

# 1. 頁面設定必須在第一行，且不要在 sidebar 裡放太多東西
st.set_page_config(
    page_title="正覺體育人", 
    page_icon="🏫", 
    layout="wide",
    initial_sidebar_state="expanded" # 強制展開側邊欄
)

# 2. 主頁面內容
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

# 3. 簡化側邊欄（只放必要的資訊）
st.sidebar.image("https://img.icons8.com/fluency/96/trophy.png", width=60)
st.sidebar.caption("正覺蓮社學校 體育組")




























