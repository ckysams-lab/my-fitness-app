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

# 3. 頁面標題
st.title("🔐 老師管理後台")

# 4. Google Sheets 連線設定
sheet_url = "https://docs.google.com/spreadsheets/d/1KNota1LPNmDtg5qIgSzKQjc_5BGvxNB8mdPO-aPCgUk/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

tab1, tab2 = st.tabs(["📊 數據總覽", "⚙️ 系統設定"])

with tab1:
    st.subheader("學生評測數據紀錄")
    try:
        # 讀取最新數據 (ttl="0s" 確保不使用緩存)
        df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1KNota1LPNmDtg5qIgSzKQjc_5BGvxNB8mdPO-aPCgUk/edit?usp=sharing", worksheet="data", ttl="0s")
        
        # --- 新增：簡易篩選功能 ---
        search_q = st.text_input("🔍 搜尋學生姓名 / 編號", "")
        if search_q:
            df = df[df['姓名'].str.contains(search_q, na=False)]
        
        # 顯示表格
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 數據統計資訊
        st.write(f"📈 目前紀錄總數：{len(df)} 筆")
        
        # 下載按鈕
        csv = df.to_csv(index=False).encode('utf-8-sig') # 使用 utf-8-sig 解決 Excel 亂碼問題
        st.download_button(
            label="📥 下載篩選後的數據 CSV",
            data=csv,
            file_name=f"fitness_data_{search_q if search_q else 'all'}.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.info("暫時未有數據紀錄，或 Worksheet 名稱不符（請確認 Google Sheet 分頁名為 'data'）。")
        # st.error(f"錯誤詳情: {e}") # 除錯用

with tab2:
    st.subheader("權限管理")
    st.warning("⚠️ 此處僅供體育組老師使用。")
    st.write("未來可在此設定評分常模或刪除錯誤紀錄。")
