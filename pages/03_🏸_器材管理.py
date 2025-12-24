import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# 1. 頁面基本配置 (必須在第一行)
st.set_page_config(page_title="器材管理", layout="wide")

# 2. Sidebar 導航 (確保導航欄一致)
with st.sidebar:
    st.markdown("### 🏫 正覺蓮社學校\n### 🏆 體育組管理系統")
    st.divider()
    st.page_link("🏠_首頁.py", label="系統首頁", icon="🏠")
    st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")

# 3. 頁面標題
st.title("🏸 體育器材管理系統")

# 4. Google Sheets 連線
sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# 5. 新增借用紀錄邏輯
with st.expander("➕ 新增借用紀錄"):
    with st.form("borrow_form"):
        item = st.selectbox("器材名稱", ["羽毛球拍", "乒乓球拍", "足球", "籃球", "跳繩"])
        qty = st.number_input("數量", 1, 10, 1)
        borrower = st.text_input("借用人班級姓名")
        submit = st.form_submit_button("確認提交")
        
        if submit:
            if borrower:
                try:
                    # 準備新紀錄 (加入香港時間)
                    hk_now = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
                    new_data = pd.DataFrame([{
                        "借用時間": hk_now,
                        "器材名稱": item,
                        "數量": qty,
                        "借用人": borrower,
                        "狀態": "借用中"
                    }])
                    
                    # 讀取現有紀錄並合併 (Worksheet 名稱為 'borrow_logs')
                    # 注意：請確保你的 Google Sheet 裡面有一個分頁叫 borrow_logs
                    df_logs = conn.read(spreadsheet=sheet_url, worksheet="borrow_logs", ttl="0s")
                    updated_logs = pd.concat([df_logs, new_data], ignore_index=True)
                    conn.update(spreadsheet=sheet_url, worksheet="borrow_logs", data=updated_logs)
                    
                    st.success(f"✅ 已紀錄：{borrower} 借用 {qty} 件 {item}")
                except Exception as e:
                    st.error(f"⚠️ 紀錄失敗，請檢查 Google Sheets 分頁 'borrow_logs' 是否存在。")
            else:
                st.warning("請輸入借用人姓名")

# 6. 顯示現時庫存
st.subheader("📦 現時器材庫存")
try:
    # 讀取 inventory 分頁
    df_inv = conn.read(spreadsheet=sheet_url, worksheet="inventory", ttl="0s")
    st.dataframe(df_inv, use_container_width=True, hide_index=True)
except:
    st.info("💡 提示：請在 Google Sheets 建立一個名為 'inventory' 的分頁來管理庫存。")

# 7. 顯示借用流水賬 (方便老師查閱)
st.subheader("📋 最近借用紀錄")
try:
    df_show_logs = conn.read(spreadsheet=sheet_url, worksheet="borrow_logs", ttl="0s")
    st.dataframe(df_show_logs.tail(10), use_container_width=True, hide_index=True) # 只顯示最後 10 筆
except:
    pass
