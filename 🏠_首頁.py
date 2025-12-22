import streamlit as st

# 1. 頁面設定
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")
# 1. 放大側邊欄字體的 CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            font-size: 1.2rem; /
        }
        
        [data-testid="stSidebar"] h3 {
            font-size: 28px !important; /
            font-weight: bold;
            color: #FFD700; /
        }

        [data-testid="stSidebar"] a {
            font-size: 20px !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. 隱藏預設選單，確保「正覺體育組」在最上方
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# 3. 側邊欄設定 (請確保這裡的縮排完全整齊)
with st.sidebar:
    # 1. 顯示標題
    st.markdown("### 正覺蓮社學校 體育組")
    
    # 2. 插入縮小版校徽 (加上置中與大小控制)
    st.markdown('<div style="text-align: center;"><img src="https://www.bclps.edu.hk/it-school/php/web_content/624/logo.png" width="100"></div>', unsafe_allow_html=True)
    
    st.divider()
    
    # 3. 手動放置頁面選單 (修正路徑)
    # 不論在哪個頁面，Streamlit 官方建議從根目錄開始寫，但不加第一個斜線
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    st.page_link("pages/1_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_admin.py", label="老師管理後台", icon="🔐")

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









































