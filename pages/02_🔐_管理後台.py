import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. 頁面基本配置 (必須放在第一行)
st.set_page_config(page_title="老師管理後台", layout="wide")

# 2. Sidebar 導航 (確保每一頁都有一樣的導航)
with st.sidebar:
    st.markdown("### 🏫 正覺蓮社學校\n### 🏆 體育組管理系統")
    st.divider()
    st.page_link("🏠_首頁.py", label="系統首頁", icon="🏠")
    st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")
    st.page_link("pages/04_🌟_體育之星.py", label="體育之星", icon="🌟")

# --- 🔐 密碼登入保護邏輯 ---
def check_password():
    """驗證密碼，成功回傳 True"""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    # 如果已經登入成功，直接回傳
    if st.session_state["password_correct"]:
        return True

    # 登入介面
    st.title("🔐 體育組後台登入")
    pwd_input = st.text_input("請輸入老師專用密碼", type="password")
    if st.button("確認登入"):
        if pwd_input == "123456":  # <-- 老師可以在這裡修改你的密碼
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ 密碼錯誤，請重新輸入。")
    return False

# 執行驗證
if check_password():
    # --- 驗證成功後顯示的內容 ---
    st.title("🔐 老師管理後台")

    # 4. Google Sheets 連線設定
    sheet_url = "https://docs.google.com/spreadsheets/d/1KNota1LPNmDtg5qIgSzKQjc_5BGvxNB8mdPO-aPCgUk/edit?usp=sharing"
    conn = st.connection("gsheets", type=GSheetsConnection)

    tab1, tab2 = st.tabs(["📊 數據總覽", "⚙️ 系統設定"])

    with tab1:
        st.subheader("學生評測數據紀錄")
        try:
            # 讀取最新數據
            df = conn.read(spreadsheet=sheet_url, worksheet="data", ttl="0s")
            
            # 簡易篩選
            search_q = st.text_input("🔍 搜尋學生姓名 / 編號", "")
            if search_q:
                df = df[df['姓名'].str.contains(search_q, na=False)]
            
            # 顯示表格
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.write(f"📈 目前紀錄總數：{len(df)} 筆")
            
            # 下載按鈕
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 下載數據 CSV",
                data=csv,
                file_name=f"fitness_data_{search_q if search_q else 'all'}.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.info("暫時未有數據紀錄，或 Worksheet 名稱不符（請確認 Google Sheet 分頁名為 'data'）。")

    with tab2:
        st.subheader("⚙️ 系統管理")
        st.write("目前狀態：**已授權登入**")
        if st.button("🔴 安全登出"):
            st.session_state["password_correct"] = False
            st.rerun()
        
        st.divider()
        st.warning("⚠️ 權限說明：此處僅供體育組老師查閱及下載數據。")
