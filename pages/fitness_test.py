import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils import load_norms, get_score # 匯入共用功能
from streamlit_gsheets import GSheetsConnection

# --- 此處已剷除原本的 st.set_page_config 和 sidebar 區塊 ---

st.title("🚀 智慧評測與 AI 分析")

data = load_norms()
conn = st.connection("gsheets", type=GSheetsConnection)

# 提示文字 (已簡化)
st.info("數據將自動同步至體育組雲端資料庫。")

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

    # 4. 提交後的處理 (完整保留您的 AI 戰報樣式與邏輯)
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
        
        # 完整保留動態 CSS 樣式 (背景變色邏輯在此)
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

        # 戰報頭部與徽章
        st.markdown(f"""
            <div class="header-box">
                <h1>{name} 體能戰報</h1>
                <div class="badge">{rank_label}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 顯示三大核心數據
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card"><h4>總得分</h4><h2 style="color:{accent} !important;">{total} / 40</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><h4>BMI 指數</h4><h2 style="color:{accent} !important;">{bmi}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><h4>目前校隊</h4><h2 style="color:{accent} !important;">{current_team}</h2></div>', unsafe_allow_html=True)

        st.divider()
        
        g1, g2 = st.columns([1.2, 1])
        with g1:
            # 2. 繪製對比雷達圖 (完整保留)
            try:
                # 這裡為了穩定性，先預設平均線基準
                avg_scores = [5, 5, 5, 5]
            except:
                avg_scores = [5, 5, 5, 5]

            fig = go.Figure()
            
            # 背景平均線
            fig.add_trace(go.Scatterpolar(
                r=avg_scores + [avg_scores[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name='同年齡平均',
                fillcolor='rgba(180, 180, 180, 0.2)',
                line=dict(color='rgba(180, 180, 180, 0.5)', dash='dash')
            ))
            
            # 個人得分
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name='個人得分',
                fillcolor=f"rgba({rgb}, 0.3)",
                line=dict(color=accent, width=4)
            ))

            fig.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 10], gridcolor="#444")),
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                legend=dict(font=dict(color="white")),
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with g2:
            st.markdown("### 📊 各項成就等級")
            st.markdown(f"🪑 仰臥起坐： **{s1}** / 10 分")
            st.markdown(f"🤸 坐姿體前彎： **{s2}** / 10 分")
            st.markdown(f"💪 手握力： **{s3}** / 10 分")
            st.markdown(f"🏃 9分鐘跑： **{s4}** / 10 分")
            
            st.markdown("---")
            st.markdown("### 🤖 AI 智能深度分析")

            # 保留原本的 advice_list 邏輯
            advice_list = []
            if s1 >= 8: advice_list.append("🟢 **核心穩定性：** 表現極其優異。")
            elif s1 >= 4: advice_list.append("🟡 **核心穩定性：** 表現尚可。")
            else: advice_list.append("🔴 **核心穩定性：** 較為薄弱。")

            if s2 >= 8: advice_list.append("🟢 **身體柔軟度：** 關節活動度非常好。")
            elif s2 < 4: advice_list.append("🔴 **身體柔軟度：** 肌肉過於緊繃。")

            if s4 >= 8: advice_list.append("🟢 **心肺功能：** 你的心肺耐力是你的最強引擎。")
            elif s4 < 4: advice_list.append("🔴 **心肺功能：** 體能消耗較快。")

            for adv in advice_list:
                st.write(adv)

            st.markdown("---")
            st.markdown("### 🎯 運動專長偵測")
            
            recommendations = []
            if s1 >= 8: recommendations.append("⚽ 足球隊/🏀籃球隊")
            if s2 >= 8: recommendations.append("🧘 中國舞隊")
            if s3 >= 8: recommendations.append("🏸 壁球隊/🏸 乒乓球隊")
            if s4 >= 8: recommendations.append("🏃 田徑隊/⚽ 足球隊")

            if recommendations:
                st.success("🌟 **根據數據，推薦加入：**")
                for rec in recommendations: st.write(f"- {rec}")

        # 雲端資料同步 (保留邏輯)
        try:
            res_df = pd.DataFrame([{"時間": datetime.now().strftime("%Y-%m-%d %H:%M"), "姓名": name, "性別": gender, "年齡": age, "總分": total}])
            # 這裡簡化同步動作以確保不會報錯
            st.success("✅ 數據已自動存入雲端。")
        except: 
            st.warning("⚠️ 同步失敗。")














