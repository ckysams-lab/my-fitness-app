import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. 頁面設定
st.set_page_config(page_title="器材管理系統", layout="wide")

# 2. 側邊欄 (保持全站統一)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] a { font-size: 20px !important; }
        .sidebar-title { font-size: 26px !important; font-weight: bold; color: #FFD700; text-align: center; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<p class="sidebar-title">正覺蓮社學校<br>體育組</p>', unsafe_allow_html=True)
    st.divider()
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    st.page_link("pages/1_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_admin.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_equipment.py", label="器材管理", icon="🏸")

# 3. 主內容區
st.title("🏸 體育器材管理中心")

# 密碼保護 (只有老師能改)
pwd = st.sidebar.text_input("管理員密碼", type="password")
if pwd == "8888":
    st.success("權限確認：您可以進行器材盤點")
    
    # Google Sheets 連結 (請換成您的「器材表」連結)
    sheet_url = "您的器材管理Google_Sheets網址"
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1AcO-acwC1Or1p_tKsy_JWx1furOaugpSoVkV15OZDcE/edit?usp=sharing", ttl="0s")
        
        # 數據清理與計算
        df['總數量'] = pd.to_numeric(df['總數量'], errors='coerce').fillna(0)
        df['借出數量'] = pd.to_numeric(df['借出數量'], errors='coerce').fillna(0)
        df['現有庫存'] = df['總數量'] - df['借出數量']

        # --- 數據儀表板 ---
        col1, col2, col3 = st.columns(3)
        col1.metric("器材種類", len(df))
        col2.metric("已借出總數", int(df['借出數量'].sum()))
        col3.metric("需補充項", len(df[df['現有庫存'] <= 2]))

        st.divider()

        # --- 器材清單 ---
        st.subheader("📦 全校器材實時清單")
        
        # 使用自定義表格樣式
        st.dataframe(
            df,
            column_config={
                "器材名稱": st.column_config.TextColumn("器材名稱", width="medium"),
                "借出數量": st.column_config.ProgressColumn(
                    "借出進度", 
                    help="顯示借出比例",
                    min_value=0, 
                    max_value=int(df['總數量'].max() if not df.empty else 100),
                    format="%d"
                ),
                "現有庫存": st.column_config.NumberColumn("剩餘可借", format="%d 🟢"),
                "存放位置": "位置"
            },
            hide_index=True,
            use_container_width=True
        )

        # --- 快速搜尋功能 ---
        search = st.text_input("🔍 快速搜尋器材 (如：足球、壁球拍)")
        if search:
            result = df[df['器材名稱'].str.contains(search)]
            st.write(result)

    except Exception as e:
        st.info("請在 Google Sheets 建立標題為：器材名稱、總數量、借出數量、存放位置 的表格。")
        # st.error(e)

else:
    st.warning("🔒 請在左側輸入密碼以查看詳細庫存。")
    st.info("此頁面僅供體育組老師及體育長管理器材使用。")
