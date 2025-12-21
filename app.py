import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# 1. 頁面與連線設定
st.set_page_config(page_title="體適能評測系統", page_icon="🏃‍♂️", layout="wide")

# 建立雲端連線
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"連線設定錯誤: {e}")

# 2. 定義功能函數
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
            if val >= t: return 5 - i
        return 0
    except: return 0

# --- 主介面 ---
st.title("🏃‍♂️ 小學體適能評測系統")
data = load_data()

if data:
    # 3. 建立表單
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        gender = col1.radio("性別", ["男", "女"], horizontal=True)
        age = col2.number_input("年齡", 5, 13, 10)
        name = st.text_input("學生姓名/編號", "學生A")        
        current_team = st.selectbox(
            "目前所屬校隊", 
            ["無", "足球隊", "壁球隊", "乒乓球隊", "籃球隊", "田徑隊", "射箭隊"]
        )
        
        st.subheader("測量數值")
        h = st.number_input("身高 (cm)", 100.0, 180.0, 140.0)
        w = st.number_input("體重 (kg)", 15.0, 90.0, 35.0)
        v1 = st.number_input("仰臥起坐 (次)", 0)
        v2 = st.number_input("坐姿體前彎 (cm)", 0)
        v3 = st.number_input("手握力 (kg)", 0.0, 50.0, 15.0)
        v4 = st.number_input("9分鐘耐力跑 (米)", 0)
        
        submitted = st.form_submit_button("🌟 計算總成績並同步雲端")

    # 4. 提交後的處理
    if submitted:
        # A. 計算分數
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data)
        s3 = get_score(v3, gender, age, "grip_strength", data) 
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4

        # B. 根據分數決定鮮豔的主題色 (R, G, B)
        if total >= 15:
            rgb = "255, 215, 0"  # 鮮豔金
            rank_label = "🥇 卓越 (GOLD ELITE)"
        elif total >= 10:
            rgb = "0, 212, 255"  # 科技藍
            rank_label = "🥈 優良 (SILVER PRO)"
        elif total >= 8:
            rgb = "255, 140, 0"  # 活力橘
            rank_label = "🥉 尚可 (BRONZE)"
        else:
            rgb = "255, 46, 99"  # 極限紅
            rank_label = "⚪ 待加強 (CHALLENGER)"

        accent = f"rgb({rgb})"
        fill = f"rgba({rgb}, 0.3)"

        # C. 注入動態 CSS：讓介面變鮮豔
        st.markdown(f"""
            <style>
            .stApp {{ background: radial-gradient(circle, #1A1A2E 0%, #0F0F1B 100%); color: white !important; }}
            /* 霓虹標題卡片 */
            .header-box {{
                background-color: {accent};
                padding: 20px; border-radius: 15px; text-align: center;
                box-shadow: 0 0 20px {accent}; margin-bottom: 25px;
            }}
            /* 數據卡片 */
            .metric-card {{
                background: rgba(255,255,255,0.05); border-left: 5px solid {accent};
                padding: 15px; border-radius: 10px;
            }}
            /* 強制修改進度條顏色 */
            div[data-testid="stProgress"] > div > div > div > div {{ background-color: {accent} !important; }}
            h1, h2, h3, p, span {{ color: white !important; }}
            </style>
        """, unsafe_allow_html=True)

        # D. 顯示戰報抬頭
        st.markdown(f'<div class="header-box"><h1 style="color:black !important; margin:0;">{name} 體能戰報</h1><h2 style="color:black !important; margin:0;">{rank_label}</h2></div>', unsafe_allow_html=True)

        # E. 三大指標
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1: st.markdown(f'<div class="metric-card"><h4>總得分</h4><h2 style="color:{accent} !important;">{total} / 20</h2></div>', unsafe_allow_html=True)
        with col_m2: st.markdown(f'<div class="metric-card"><h4>BMI 狀態</h4><h2 style="color:{accent} !important;">{bmi}</h2></div>', unsafe_allow_html=True)
        with col_m3: st.markdown(f'<div class="metric-card"><h4>評測等級</h4><h2 style="color:{accent} !important;">{rank_name if "rank_name" in locals() else rank_label.split(" ")[1]}</h2></div>', unsafe_allow_html=True)

        # F. 雷達圖與進度條
        st.divider()
        g1, g2 = st.columns([1, 1])
        with g1:
            st.subheader("🕸️ 均衡度分析")
            categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘耐力跑']
            scores = [s1, s2, s3, s4]
            fig = go.Figure(go.Scatterpolar(
                r=scores + [scores[0]], theta=categories + [categories[0]], 
                fill='toself', line=dict(color=accent), fillcolor=fill
            ))
            fig.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 5], gridcolor="#444")),
                paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=350, margin=dict(l=40, r=40, t=30, b=30)
            )
            st.plotly_chart(fig, use_container_width=True)

        with g2:
            st.subheader("⚡ 分項強弱")
            for label, score in zip(categories, scores):
                st.write(f"**{label}** : {score}/5")
                st.progress(score / 5)

        # --- G. 智能運動建議與處方 ---
        st.divider()
        st.subheader("📋 專屬運動處方 (Exercise Prescription)")
        
        # 建立建議容器
        advice_list = []

        # 1. 仰臥起坐 (核心肌群)
        if s1 >= 4:
            advice_list.append("✅ **核心強大：** 你的腹肌耐力優異，這有助於你在所有運動中保持穩定。")
        elif s1 <= 2:
            advice_list.append("📍 **核心訓練：** 建議加強腹部力量，每天嘗試 3 組 30 秒的「棒式 (Plank)」。")

        # 2. 坐姿體前彎 (柔軟度)
        if s2 >= 4:
            advice_list.append("✅ **柔軟大師：** 你的關節活動度很好，運動時較不容易受傷。")
        elif s2 <= 2:
            advice_list.append("📍 **柔韌伸展：** 建議每天睡前進行 5 分鐘坐姿體前彎拉伸，每次停留 15 秒，不要憋氣。")

        # 3. 手握力 (上肢爆發力)
        if s3 >= 4:
            advice_list.append("✅ **力量驚人：** 你的抓握力強，在壁球或乒乓球的控球上很有優勢。")
        elif s3 <= 2:
            advice_list.append("📍 **抓握練習：** 可以練習擠壓網球或使用握力器，提升上肢的抓握穩定性。")

        # 4. 耐力跑 (心肺耐力)
        if s4 >= 4:
            advice_list.append("✅ **耐力小超人：** 你的心肺能力極佳，具備成為長跑或足球選手的潛力。")
        elif s4 <= 2:
            advice_list.append("📍 **心肺強化：** 建議每週進行 3 次 15 分鐘的慢跑，或在公園進行往返快走。")

        # 顯示建議
        if advice_list:
            for advice in advice_list:
                # 根據強弱項顯示不同顏色
                if "✅" in advice:
                    st.success(advice)
                else:
                    st.info(advice)
        
        # --- 自動同步與下載邏輯 (保持不變) ---

        try:
            res_df = pd.DataFrame([{
                "時間": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                "姓名": name, "性別": gender, "年齡": age,
                "所屬校隊": current_team,
                "BMI": bmi, "總分": total,
                "仰臥起坐": v1, "體前彎": v2, "手握力": v3, "9分鐘耐力跑": v4
            }])
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, res_df], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ 數據已自動存入雲端試算表！")
        except Exception as e:
            st.warning(f"⚠️ 雲端同步失敗（但本地計算成功）：{e}")

        # 下載按鈕
        csv = res_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載本次報告", csv, f"{name}.csv", "text/csv")

else:
    st.error("❌ 找不到數據庫！請確保 norms.json 存在。")















