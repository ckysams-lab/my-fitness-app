import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# 1. 頁面基本配置
st.set_page_config(page_title="器材管理", layout="wide")

# 2. Sidebar 導航
with st.sidebar:
    st.markdown("### 🏫 正覺蓮社學校\n### 🏆 體育組管理系統")
    st.divider()
    st.page_link("🏠_首頁.py", label="系統首頁", icon="🏠")
    st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")

# --- 🔐 密碼保護邏輯 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.title("🔐 器材管理登入")
    pwd = st.text_input("請輸入體育組專用密碼", type="password")
    if st.button("確認登入"):
        if pwd == "123456":  # <-- 密碼可以同後台一樣，或者另外設一個
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ 密碼錯誤")
    return False

# 執行驗證
if check_password():
    st.title("🏸 體育器材管理系統")

    # 4. Google Sheets 連線
    sheet_url = "https://docs.google.com/spreadsheets/d/1KNota1LPNmDtg5qIgSzKQjc_5BGvxNB8mdPO-aPCgUk/edit?usp=sharing"
    conn = st.connection("gsheets", type=GSheetsConnection)

    # 分頁顯示：借用與庫存
    tab1, tab2 = st.tabs(["📝 借用登記", "📦 庫存狀況"])

    with tab1:
        with st.expander("➕ 新增借用紀錄", expanded=True):
            with st.form("borrow_form"):
                item = st.selectbox("器材名稱", ["羽毛球拍", "乒乓球拍", "足球", "籃球", "跳繩"])
                qty = st.number_input("數量", 1, 10, 1)
                borrower = st.text_input("借用人班級姓名")
                submit = st.form_submit_button("確認提交")
                
                if submit:
                    if borrower:
                        try:
                            # 修正香港時間
                            hk_now = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
                            new_log = pd.DataFrame([{
                                "借用時間": hk_now,
                                "器材名稱": item,
                                "數量": qty,
                                "借用人": borrower,
                                "狀態": "借用中"
                            }])
                            
                            # 讀取並更新 borrow_logs 分頁
                            df_logs = conn.read(spreadsheet=sheet_url, worksheet="borrow_logs", ttl="0s")
                            updated_logs = pd.concat([df_logs, new_log], ignore_index=True)
                            conn.update(spreadsheet=sheet_url, worksheet="borrow_logs", data=updated_logs)
                            st.success(f"✅ 紀錄成功：{borrower} 已借用 {item}")
                        except:
                            st.error("⚠️ 寫入失敗，請確認 Sheets 中有 'borrow_logs' 分頁。")
                    else:
                        st.warning("請填寫借用人姓名。")

        st.subheader("📋 最近借用流水賬")
        try:
            df_show = conn.read(spreadsheet=sheet_url, worksheet="borrow_logs", ttl="0s")
            st.dataframe(df_show.tail(15), use_container_width=True, hide_index=True)
        except:
            st.info("暫無借用紀錄。")

    with tab2:
        st.subheader("📦 現時器材庫存")
        try:
            df_inv = conn.read(spreadsheet=sheet_url, worksheet="inventory", ttl="0s")
            st.dataframe(df_inv, use_container_width=True, hide_index=True)
        except:
            st.info("請在 Google Sheets 建立 'inventory' 分頁。")
        
        if st.button("🔴 安全登出系統"):
            st.session_state["password_correct"] = False
            st.rerun()
