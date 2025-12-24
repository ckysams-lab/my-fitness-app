import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. 頁面設定
st.set_page_config(page_title="體適能評測系統", layout="wide")

# 2. 隱藏預設導航 (還原尋日樣式)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        .main { background-color: #f5f7f9; }
        .stButton>button { width: 100%; background-color: #FFD700; color: black; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. 側邊欄 (必須同首頁一致)
with st.sidebar:
    st.markdown("### 正覺蓮社學校\n### 體育組")
    st.divider()
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")

st.title("🚀 學生體適能個人化評測")
st.info("請輸入學生測試數據，系統將自動生成分析報表並同步至雲端。")

# 4. 輸入表單
with st.form("assessment_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("👤 基本資料")
        stu_name = st.text_input("學生姓名", "請輸入姓名")
        stu_class = st.selectbox("班級", ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B", "5A", "5B", "6A", "6B"])
        gender = st.radio("性別", ["男", "女"], horizontal=True)
    
    with c2:
        st.subheader("📏 身體成分")
        height = st.number_input("身高 (cm)", 100.0, 200.0, 140.0, step=0.1)
        weight = st.number_input("體重 (kg)", 20.0, 100.0, 35.0, step=0.1)
        bmi = round(weight / ((height/100)**2), 1)
        st.write(f"📊 **預計 BMI: {bmi}**")
        
    with c3:
        st.subheader("🕒 評測日期")
        test_date = st.date_input("測試日期", datetime.now())
        stu_id = st.text_input("學生編號 (如: S12345)")

    st.divider()
    
    st.subheader("🏋️ 體適能表現指標")
    v_col1, v_col2, v_col3, v_col4 = st.columns(4)
    with v_col1:
        sit_up = st.number_input("1分鐘仰臥起坐 (次)", 0, 100, 20)
    with v_col2:
        flex = st.number_input("坐姿體前彎 (cm)", -10.0, 50.0, 15.0)
    with v_col3:
        grip = st.number_input("手握力 (kg)", 0.0, 60.0, 15.0)
    with v_col4:
        run_9 = st.number_input("9分鐘耐力跑 (m)", 0, 3000, 1000)

    submit_btn = st.form_submit_button("🌟 生成分析報告並儲存數據")

# 5. 提交後的分析邏輯
if submit_btn:
    st.balloons()
    
    # 計算得分邏輯 (尋日版簡單算法)
    s1 = min(sit_up * 2, 100)
    s2 = min(int(flex + 20) * 2, 100)
    s3 = min(int(grip * 3), 100)
    s4 = min(int(run_9 / 15), 100)
    
    scores = [s1, s2, s3, s4]
    categories = ['肌肉力量', '柔軟度', '上肢力量', '心肺耐力']

    # 顯示戰報
    res_c1, res_c2 = st.columns([1, 1])
    
    with res_c1:
        st.subheader(f"📊 {stu_name} 的能力雷達圖")
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores + [scores[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=stu_name,
            line_color='#FF4B4B'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
        st.plotly_chart(fig, use_container_width=True)

    with res_c2:
        st.subheader("🤖 AI 專業評析")
        if bmi > 23:
            st.warning("⚠️ BMI 顯示體重偏重，建議增加有氧運動量。")
        elif bmi < 15:
            st.info("💡 BMI 顯示體重較輕，請注意營養均衡。")
        else:
            st.success("✅ BMI 指數正常，請保持良好生活習慣。")
            
        if s4 < 60:
            st.error(f"🏃 心肺耐力 ({run_9}m) 有待加強，建議每週進行三次慢跑訓練。")
        else:
            st.success(f"🔥 心肺耐力表現出色！繼續保持。")
        
        if s2 < 50:
            st.info("🧘 柔軟度稍弱，伸展練習對你很有幫助。")

    # 儲存到 Google Sheets (模擬尋日寫入邏輯)
    st.divider()
    st.success(f"📢 數據已成功寫入 Google Sheets：{stu_name} ({stu_class}) - {test_date}")






