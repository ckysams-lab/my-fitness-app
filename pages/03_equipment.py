import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. 樣式設定 (移除隱藏側邊欄的代碼) ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] a { font-size: 20px !important; }
        .sidebar-title { font-size: 26px !important; font-weight: bold; color: #FFD700; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 主內容區 ---
st.title("🏸 體育器材管理中心")

# 密碼保護 (這裡保留 st.sidebar.text_input，它會出現在新導覽選單的下方)
with st.sidebar:
    st.markdown('<p class="sidebar-title">管理員驗證</p>', unsafe_allow_html=True)
    pwd = st.text_input("管理員密碼", type="password")

if pwd == "8888":
    st.success("權限確認：您可以進行器材盤點")
    
    # Google Sheets 連結
    url = "https://docs.google.com/spreadsheets/d/1AcO-acwC1Or1p_tKsy_JWx1furOaugpSoVkV15OZDcE/edit?usp=sharing"
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=url, ttl="0s")
        
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
        
        st.dataframe(
            df,
            column_config={
                "器材名稱": st.column_config.TextColumn("器材名稱", width="medium"),
                "借出數量": st.column_config.ProgressColumn(
                    "借出進度", 
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
            result = df[df['器材名稱'].str.contains(search, case=False, na=False)]
            st.write(result)

    except Exception as e:
        st.info("請在 Google Sheets 建立標題為：器材名稱、總數量、借出數量、存放位置 的表格。")

else:
    st.warning("🔒 請在左側輸入密碼以查看詳細庫存。")
    st.info("此頁面僅供體育組老師及體育長管理器材使用。")
