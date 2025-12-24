import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. 頁面配置
st.set_page_config(page_title="體育之星 - 正覺蓮社學校", layout="wide")

# 2. Sidebar 導航
with st.sidebar:
    st.markdown("### 🏫 正覺蓮社學校\n### 🏆 體育組管理系統")
    st.divider()
    st.page_link("🏠_首頁.py", label="系統首頁", icon="🏠")
    st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")
    st.page_link("pages/04_🌟_體育之星.py", label="體育之星", icon="🌟")

# 3. 樣式美化
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%); }
    .star-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        border: 2px solid #FFD700;
        text-align: center;
        transition: transform 0.3s;
        margin-bottom: 20px;
    }
    .star-card:hover { transform: translateY(-10px); background: rgba(255, 255, 255, 0.15); }
    .star-img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #FFD700;
        margin-bottom: 15px;
    }
    .team-badge {
        background: #FFD700;
        color: black;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .award-text { color: #00FFCC; font-weight: bold; font-style: italic; }
    h1, h2, h3, p { color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🌟 年度校隊體育之星")
st.markdown("### 榮耀時刻：表揚各校隊表現最傑出之運動員")

# 4. 數據連線
sheet_url = "https://docs.google.com/spreadsheets/d/1KNota1LPNmDtg5qIgSzKQjc_5BGvxNB8mdPO-aPCgUk/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 讀取體育之星數據 (建議在 Google Sheet 建立一個名為 'stars' 的分頁)
    # 欄位：年度, 班別, 姓名, 所屬校隊, 獎項, 照片URL
    df_stars = conn.read(spreadsheet=sheet_url, worksheet="stars", ttl="0s")
    
    # 選擇年度
    years = sorted(df_stars['年度'].unique(), reverse=True)
    selected_year = st.selectbox("📅 選擇學年", years)
    
    filtered_df = df_stars[df_stars['年度'] == selected_year]
    
    # 顯示星章
    cols = st.columns(3) # 每行顯示 3 位學生
    
    for i, (idx, row) in enumerate(filtered_df.iterrows()):
        with cols[i % 3]:
            # 處理照片：如果冇 URL 則用預設圖
            img_url = row['照片URL'] if pd.notna(row['照片URL']) else "https://cdn-icons-png.flaticon.com/512/1041/1041262.png"
            
            st.markdown(f"""
                <div class="star-card">
                    <div class="team-badge">{row['所屬校隊']}</div>
                    <img src="{img_url}" class="star-img">
                    <h2>{row['姓名']} <small>({row['班別']})</small></h2>
                    <p class="award-text">🏆 {row['獎項']}</p>
                </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.info("💡 請在 Google Sheets 建立 'stars' 分頁，並填入：年度、班別、姓名、所屬校隊、獎項、照片URL。")
