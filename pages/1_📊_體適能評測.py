import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils import load_norms, get_score 
from streamlit_gsheets import GSheetsConnection

# 1. 頁面設定
st.set_page_config(page_title="體適能評測系統", layout="wide")

# 2. 側邊欄與 CSS
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] a { font-size: 22px !important; margin-bottom: 10px; }
        [data-testid="stSidebar"] h3 { font-size: 28px !important; color: #FFD700; text-align: center; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 正覺蓮社學校\n### 體育組")
    st.divider()
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")

st.title("🚀 智慧評測與 AI 分析")

data = load_norms()

with st.form("input_form"):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        gender = st.radio("性別", ["男", "女"], horizontal=True)
        age = st.number_input("年齡", 5, 13, 10)
    with col2:
        name = st.text_input("學生姓名/編號", "學生A")
        current_team = st.selectbox("目前校隊", ["無", "足球隊", "壁球隊", "乒乓球隊", "籃球隊", "田徑隊", "射箭隊"])
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

if submitted:
    bmi = round(w / ((h/100)**2), 1)
    s1 = get_score(v1, gender, age, "sit_ups", data)
    s2 = get_score(v2, gender, age, "sit_reach", data) 
    s3 = get_score(v3, gender, age, "grip_strength", data)
    s4 = get_score(v4, gender, age, "run_9min", data)
    total = s1 + s2 + s3 + s4
    categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘跑']
    scores = [s1, s2, s3, s4]

    # 色彩邏輯
    if total >= 32: rgb, rank = "255, 215, 0", "🥇 卓越 (GOLD)"
    elif total >= 24: rgb, rank = "0, 212, 255", "🥈 優良 (SILVER)"
    elif total >= 16: rgb, rank = "255, 140, 0", "🥉 尚可 (BRONZE)"
    else: rgb, rank = "255, 46, 99", "⚪ 待加強 (CHALLENGER)"
    accent = f"rgb({rgb})"

    st.markdown(f"""
        <style>
        .stApp {{ background: #0F0F1B; color: white !important; }}
        .header-box {{ background-color: {accent}; padding: 20px; border-radius: 15px; text-align: center; color: black !important; }}
        .metric-card {{ background: rgba(255,255,255,0.05); border-left: 5px solid {accent}; padding: 15px; border-radius: 10px; margin-top: 10px; }}
        h1, h2, h3, h4, p, span {{ color: white !important; }}
        .header-box h1 {{ color: black !important; }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="header-box"><h1>{name} 體能戰報</h1><h3>{rank}</h3></div>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    m1.markdown(f'<div class="metric-card"><h4>總得分</h4><h2 style="color:{accent} !important;">{total} / 40</h2></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><h4>BMI 指數</h4><h2 style="color:{accent} !important;">{bmi}</h2></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><h4>目前校隊</h4><h2 style="color:{accent} !important;">{current_team}</h2></div>', unsafe_allow_html=True)

    st.divider()
    
    g1, g2 = st.columns([1.2, 1])
    with g1:
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=scores+[scores[0]], theta=categories+[categories[0]], fill='toself', line_color=accent, fillcolor=f"rgba({rgb}, 0.3)"))
        fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 10])), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with g2:
        st.markdown("### 🤖 AI 智能深度分析")
        if s1 < 4: st.write("🔴 **核心力量：** 仰臥起坐表現較弱，建議每天練習。")
        if s4 >= 8: st.write("🟢 **耐力表現：** 具備強大的肺活量潛質。")
        
        st.markdown("---")
        st.markdown("### 🎯 運動專長推薦")
        recs = []
        if s1 >= 7: recs.append("⚽ 足球隊 / 🏀 籃球隊")
        if s2 >= 7: recs.append("🤸 體操 / 🧘 瑜伽組")
        if s3 >= 7: recs.append("🏸 壁球 / 乒乓球")
        if s4 >= 7: recs.append("🏃 田徑隊")
        
        if recs:
            for r in recs: st.success(f"🌟 適合加入：{r}")
        else:
            st.info("💡 暫未偵測到突出項目，建議先參加「體適能興趣小組」打好基礎。")
    
    st.balloons()




