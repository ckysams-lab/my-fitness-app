import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 注意：子頁面不需要 st.set_page_config，首頁有寫就可以了

st.title("🚀 智慧評測與 AI 分析")

# 連結 Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1012dxtCcrg3KEvoaVEhIsiJRr3GTmx9wYEVPfHQvQXw/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("input_form"):
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

    st.markdown("---")
    v1 = st.number_input("仰臥起坐 (次)", 0)
    v2 = st.number_input("坐姿體前彎 (cm)", 0)
    v3 = st.number_input("手握力 (kg)", 0.0)
    v4 = st.number_input("9分鐘耐力跑 (米)", 0)
    
    submitted = st.form_submit_button("🌟 生成個人戰報並啟動 AI 分析")

if submitted:
    st.success(f"✅ {name} 的數據分析已完成！")
    
    # --- 1. 還原 Plotly 雷達圖邏輯 ---
    categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘跑']
    # 這裡假設一個簡單的評分邏輯 (例如 0-100 分)，你可以根據實際常模調整
    values = [min(v1*2, 100), min(v2*2, 100), min(v3*3, 100), min(v4/20, 100)] 
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=name,
        line_color='#FFD700'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title=f"{name} 的體能雷達圖"
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- 2. 還原 AI 評語邏輯 ---
    st.subheader("🤖 AI 戰術分析")
    if v4 < 1000:
        st.warning("💪 耐力表現有提升空間，建議加強有氧訓練。")
    else:
        st.success("🔥 耐力優秀！適合擔任校隊長距離項目。")
        
    st.info(f"💡 建議：針對「{categories[values.index(min(values))]}」進行專項強化。")









