import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. 樣式設定 (僅保留字體放大，剷除隱藏側邊欄的 CSS) ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] a { font-size: 20px !important; }
        .sidebar-header { font-size: 26px !important; font-weight: bold; color: #FFD700; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 全校體適能數據管理")

# --- 2. 嚴格密碼鎖 ---
# 提示：為了美觀，您可以考慮將密碼框放在 st.sidebar 裡
pwd = st.text_input("請輸入管理員密碼", type="password")

if pwd == "8888":
    st.success("身分驗證成功")
    conn = st.connection("gsheets", type=GSheetsConnection)
    url = "https://docs.google.com/spreadsheets/d/1KNota1LPNmDtg5qIgSzKQjc_5BGvxNB8mdPO-aPCgUk/edit"
    
    try:
        all_data = conn.read(spreadsheet=url, ttl=0)
        
        # 數據概覽卡片
        col1, col2, col3 = st.columns(3)
        col1.metric("已測評人數", len(all_data))
        # 處理空值避免報錯
        avg_score = round(all_data['總分'].mean(), 1) if '總分' in all_data.columns else 0
        max_score = all_data['總分'].max() if '總分' in all_data.columns else 0
        
        col1.metric("已測評人數", len(all_data))
        col2.metric("平均總分", avg_score)
        col3.metric("最高得分", max_score)
        
        st.divider()
        
        # 數據篩選與表格
        if '所屬校隊' in all_data.columns:
            teams = all_data['所屬校隊'].unique()
            team_filter = st.multiselect("篩選校隊", options=teams, default=teams)
            filtered_df = all_data[all_data['所屬校隊'].isin(team_filter)]
        else:
            filtered_df = all_data
        
        st.subheader("📋 完整數據清單")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # 下載功能
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("💾 下載篩選後的 CSV 報表", csv, "School_Fitness_Data.csv", "text/csv")
        
    except Exception as e:
        st.error(f"讀取失敗，請檢查 Google Sheet 欄位名稱是否正確。")
        
elif pwd != "":
    st.error("密碼錯誤，請重試")
else:
    st.info("💡 請輸入密碼以解鎖全校學生數據。")
