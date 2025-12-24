import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

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
    # 此處保留您原本的 Plotly 雷達圖邏輯...









