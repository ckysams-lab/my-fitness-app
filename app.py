import streamlit as st

st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

st.title("🌟 正覺體育人：精彩瞬間")
st.markdown("---")

# 精彩影片區 (首頁核心)
st.header("🎬 學生運動亮點")
col_v1, col_v2 = st.columns(2)
with col_v1:
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # 替換為學校連結
    st.subheader("🏃‍♂️ 9分鐘耐力跑精選")
with col_v2:
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    st.subheader("⚽ 校隊訓練花絮")

st.divider()

# 快速入口卡片
st.header("📌 快速功能導覽")
c1, c2 = st.columns(2)
c1.info("👉 **[📊 體適能評測]**：輸入成績，獲取 AI 分析與運動建議。")
c2.warning("👉 **[🔐 老師管理後台]**：僅限體育組老師查閱數據。")

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/trophy.png", width=60)
    st.caption("正覺蓮社學校 體育組")




























