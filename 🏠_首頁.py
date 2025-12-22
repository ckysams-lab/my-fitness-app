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
    # 顯示校名
    st.markdown("### 正覺蓮社學校\n### 體育組")
    
    # 插入縮小版校徽 (置中)
    st.markdown('<div style="text-align: center;"><img src="https://www.bclps.edu.hk/it-school/php/web_content/624/logo.png" width="120"></div>', unsafe_allow_html=True)
    
    st.divider()
    
    # --- 手動導航連結 ---
    # 規則：如果 GitHub 檔名有 Emoji 或空格，字串必須精確匹配
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    
    # 使用 try-except 防止單一頁面報錯導致整個側邊欄崩潰
    try:
        st.page_link("pages/1_體適能評測.py", label="體適能評測", icon="📊")
    except:
        # 如果 GitHub 上其實沒有 '1_' 開頭，嘗試自動尋找
        st.warning("請確認 '1_體適能評測.py' 檔名正確")

    try:
        st.page_link("pages/02_admin.py", label="老師管理後台", icon="🔐")
    except:
        st.warning("請確認 '02_admin.py' 檔名正確")









































