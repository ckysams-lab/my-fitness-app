import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils import load_norms, get_score # 確保你根目錄有 utils.py
from streamlit_gsheets import GSheetsConnection

# --- 已經移除 st.set_page_config，由首頁統一管理 ---

st.title("🚀 智慧評測與 AI 分析")

# 初始化連線與讀取常模
data = load_norms()
conn = st.connection("gsheets", type=GSheetsConnection)

st.info("數據將自動同步至體育組雲端資料庫。")

if data is not None:
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

    # 4. 提交後的處理 (黑金戰報樣式)
    if submitted:
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data) 
        s3 = get_score(v3, gender, age, "grip_strength", data)
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4
        categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘耐力跑']
        scores = [s1, s2, s3, s4]

        # 徽章顏色邏輯
        if total >= 32: 
            rgb, rank_label = "255, 215, 0", "🥇 卓越 (GOLD ELITE)"
        elif total >= 24: 
            rgb, rank_label = "0, 212, 255", "🥈 優良 (SILVER PRO)"
        elif total >= 16: 
            rgb, rank_label = "255, 140, 0", "🥉 尚可 (BRONZE)"
        else: 
            rgb, rank_label = "255, 46, 99", "⚪ 待加強 (CHALLENGER)"

        accent = f"rgb({rgb})"
        
        # 強大嘅動態 CSS 背景樣式
        st.markdown(f"""
            <style>
            .stApp {{ background: radial-gradient(circle, #1A1A2E 0%, #0F0F1B 100%); color: white !important; }}
            .header-box {{ background-color: {accent}; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px; }}
            .badge {{ background: white; color: black !important; padding: 8px 25px; border-radius: 50px; font-weight: bold; border: 2px solid #333; display: inline-block; margin-top: 10px; }}
            .metric-card {{ background: rgba(255,255,255,0.05); border-left: 5px solid {accent}; padding: 15px; border-radius: 10px; }}
            h1, h2, h3, h4, p, span, label, div {{ color: white !important; }}
            .header-box h1 {{ color: black !important; margin: 0; }}
            </style>
        """, unsafe_allow_html=True)

        # 戰報頂部
        st.markdown(f"""
            <div class="header-box">
                <h1>{name} 體能戰報</h1>
                <div class="badge">{rank_label}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 顯示三大核心數據
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card"><h4>總得分</h4><h2 style="color:{accent} !important;">{total} / 40</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div





