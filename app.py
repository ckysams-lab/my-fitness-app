import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. 頁面與連線設定
st.set_page_config(page_title="小學體適能智慧評測系統 v2.0", page_icon="🏃‍♂️", layout="wide")

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
        
        # 動態 CSS 樣式
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
            # 雷達圖分析
            fig = go.Figure(go.Scatterpolar(r=scores + [scores[0]], theta=categories + [categories[0]], fill='toself', line=dict(color=accent), fillcolor=f"rgba({rgb}, 0.3)"))
            fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 10], gridcolor="#444")), paper_bgcolor='rgba(0,0,0,0)', height=450)
            st.plotly_chart(fig, use_container_width=True)
        
        with g2:
            st.markdown("### 📊 各項成就等級")
            st.markdown(f"🪑 仰臥起坐： **{s1}** / 10 分")
            st.markdown(f"🤸 坐姿體前彎： **{s2}** / 10 分")
            st.markdown(f"💪 手握力： **{s3}** / 10 分")
            st.markdown(f"🏃 9分鐘跑： **{s4}** / 10 分")
            
            st.markdown("---")
            st.markdown("### 🤖 AI 智能深度分析")

            # 1. 核心邏輯分析
            advice_list = []
            
            # 仰臥起坐 (核心)
            if s1 >= 8: advice_list.append("🟢 **核心穩定性：** 表現極其優異，這有助於你在任何運動中保持身體平衡。")
            elif s1 >= 4: advice_list.append("🟡 **核心穩定性：** 表現尚可，建議增加每日仰臥起坐次數，提升腹部耐力。")
            else: advice_list.append("🔴 **核心穩定性：** 較為薄弱，這可能會影響你的坐姿與體育活動中的發力，建議從基礎平板支撐練習。")

            # 體前彎 (柔軟度)
            if s2 >= 8: advice_list.append("🟢 **身體柔軟度：** 關節活動度非常好，這能有效減少運動傷害。")
            elif s2 < 4: advice_list.append("🔴 **身體柔軟度：** 肌肉過於緊繃，建議運動後加強拉伸，以免在劇烈運動中拉傷。")

            # 耐力跑 (心肺)
            if s4 >= 8: advice_list.append("🟢 **心肺功能：** 你的心肺耐力是你的最強引擎，非常適合長距離運動。")
            elif s4 < 4: advice_list.append("🔴 **心肺功能：** 體能消耗較快，建議增加慢跑頻率，循序漸進提升心肺效率。")

            # BMI 建議
            if bmi > 24: bmi_advice = "建議注意飲食均衡，並配合更多有氧運動以減輕關節負擔。"
            elif bmi < 18.5: bmi_advice = "體重較輕，建議加強蛋白質攝取並配合阻力訓練增加肌肉量。"
            else: bmi_advice = "體位指標非常標準，請繼續保持良好的生活習慣。"

            # 顯示深度評語
            st.info(f"**【總結評論】**\n\n{name} 同學，{bmi_advice}")
            
            for adv in advice_list:
                st.write(adv)

            st.markdown("---")
            st.markdown("### 🎯 運動專長偵測")
            
            # --- 運動專長分析邏輯 ---
            recommendations = []
            
            # 1. 爆發與核心型 (仰臥起坐得分高)
            if s1 >= 8: recommendations.append("⚽ 足球隊/🏀籃球隊 (需要強大核心與爆發力)")
            
            # 2. 柔軟度型 (體前彎得分高)
            if s2 >= 8: recommendations.append("🧘 中國舞隊 (具備卓越體感潛力)")
            
            # 3. 力量型 (手握力得分高)
            if s3 >= 8: recommendations.append("🏸 壁球隊/🏸 乒乓球隊 (具備優秀上肢穩定與爆發)")
            
            # 4. 耐力型 (9分鐘跑得分高)
            if s4 >= 8: recommendations.append("🏃 田徑隊/⚽ 足球隊 (具備優異心肺耐力)")

            # 綜合判斷：如果總分很高但沒有單項特別突出
            if total >= 30 and not recommendations:
                recommendations.append("🏸 壁球隊/⚽ 足球隊 (全方位素質極佳)")

            # 顯示推薦結果
            if recommendations:
                st.success("🌟 **根據體能數據，你非常適合加入：**")
                for rec in recommendations:
                    st.write(f"- {rec}")
            else:
                st.info("💡 目前體能均衡，建議先從感興趣的運動社團開始嘗試喔！")
            
            st.markdown("---")
            st.markdown("### 🤖 AI 智能助教評語")
            # 保持原本的評語邏輯
            if total >= 32:
                comment = f"震撼！{name} 你具備頂尖運動員的素質。"
            elif total >= 24:
                comment = f"出色！{name} 你的體能表現非常全面。"
            else:
                comment = f"加油 {name}！專注於強項發展，你能做得更好。"
            
            best_item = categories[scores.index(max(scores))]
            st.write(f"📢 {comment}")
            st.write(f"💡 你表現最突出的項目是：**{best_item}**")
        # 雲端資料同步
        try:
            res_df = pd.DataFrame([{"時間": datetime.now().strftime("%Y-%m-%d %H:%M"), "姓名": name, "性別": gender, "年齡": age, "所屬校隊": current_team, "BMI": bmi, "總分": total, "仰臥起坐": v1, "體前彎": v2, "手握力": v3, "9分鐘耐力跑": v4}])
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, res_df], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ 數據已雲端同步。")
        except: 
            st.warning("⚠️ 同步失敗，請確認 Secrets 設定。")

    # --- 老師專屬區塊 (嚴格密碼鎖) ---
    st.write("---")
    with st.expander("📊 老師專屬：全校管理後台"):
        pwd = st.text_input("🔑 請輸入管理員密碼", type="password", key="admin_key")
        
        if pwd == "8888":
            st.success("✅ 歡迎老師登入系統")
            all_db = conn.read(ttl=0)
            
            if not all_db.empty:
                st.subheader("🏆 全校榮譽榜")
                h1, h2 = st.columns(2)
                with h1:
                    st.write("✨ **總分 Top 5**")
                    st.table(all_db.nlargest(5, '總分')[['姓名', '總分', '所屬校隊']])
                with h2:
                    st.write("🔥 **單項最強王者**")
                    try:
                        b1 = all_db.loc[all_db['仰臥起坐'].idxmax()]
                        b2 = all_db.loc[all_db['體前彎'].idxmax()]
                        b3 = all_db.loc[all_db['手握力'].idxmax()]
                        b4 = all_db.loc[all_db['9分鐘耐力跑'].idxmax()]
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            st.info(f"🧱 核心王: {b1['姓名']} ({int(b1['仰臥起坐'])}次)")
                            st.info(f"💪 力量王: {b3['姓名']} ({b3['手握力']}kg)")
                        with c2:
                            st.info(f"🤸 柔軟王: {b2['姓名']} ({int(b2['體前彎'])}cm)")
                            st.info(f"🏃 耐力王: {b4['姓名']} ({int(b4['9分鐘耐力跑'])}m)")
                    except: st.write("數據處理中...")

                st.divider()
                t1, t2, t3 = st.tabs(["潛力新星", "校隊追蹤", "數據解析"])
                with t1:
                    st.write("🔍 非校隊優秀學生：")
                    st.dataframe(all_db[all_db['所屬校隊'] == "無"].nlargest(10, '總分')[['姓名', '總分', 'BMI']], hide_index=True)
                with t2:
                    team = st.selectbox("選擇校隊", ["足球隊", "壁球隊", "乒乓球隊", "籃球隊", "田徑隊", "射箭隊"])
                    st.dataframe(all_db[all_db['所屬校隊'] == team][['姓名', '總分', '時間']], use_container_width=True)
                with t3:
                    st.write("📊 等級分佈")
                    def get_rank_simple(s):
                        if s >= 32: return "🥇 卓越"
                        if s >= 24: return "🥈 優良"
                        return "⚪ 需加強"
                    all_db['等級'] = all_db['總分'].apply(get_rank_simple)
                    st.bar_chart(all_db['等級'].value_counts())
                
                csv = all_db.to_csv(index=False).encode('utf-8-sig')
                st.download_button("💾 下載全校總表 (CSV)", csv, "Fitness_Report.csv", "text/csv")
            else:
                st.info("尚無學生紀錄")
        elif pwd == "":
            st.info("💡 請輸入密碼以解鎖管理功能。")
        else:
            st.error("❌ 密碼錯誤，拒絕訪問。")

else:
    st.error("❌ 找不到數據庫 (norms.json)！")





















