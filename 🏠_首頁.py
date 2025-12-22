import streamlit as st

# 1. 頁面設定
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

with st.sidebar:
    st.markdown("### 正覺蓮社學校 體育組")  # 標題置頂
    st.markdown("🏆")                   # 獎盃 Emoji (不放大，維持文字大小)
    st.divider()                        # 畫一條橫線，下方會自動接 page 選單
    
    # 提示：Streamlit 會自動在這裡插入 Pages 選單

# 3. 主頁面內容 (精彩影片等)
st.title("🌟 正覺體育人：精彩瞬間")
# ... 剩下的影片與卡片代碼 ...

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
































