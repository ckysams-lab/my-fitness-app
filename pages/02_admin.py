import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="老師管理後台", layout="wide")

# 側邊欄樣式 (與首頁保持一致)
st.markdown("""
    <style>
        [data-testid="stSidebar"] a { font-size: 20px !important; }
        .sidebar-header { font-size: 26px !important; font-weight: bold; color: #FFD700; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 全校體適能數據管理")

# 嚴格密碼鎖
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
        col2.metric("平均總分", round(all_data['總分'].mean(), 1))
        col3.metric("最高得分", all_data['總分'].max())
        
        st.divider()
        
        # 數據篩選與表格
        team_filter = st.multiselect("篩選校隊", options=all_data['所屬校隊'].unique(), default=all_data['所屬校隊'].unique())
        filtered_df = all_data[all_data['所屬校隊'].isin(team_filter)]
        
        st.subheader("📋 完整數據清單")
        st.dataframe(filtered_df, use_container_width=True)
        
        # 下載功能
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("💾 下載篩選後的 CSV 報表", csv, "School_Fitness_Data.csv", "text/csv")
        
    except Exception as e:
        st.error(f"讀取失敗：{e}")
        
elif pwd != "":
    st.error("密碼錯誤，請重試")
