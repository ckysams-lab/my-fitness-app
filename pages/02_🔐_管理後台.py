import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import requests
import base64
from PIL import Image
import io

# 1. 頁面基本配置 (必須放在第一行)
st.set_page_config(page_title="老師管理後台", layout="wide")

# 2. Sidebar 導航
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
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    st.title("🔐 體育組後台登入")
    pwd_input = st.text_input("請輸入老師專用密碼", type="password")
    if st.button("確認登入"):
        if pwd_input == "123456":  # <-- 密碼喺呢度改
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ 密碼錯誤，請重新輸入。")
    return False

# 執行驗證
if check_password():
    st.title("🔐 老師管理後台")

    # 4. Google Sheets 連線設定
    sheet_url = "https://docs.google.com/spreadsheets/d/1KNota1LPNmDtg5qIgSzKQjc_5BGvxNB8mdPO-aPCgUk/edit?usp=sharing"
    conn = st.connection("gsheets", type=GSheetsConnection)

    tab1, tab2, tab3 = st.tabs(["📊 數據總覽", "⚙️ 系統設定", "🌟 發佈體育之星"])

    with tab1:
        st.subheader("學生評測數據紀錄")
        try:
            df = conn.read(spreadsheet=sheet_url, worksheet="data", ttl="0s")
            search_q = st.text_input("🔍 搜尋學生姓名 / 編號", "")
            if search_q:
                df = df[df['姓名'].str.contains(search_q, na=False)]
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 下載數據 CSV", data=csv, file_name="fitness_data.csv", mime="text/csv")
        except:
            st.info("暫時未有數據紀錄。")

    with tab2:
        st.subheader("⚙️ 系統管理")
        st.write("目前狀態：**已授權登入**")
        if st.button("🔴 安全登出"):
            st.session_state["password_correct"] = False
            st.rerun()
        st.divider()
        st.warning("⚠️ 權限說明：此處僅供體育組老師查閱及下載數據。")

    with tab3:
        st.subheader("📝 發佈年度校隊體育之星")
        
        # 老師你的 ImgBB API Key 已放入
        API_KEY = "8c4237f6fd2bdbdcb8c215d0ea306e0f" 

        with st.form("star_upload_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                s_year = st.selectbox("學年", ["2024-25", "2025-26"])
                s_team = st.selectbox("所屬校隊", ["足球隊", "乒乓球隊", "籃球隊", "田徑隊", "羽毛球隊", "射箭隊", "壁球隊"])
                s_class = st.text_input("班別 (如: 6C)")
                s_name = st.text_input("學生姓名")
            with col2:
                s_award = st.text_input("獎項 (如: 年度最有價值球員)")
                s_file = st.file_uploader("上傳學生照片", type=["jpg", "png", "jpeg"])
            
            submit_star = st.form_submit_button("🚀 確定發佈")

            if submit_star:
                if s_file and s_name and s_class:
                    try:
                        with st.spinner('正在優化相片並發佈中...'):
                            # 1. 圖片壓縮處理
                            img = Image.open(s_file)
                            img.thumbnail((800, 800)) 
                            buffer = io.BytesIO()
                            img = img.convert("RGB")
                            img.save(buffer, format="JPEG", quality=85)
                            
                            # 2. 上傳到 ImgBB
                            img_base64 = base64.b64encode(buffer.getvalue())
                            res = requests.post("https://api.imgbb.com/1/upload", {"key": API_KEY, "image": img_base64})
                            res_data = res.json()
                            
                            if res.status_code == 200:
                                final_url = res_data['data']['url']
                                
                                # 3. 準備寫入 Google Sheet
                                new_star = pd.DataFrame([{
                                    "年度": s_year, 
                                    "班別": s_class, 
                                    "姓名": s_name,
                                    "所屬校隊": s_team, 
                                    "獎項": s_award, 
                                    "照片URL": final_url
                                }])

                                try:
                                    existing_df = conn.read(spreadsheet=sheet_url, worksheet="stars", ttl="0s")
                                    if existing_df is not None and not existing_df.empty:
                                        updated_df = pd.concat([existing_df, new_star], ignore_index=True)
                                    else:
                                        updated_df = new_star
                                except:
                                    updated_df = new_star
                                
                                conn.update(spreadsheet=sheet_url, worksheet="stars", data=updated_df)
                                st.success(f"✅ {s_name} 的資料已成功發佈！")
                                st.balloons()
                            else:
                                st.error(f"❌ 相片上傳失敗：{res_data.get('error', {}).get('message', '未知錯誤')}")
                    except Exception as e:
                        st.error(f"❌ 系統錯誤：{str(e)}")
                else:
                    st.warning("⚠️ 請填寫姓名、班別並上傳相片。")
