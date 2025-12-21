import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. 頁面與連線設定
st.set_page_config(page_title="小學體適能數位戰報系統 v2.0", page_icon="🏃‍♂️", layout="wide")

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
            if val >= t: 
                return 10 - (i * 2)  # 滿分 10 分
        return 0
    except: return 0

# --- 主介面 ---
st.title("🚀 小學體適能智慧評測系統 - 旗艦專業版")
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
        with col3:
            h = st.number_input("身高 (cm)", 100.0, 180.0, 140.0)
            w = st.number_input("體重 (kg)", 15.0, 90.0, 35.0)

        st.markdown("---")
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        v1 = v_col1.number_input("仰臥起坐 (次)", 0)
        v2 = v_col2.number_input("坐姿體前彎 (cm)", 0)
        v3 = v_col3.number_input("手握力 (kg)", 0.0, 100.0, 10.0)
        v4 = v_col4.number_input("9分鐘耐力跑 (米)", 0)
        
        submitted = st.form_submit_button("🌟 生成個人戰報並啟動 AI 分析")

    # 4. 提交後的處理
    if submitted:
        # A. 計算分數
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data) 
        s3 = get_score(v3, gender, age, "grip_strength", data)
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4
        categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘耐力跑']
        scores = [s1, s2, s3, s4]

        # B. 決定等級主題色
        if total >= 32:
            rgb, rank_label = "255, 215, 0", "🥇 卓越 (GOLD ELITE)"
        elif total >= 24:
            rgb, rank_label = "0, 212, 255", "🥈 優良 (SILVER PRO)"
        elif total >= 16:
            rgb, rank_label = "255, 140, 0", "🥉 尚可 (BRONZE)"
        else:
            rgb, rank_label = "255, 46, 99", "⚪ 待加強 (CHALLENGER)"

        accent = f"rgb({rgb})"
        
        # C. 注入 CSS (深色電競風)
        st.markdown(f"""
            <style>
            .stApp {{ background: radial-gradient(circle, #1A1A2E 0%, #0F0F1B 100%); color: white !important; }}
            .header-box {{ background-color: {accent}; padding: 20px; border-radius: 15px; text-align: center; color: black !important; margin-bottom: 25px; }}
            .metric-card {{ background: rgba(255,255,255,0.05); border-left: 5px solid {accent}; padding: 15px; border-radius: 10px; }}
            h1, h2, h3, h4, p, span, label, div {{ color: white !important; }}
            .header-box h1, .header-box h2 {{ color: black !important; }}
            div[data-testid="stProgress"] > div > div > div > div {{ background-color: {accent} !important; }}
            </style>
        """, unsafe_allow_html=True)

        # D. 個人戰報抬頭
        st.markdown(f'<div class="header-box"><h1>{name} 體能戰報</h1><h2>{rank_label}</h2></div>', unsafe_allow_html=True)
        
        # E. 數據看板
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card"><h4>總得分</h4><h2 style="color:{accent} !important;">{total} / 40</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><h4>BMI 指數</h4><h2 style="color:{accent} !important;">{bmi}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><h4>目前校隊</h4><h2 style="color:{accent} !important;">{current_team}</h2></div>', unsafe_allow_html=True)

        # F. 視覺化：雷達圖與 AI 助教
        st.divider()
        g1, g2 = st.columns([1.2, 1])
        with g1:
            fig = go.Figure(go.Scatterpolar(
                r=scores + [scores[0]], theta=categories + [categories[0]], 
                fill='toself', line=dict(color=accent), fillcolor=f"rgba({rgb}, 0.3)"
            ))
            fig.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 10], gridcolor="#444")),
                paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with g2:
            st.markdown("### 🤖 AI 智能助教評語")
            # AI 邏輯生成
            ai_comment = []
            if total >= 32: ai_comment.append(f"震撼！{name} 你具備頂尖運動員的素質。")
            elif total >= 24: ai_comment.append(f"出色！{name} 你的體能表現非常全面。")
            else: ai_comment.append(f"加油 {name}！專注於強項發展，你能做得更好。")
            
            best_idx = scores.index(max(scores))
            ai_comment.append(f"你的 **{categories[best_idx]}** 表現最為突出，這是你的天賦所在。")
            
            if bmi > 24: ai_comment.append("注意：增加有氧運動可減輕關節負擔。")
            elif bmi < 18.5: ai_comment.append("提醒：多攝取營養並強化力量訓練。")
            
            st.info("\n\n".join(ai_comment))

            # 天賦稱號
            titles = []
            if s1 == 10: titles.append("🧱 核心守護者")
            if s2 == 10: titles.append("🤸 柔軟大師")
            if s3 == 10: titles.append("💪 校園力王")
            if s4 == 10: titles.append("🔥 無盡引擎")
            if titles:
                st.write("✨ **解鎖稱號：**")
                title_html = "".join([f'<span style="background-color:gold; color:black; padding:4px 10px; border-radius:15px; margin-right:5px; font-weight:bold;">{t}</span>' for t in titles])
                st.markdown(title_html, unsafe_allow_html=True)

        # G



























