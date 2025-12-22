import streamlit as st

# 1. 頁面設定
st.set_page_config(page_title="正覺體育人", page_icon="🏫", layout="wide")

# 2. 側邊欄樣式與功能控制 (CSS)
st.markdown("""
    <style>
        /* 隱藏原生導航，防止出現重複選單 */
        [data-testid="stSidebarNav"] {display: none;}
        
        /* 放大側邊欄連結字體 */
        [data-testid="stSidebar"] a {
            font-size: 22px !important;
            margin-bottom: 10px;
        }
        
        /* 放大 Markdown 標題字體 */
        [data-testid="stSidebar"] h3 {
            font-size: 28px !important;
            font-weight: bold;
            color: #FFD700;
            text-align: center;
        }

        /* 讓 divider 顏色明顯一點 */
        hr { margin-top: 1rem; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.2); }
    </style>
""", unsafe_allow_html=True)

# 3. 側邊欄設定
with st.sidebar:
    # 1. 顯示標題
    st.markdown("### 正覺蓮社學校\n### 體育組")
    
    # 2. 插入縮小版校徽 (置中並控制寬度)
    st.markdown('<div style="text-align: center;"><img src="https://www.bclps.edu.hk/it-school/php/web_content/624/logo.png" width="100"></div>', unsafe_allow_html=True)
    
    st.divider()
    
    # 3. 手動放置頁面選單 (請務必確認與 GitHub 檔名完全一致)
    
    # 首頁 (根目錄)
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    
    # 體適能評測 (注意：GitHub 檔案是 "1_體適能評測.py")
    st.page_link("pages/1_體適能評測.py", label="體適能評測", icon="📊")
    
    # 老師管理後台 (注意：GitHub 檔案是 "02_admin.py")
    st.page_link("pages/02_admin.py", label="老師管理後台", icon="🔐")









































