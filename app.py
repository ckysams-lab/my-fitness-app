import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. 頁面與連線設定
st.set_page_config(page_title="小學體適能數位戰報系統", page_icon="🏃‍♂️", layout="wide")

# 建立雲端連線
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"連線設定錯誤: {e}")

# 2. 定義功能函數 (調整為 10 分制)
def load_data():
    try:
        with open('norms.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def get_score(val, gender, age, item_key, data):
    try:
        thresholds = data[item_key][gender][str(age)]
        for i, t in enumerate(thresholds):
            if val >= t: 
                return 10 - (i * 2)  # 原本 5,4,3,2,1 變為 10,8,6,4,2 分
        return 0
    except: return 0

# --- 主介面 ---
st.title("🚀 小學體適能智慧評測系統 (40分制版本)")
data = load_data()

if data:
    # 3. 建立表單輸入區
    with st.form("input_form"):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            gender = st.radio("性別", ["男", "女"], horizontal=True)
            age = st.number_input("年齡", 5, 13, 10)
        with col2:
            name = st.text_input("學生姓名/編號", "學生A")
            current_team = st.selectbox("目前所屬校隊", ["無", "足球隊", "壁球隊", "乒乓球隊", "籃球隊", "田徑隊", "射箭隊"])
            enable_cam = st.checkbox("📸 開啟相機拍攝球員照")
            
        with col3:
            h = st.number_input("身高 (cm)", 100.0, 180.0, 140.0)
            w = st.number_input("體重 (kg)", 15.0, 90.0, 35.0)

        # 相機放在表單內，但在提交按鈕前
        photo = None
        if enable_cam:
            photo = st.camera_input("請對準學生拍照")

        st.markdown("---")
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        v1 = v_col1.number_input("仰臥起坐 (次)", 0)
        v2 = v_col2.number_input("坐姿體前彎 (cm)", 0)
        v3 = v_col3.number_input("手握力 (kg)", 0.0, 100.0, 10.0)
        v4 = v_col4.number_input("9分鐘耐力跑 (米)", 0)
        
        submitted = st.form_submit_button("🌟 生成個人戰報")

    # 4. 提交後的處理 (核心邏輯)
    if submitted:
        # A. 計算分數
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data) 
        s3 = get_score(v3, gender, age, "grip_strength", data)
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4

        # B. 決定等級 (標準隨總分 40 同步調整)
        if total >= 32:
            rgb, rank_label = "255, 215, 0", "🥇 卓越 (GOLD ELITE)"
        elif total >= 24:
            rgb, rank_label = "0, 212, 255", "🥈 優良 (SILVER PRO)"
        elif total >= 16:
            rgb, rank_label = "255, 140, 0", "🥉 尚可 (BRONZE)"
        else:
            rgb, rank_label = "255, 46, 99", "⚪ 待加強 (CHALLENGER)"

        accent = f"rgb({rgb})"
        
        # C. 注入 CSS
        st.markdown(f"""
            <style>
            .stApp {{ background: radial-gradient(circle, #1A1A2E 0%, #0F0F1B 100%); color: white !important; }}
            .header-box {{ background-color: {accent}; padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 0 20px {accent}; margin-bottom: 25px; color: black !important; }}
            .metric-card {{ background: rgba(255,255,255,0.05); border-left: 5px solid {accent}; padding: 15px; border-radius: 10px; }}
            div[data-testid="stProgress"] > div > div > div > div {{ background-color: {accent} !important; }}
            h1, h2, h3, h4, p, span, label {{ color: white !important; }}
            </style>
        """, unsafe_allow_html=True)

        # D. 個人戰報抬頭
        st.markdown(f'<div class="header-box"><h1 style="color:black !important; margin:0;">{name} 體能戰報</h1><h2 style="color:black !important; margin:0;">{rank_label}</h2></div>', unsafe_allow_html=True)
        
        # --- 勳章顯示 (10 分滿分勳章) ---
        badges = []
        if s1 == 10: badges.append("🧱 鋼鐵核心")
        if s2 == 10: badges.append("🤸 柔軟大師")
        if s3 == 10: badges.append("⚡ 神力超人")
        if s4 == 10: badges.append("🔥 耐力之王")
        
        if badges:
            b_cols = st.columns(len(badges))
            for i, b in enumerate(badges):
                b_cols[i].success(f"🏅 {b}")

        # E. 數據看板 (顯示 40 分)
        st.write("")
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card"><h4>總得分</h4><h2 style="color:{accent} !important;">{total} / 40</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><h4>BMI 指數</h4><h2 style="color:{accent} !important;">{bmi}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><h4>目前隊伍</h4><h2 style="color:{accent} !important;">{current_team}</h2></div>', unsafe_allow_html=True)

        # F. 體能球員卡看板 (優化照片顯示邏輯)
        st.divider()
        g1, g2, g3 = st.columns([1, 1.2, 1]) 
        
        with g1:
            st.markdown("### 👤 選手動態")
            # 優先檢查本次提交的 photo 變數
            if photo is not None:
                st.image(photo, use_container_width=True, caption="本次實拍")
                st.markdown(f"<p style='text-align:center; color:{accent} !important;'><b>{current_team} 成員</b></p>", unsafe_allow_html=True)
            else:
                # 顯示預設頭像
                st.markdown(f"""
                    <div style="height:220px; background:rgba(255,255,255,0.05); 
                                display:flex; align-items:center; justify-content:center; 
                                border: 2px dashed {accent}; border-radius:15px;">
                        <div style="text-align:center;">
                            <span style="font-size:4rem;">👤</span><br>
                            <span style="font-size:0.8rem; color:#888;">未偵測到照片</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
        # G. 運動建議 (針對 10 分制判定)
        st.divider()
        st.subheader("🎯 運動處方與推薦")
        rec_col1, rec_col2 = st.columns(2)
        with rec_col1:
            if s4 >= 8: st.success("⚽ **推薦社團：足球 / 田徑**")
            elif s3 >= 8: st.success("🎾 **推薦社團：壁球 / 乒乓球**")
            elif s1 >= 8: st.success("🏀 **推薦社團：籃球**")
            else: st.info("🏃 **建議：** 多方嘗試找出最有興趣的項目！")
        with rec_col2:
            if s2 <= 4: st.warning("🧘 **改善建議：** 加強每天的坐姿體前彎伸展。")
            if s4 <= 4: st.warning("🏃 **改善建議：** 每週增加心肺耐力訓練。")

        # H. 雲端同步
        try:
            res_df = pd.DataFrame([{
                "時間": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "姓名": name, "性別": gender, "年齡": age, "所屬校隊": current_team,
                "BMI": bmi, "總分": total, "仰臥起坐": v1, "體前彎": v2, "手握力": v3, "9分鐘耐力跑": v4
            }])
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, res_df], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ 數據已自動同步至雲端！")
        except:
            st.warning("⚠️ 雲端同步失敗，請手動下載。")

        st.download_button("📥 下載本次戰報", res_df.to_csv(index=False).encode('utf-8-sig'), f"{name}_40pts.csv")

        # I. 老師大盤分析 (大盤數據同步顯示新分數)
        with st.expander("📊 老師專屬：大盤分析"):
            all_db = conn.read(ttl=0)
            if not all_db.empty:
                st.bar_chart(all_db.groupby("所屬校隊")["總分"].mean())
                st.write("⚠️ **低分關注名單 (總分 < 16)**")
                st.dataframe(all_db[all_db["總分"] < 16][["姓名", "總分", "所屬校隊"]])
else:
    st.error("❌ 找不到 norms.json 數據庫！")
























