import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from utils import load_norms, get_score  # 確保 utils.py 在根目錄

# 1. 頁面基本設定
st.set_page_config(page_title="體適能評測", layout="wide")

# 2. 準備環境
data = load_norms()
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"雲端連線異常: {e}")

# 3. 頁面標題
st.title("📊 學生體適能評測系統")
st.markdown("請在下方輸入測驗數據，系統將自動生成 AI 分析戰報。")

if data:
    # --- A. 輸入區域 (Form) ---
    with st.form("input_form"):
        st.subheader("📝 基本資料")
        col1, col2, col3 = st.columns(3)
        with col1:
            gender = st.radio("性別", ["男", "女"], horizontal=True)
            age = st.number_input("年齡", 5, 13, 10)
        with col2:
            name = st.text_input("學生姓名/編號", "學生A")
            current_team = st.selectbox("目前所屬校隊", ["無", "足球隊", "壁球隊", "乒乓球隊", "籃球隊", "田徑隊", "射箭隊"])
        with col3:
            h = st.number_input("身高 (cm)", 100.0, 180.0, 140.0)
            w = st.number_input("體重 (kg)", 15.0, 90.0, 35.0)

        st.divider()
        st.subheader("💪 測驗數據")
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        v1 = v_col1.number_input("仰臥起坐 (次)", 0)
        v2 = v_col2.number_input("坐姿體前彎 (cm)", 0)
        v3 = v_col3.number_input("手握力 (kg)", 0.0, 100.0, 10.0)
        v4 = v_col4.number_input("9分鐘耐力跑 (米)", 0)
        
        submitted = st.form_submit_button("🌟 生成個人戰報並啟動 AI 分析")

    # --- B. 提交後的結果顯示區域 ---
    if submitted:
        # 修正香港時間
        hk_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
        
        # 1. 核心數據計算
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data) 
        s3 = get_score(v3, gender, age, "grip_strength", data)
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4
        categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘跑']
        scores = [s1, s2, s3, s4]

        # 2. 視覺化風格定義
        if total >= 32: rgb, rank_label = "255, 215, 0", "🥇 卓越 (GOLD)"
        elif total >= 24: rgb, rank_label = "0, 212, 255", "🥈 優良 (SILVER)"
        elif total >= 16: rgb, rank_label = "255, 140, 0", "🥉 尚可 (BRONZE)"
        else: rgb, rank_label = "255, 46, 99", "⚪ 待加強 (CHALLENGER)"
        accent = f"rgb({rgb})"

        st.markdown(f"""
            <style>
            .stApp {{ background: radial-gradient(circle, #1A1A2E 0%, #0F0F1B 100%); }}
            .header-box {{ background-color: {accent}; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; }}
            .header-box h1 {{ color: black !important; margin: 0; font-size: 2.5rem; }}
            .badge {{ background: white; color: black !important; padding: 10px 30px; border-radius: 50px; font-weight: bold; font-size: 1.2rem; display: inline-block; margin-top: 15px; }}
            .metric-card {{ background: rgba(255,255,255,0.08); border-left: 6px solid {accent}; padding: 20px; border-radius: 12px; margin: 10px 0; }}
            h3, h4, p, span, div {{ color: white; }}
            </style>
            <div class="header-box">
                <h1>{name} 同學的體能戰報</h1>
                <div class="badge">{rank_label}</div>
            </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card"><h4>總分</h4><h2 style="color:{accent}">{total} / 40</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><h4>BMI 指數</h4><h2 style="color:{accent}">{bmi}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><h4>狀態</h4><h2 style="color:{accent}">{rank_label.split()[1]}</h2></div>', unsafe_allow_html=True)

        st.divider()

        # 3. 雷達圖與分析內容
        g_col1, g_col2 = st.columns([1.2, 1])
        with g_col1:
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]], theta=categories + [categories[0]],
                fill='toself', fillcolor=f"rgba({rgb}, 0.3)",
                line=dict(color=accent, width=4)
            ))
            fig.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 10], gridcolor="#444")),
                paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white", size=14), height=500
            )
            st.plotly_chart(fig, use_container_width=True)

        with g_col2:
            st.subheader("🤖 AI 智能助教評語")
            # --- 跟返你原創嘅推薦邏輯 ---
            recs = []
            if s1 >= 8: recs.append("⚽ 足球/籃球 (需要核心)")
            if s2 >= 8: recs.append("🧘 中國舞 (柔軟度優)")
            if s3 >= 8: recs.append("🏸 壁球/乒乓球 (手部爆發)")
            if s4 >= 8: recs.append("🏃 田徑 (耐力驚人)")
            
            if recs:
                st.success(f"🌟 **運動推薦：**\n" + "\n".join([f"- {r}" for r in recs]))
            else:
                st.info("💡 **發展建議：** 目前各項表現均衡，建議多嘗試不同種類運動以發掘潛能。")
            
            # 給予具體建議
            max_item = categories[scores.index(max(scores))]
            st.info(f"💡 **訓練建議：**\n你表現最出色的是「{max_item}」，建議繼續保持！對於分數較低的項目，可以每天安排 15 分鐘的專項練習。")

        # 4. 數據同步雲端
        try:
            res_df = pd.DataFrame([{
                "時間": hk_time, "姓名": name, "性別": gender, "年齡": age, 
                "總分": total, "BMI": bmi, "仰臥起坐": v1, "體前彎": v2, 
                "手握力": v3, "9分鐘跑": v4
            }])
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, res_df], ignore_index=True)
            conn.update(data=updated_df)
            st.toast("✅ 數據已雲端備份")
        except:
            st.warning("⚠️ 數據未能存檔，請確認 Secrets 設定。")
else:
    st.error("找不到數據庫，請確認檔案路徑。")


