import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 已剷除 st.set_page_config 與 sidebar 導航代碼 ---

st.title("⭐ 年度體育之星")
st.info("表揚各校隊中表現傑出的隊員，激勵學生追求卓越。")
st.markdown("---")

# 3. Google Sheets 連接
sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

def get_image_url(url):
    """處理 Google Drive 圖片連結轉化為直連格式"""
    if pd.isna(url) or str(url).strip() == "":
        return "https://via.placeholder.com/300x400?text=No+Photo"
    
    if "drive.google.com" in str(url):
        try:
            if 'file/d/' in url:
                file_id = url.split('file/d/')[1].split('/')[0]
            else:
                file_id = url.split('id=')[1].split('&')[0]
            return f"https://drive.google.com/uc?export=view&id={file_id}"
        except:
            return url
    return url

# 4. 讀取與顯示邏輯
try:
    df_stars = conn.read(spreadsheet=sheet_url, worksheet="stars", ttl="0s")
    
    if df_stars.empty:
        st.warning("⚠️ 目前 stars 分頁尚無資料，請先在 Google Sheet 填寫。")
    else:
        # 年度篩選器
        years = sorted(df_stars['年度'].unique(), reverse=True)
        selected_year = st.selectbox("📅 選擇年度", years)
        
        # 定義要求的六大校隊
        target_teams = ["壁球隊", "田徑隊", "籃球隊", "足球隊", "乒乓球隊", "射箭隊"]
        
        # 找出該年度有資料的隊伍
        existing_teams = df_stars[df_stars['年度'] == selected_year]['隊伍'].unique()
        
        # 循環顯示隊伍
        for team in target_teams:
            if team in existing_teams:
                st.markdown(f"## 🏆 {team}")
                team_data = df_stars[(df_stars['年度'] == selected_year) & (df_stars['隊伍'] == team)]
                
                col1, col2 = st.columns(2)
                
                # 分別顯示男、女子組
                for col, gender in zip([col1, col2], ["男", "女"]):
                    person = team_data[team_data['性別'] == gender]
                    with col:
                        if not person.empty:
                            row = person.iloc[0]
                            with st.container(border=True):
                                c_img, c_txt = st.columns([1, 1.2])
                                with c_img:
                                    img_url = get_image_url(row['相片連結'])
                                    st.image(img_url, use_container_width=True)
                                with c_txt:
                                    st.subheader(f"{gender}子組：{row['姓名']}")
                                    st.write(f"**班別：** {row['班別']} ({row['學號']})")
                                    st.write("**本年度榮譽：**")
                                    st.success(row['獎項'] if not pd.isna(row['獎項']) else "優秀運動表現")
                        else:
                            st.info(f"暫無 {team} {gender}子組資料")
                st.divider()
        
        # 顯示非名單內的其餘隊伍
        other_teams = [t for t in existing_teams if t not in target_teams]
        if other_teams:
            with st.expander("查看其他校隊"):
                for t in other_teams:
                    st.write(f"• {t}")

except Exception as e:
    st.warning("🌟 體育之星名單讀取中... 請確保 Excel 分頁名稱為 stars。")
