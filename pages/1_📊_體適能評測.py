import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils import load_norms, get_score 
from streamlit_gsheets import GSheetsConnection

# 1. 頁面設定
st.set_page_config(page_title="正覺蓮社學校 - 體適能評測", layout="wide", page_icon="🚀")

# 2. 側邊欄與 CSS 優化
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] { background-color: #1A1A2E; }
        [data-testid="stSidebar"] a { font-size: 18px !important; color: #FFFFFF !important; }
        .stApp { background: #0F0F1B; color: white; }
        .header-box { background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%); padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
        .metric-card { background: rgba(255,255,255,0.05); border-left: 5px solid var(--accent); padding: 15px; border-radius: 10px; }
        h1, h2, h3, h4 { font-family: 'Microsoft JhengHei', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# 初始化 Google Sheets 連線
conn = st.connection("gsheets", type=GSheetsConnection)

with st.sidebar:
    st.markdown("### 🏫 正覺蓮社學校\n### 🏃 體育組管理系統")
    st.divider()
    st.page_link("🏠_首頁.py", label="系統首頁", icon="🏠")
    st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")

st.title("🚀 智慧評測與 AI 分析系統")

# 載入常模數據
data = load_norms()

with st.form("input_form"):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        gender = st.radio("性別", ["男", "女"], horizontal=True)
        age = st.number_input("年齡", 5, 13, 10)
    with col2:
        name = st.text_input("學生姓名/編號", placeholder="輸入姓名")
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
    
    submitted = st.form_submit_button("🌟 生成個人戰報並儲存數據")

if submitted:
    if not name:
        st.error("請輸入學生姓名後再提交！")
    else:
        # 計算分數
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data) 
        s3 = get_score(v3, gender, age, "grip_strength", data)
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4
        
        # 評級邏輯
        if total >= 32: rgb, rank = "255, 215, 0", "🥇 卓越 (GOLD)"
        elif total >= 24: rgb, rank = "0, 212, 255", "🥈 優良 (SILVER)"
        elif total >= 16: rgb, rank = "255, 140, 0", "🥉 尚可 (BRONZE)"
        else: rgb, rank = "255, 46, 99", "⚪ 待加強 (CHALLENGER)"
        accent = f"rgb({rgb})"

        # --- 數據儲存邏輯 ---
        new_data = pd.DataFrame([{
            "日期": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "姓名": name, "性別": gender, "年齡": age, "BMI": bmi,
            "仰臥起坐": v1, "坐姿體前彎": v2, "手握力": v3, "9分鐘跑": v4,
            "總分": total, "等級": rank
        }])
        
        try:
            # 讀取現有數據並合併（假設你 Sheets URL 已在 secrets 設定好）
            existing_data = conn.read(worksheet="Sheet1")
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.toast("✅ 數據已成功同步至雲端數據庫", icon='☁️')
        except Exception as e:
            st.warning("數據儲存失敗（請檢查 Google Sheets Secrets 設定），僅顯示本地分析。")

        # --- UI 渲染 ---
        st.markdown(f"""
            <div class="header-box">
                <h1 style="color:white !important; margin:0;">{name} 體能戰報</h1>
                <h2 style="color:{accent} !important; margin:0;">{rank}</h2>
            </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card" style="--accent:{accent}"><h4>總得分</h4><h2>{total} <small>/ 40</small></h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card" style="--accent:{accent}"><h4>BMI 指數</h4><h2>{bmi}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card" style="--accent:{accent}"><h4>目前校隊</h4><h2>{current_team}</h2></div>', unsafe_allow_html=True)

        st.divider()
        
        g1, g2 = st.columns([1.2, 1])
        with g1:
            categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘跑']
            scores = [s1, s2, s3, s4]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]],
                theta=categories + [categories[0]],
                fill='toself',
                line_color=accent,
                fillcolor=f"rgba({rgb}, 0.3)"
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 10], gridcolor="gray"),
                    angularaxis=dict(gridcolor="gray")
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white", size=14)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with g2:
            st.markdown("### 🤖 AI 智能深度分析")
            analysis_box = st.container(border=True)
            with analysis_box:
                if s1 < 4: st.write("🔴 **核心力量：** 仰臥起坐得分偏低，建議加強捲腹練習。")
                if s4 >= 8: st.write("🟢 **耐力表現：** 9分鐘跑表現極佳，具備長跑運動員潛質。")
                if bmi > 24: st.write("⚠️ **健康體重：** BMI 偏高，建議增加有氧運動並注意飲食調節。")
                
                st.markdown("---")
                st.markdown("#### 🎯 建議發展方向")
                recs = []
                if s1 >= 7 and s4 >= 7: recs.append("⚽ 足球隊")
                if s2 >= 8: recs.append("🤸 體操小組")
                if s3 >= 7: recs.append("🏸 乒乓球/羽毛球")
                
                if recs:
                    st.success(f"推薦參加：{', '.join(recs)}")
                else:
                    st.info("💡 建議先參加「全能體適能班」提升基礎素質。")

        st.balloons()




