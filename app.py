import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. 頁面與連線設定
st.set_page_config(page_title="小學體適能數位戰報系統", page_icon="🏃‍♂️", layout="wide")

# 建立雲端連線
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"連線設定錯誤: {e}")

# 2. 定義功能函數 (10 分制)
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
st.title("🚀 小學體適能智慧評測系統")
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
        
        submitted = st.form_submit_button("🌟 生成 40 分制個人戰報並同步雲端")

    # 4. 提交後的處理
    if submitted:
        # A. 計算分數
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data) 
        s3 = get_score(v3, gender, age, "grip_strength", data)
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4

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
            h1, h2, h3, h4, p, span, label {{ color: white !important; }}
            div[data-testid="stProgress"] > div > div > div > div {{ background-color: {accent} !important; }}
            </style>
        """, unsafe_allow_html=True)

        # D. 個人戰報抬頭
        st.markdown(f'<div class="header-box"><h1 style="color:black !important; margin:0;">{name} 體能戰報</h1><h2 style="color:black !important; margin:0;">{rank_label}</h2></div>', unsafe_allow_html=True)
        
        # --- 勳章顯示 (10 分滿分) ---
        badges = []
        if s1 == 10: badges.append("🧱 鋼鐵核心")
        if s2 == 10: badges.append("🤸 柔軟大師")
        if s3 == 10: badges.append("⚡ 神力超人")
        if s4 == 10: badges.append("🔥 耐力之王")
        if badges:
            b_cols = st.columns(len(badges))
            for i, b in enumerate(badges): b_cols[i].success(f"🏅 {b}")

        # E. 數據看板
        st.write("")
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card"><h4>總得分</h4><h2 style="color:{accent} !important;">{total} / 40</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><h4>BMI 指數</h4><h2 style="color:{accent} !important;">{bmi}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><h4>所屬隊伍</h4><h2 style="color:{accent} !important;">{current_team}</h2></div>', unsafe_allow_html=True)

        # F. 體能數據視覺化 (雷達圖)
        st.divider()
        g1, g2 = st.columns([1.5, 1])
        with g1:
            st.markdown("### 🕸️ 體能均衡度分析 (40分制)")
            categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘耐力跑']
            scores = [s1, s2, s3, s4]
            fig = go.Figure(go.Scatterpolar(
                r=scores + [scores[0]], theta=categories + [categories[0]], 
                fill='toself', line=dict(color=accent), fillcolor=f"rgba({rgb}, 0.3)"
            ))
            fig.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 10], gridcolor="#444")),
                paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        with g2:
            st.markdown("### 📊 單項明細")
            for label, score in zip(categories, scores):
                st.write(f"**{label}** ({score}/10)")
                st.progress(score / 10)

        # G. 運動處方 (修正為多項併列顯示)
        st.divider()
        st.subheader("🎯 專屬運動處方與社團推薦")
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.write("🏆 **基於你的優勢推薦：**")
            # 檢查每一項是否優異，優異者皆顯示推薦
            has_rec = False
            if s1 >= 8: 
                st.success("🏀 **推薦：籃球隊 / 體操隊** (核心穩定性極佳)")
                has_rec = True
            if s2 >= 8: 
                st.success("🧘 **推薦：舞蹈隊 / 瑜珈社** (柔軟度表現卓越)")
                has_rec = True
            if s3 >= 8: 
                st.success("🎾 **推薦：壁球 / 乒乓球 / 羽球** (上肢爆發力強)")
                has_rec = True
            if s4 >= 8: 
                st.success("⚽ **推薦：足球隊 / 田徑隊** (心肺耐力非常優秀)")
                has_rec = True
            
            if not has_rec:
                st.info("🏃 **建議：** 目前各項均衡發展，建議多嘗試不同社團找出興趣！")
                
        with rec_col2:
            st.write("🛠️ **基於你的短板建議：**")
            # 檢查每一項是否需要加強
            if s1 <= 4: st.warning("🧱 **核心加強：** 每天練習 30 秒棒式或捲腹。")
            if s2 <= 4: st.warning("🧘 **伸展加強：** 每天睡前進行 5 分鐘坐姿體前彎。")
            if s3 <= 4: st.warning("💪 **力量加強：** 練習吊單槓或使用握力器訓練。")
            if s4 <= 4: st.warning("🏃 **耐力加強：** 每週進行兩次 10 分鐘慢跑。")

        # H. 雲端同步
        try:
            res_df = pd.DataFrame([{
                "時間": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "姓名": name, "性別": gender, "年齡": age, "所屬校隊": current_team,
                "BMI": bmi, "總分": total, "仰臥起坐": v1, "體前彎": v2, "手握力": v3, "9分鐘耐力跑": v4
            }])
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, res_df], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ 數據已成功存入雲端！")
        except:
            st.warning("⚠️ 雲端連線異常，請下載報告保存。")

        st.download_button("📥 下載本次 CSV 戰報", res_df.to_csv(index=False).encode('utf-8-sig'), f"{name}_report.csv")

        # I. 老師大盤分析 & 英雄榜
        st.write("")
        with st.expander("📊 老師專屬：全校大盤分析與英雄榜"):
            all_db = conn.read(ttl=0)
            if not all_db.empty:
                # 1. 英雄榜
                st.subheader("🏆 體能英雄榜 (Top 5)")
                h1, h2 = st.columns(2)
                with h1:
                    st.write("✨ **總分榮譽榜**")
                    st.table(all_db.nlargest(5, '總分')[['姓名', '總分', '所屬校隊']])
                with h2:
                    st.write("🔥 **單項最強王者**")
                    # 找出四個單項的最高分紀錄
                    # idxmax() 會回傳該列最大值所在的索引位置
                    best_situp = all_db.loc[all_db['仰臥起坐'].idxmax()]
                    best_reach = all_db.loc[all_db['體前彎'].idxmax()]
                    best_grip = all_db.loc[all_db['手握力'].idxmax()]
                    best_run = all_db.loc[all_db['9分鐘耐力跑'].idxmax()]
                    
                    # 使用不同顏色的 success/warning/info/error 框來區分榮譽
                    st.success(f"🧱 核心王：{best_situp['姓名']} ({int(best_situp['仰臥起坐'])}次)")
                    st.warning(f"🤸 柔軟王：{best_reach['姓名']} ({int(best_reach['體前彎'])}cm)")
                    st.info(f"💪 力量王：{best_grip['姓名']} ({best_grip['手握力']}kg)")
                    st.error(f"🏃 耐力王：{best_run['姓名']} ({int(best_run['9分鐘耐力跑'])}m)")
                
                # 2. 校隊平均分柱狀圖
                st.divider()
                st.write("🏃 **校隊平均總分對比**")
                st.bar_chart(all_db.groupby("所屬校隊")["總分"].mean())
else:
    st.error("❌ 找不到數據庫 (norms.json)！")



























