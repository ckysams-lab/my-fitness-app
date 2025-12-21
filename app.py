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

        # 顏色邏輯
        if total >= 32: rgb, rank_label = "255, 215, 0", "🥇 卓越 (GOLD ELITE)"
        elif total >= 24: rgb, rank_label = "0, 212, 255", "🥈 優良 (SILVER PRO)"
        elif total >= 16: rgb, rank_label = "255, 140, 0", "🥉 尚可 (BRONZE)"
        else: rgb, rank_label = "255, 46, 99", "⚪ 待加強 (CHALLENGER)"

        accent = f"rgb({rgb})"
        st.markdown(f"<style>.stApp {{ background: radial-gradient(circle, #1A1A2E 0%, #0F0F1B 100%); color: white !important; }} .header-box {{ background-color: {accent}; padding: 20px; border-radius: 15px; text-align: center; color: black !important; margin-bottom: 25px; }} .metric-card {{ background: rgba(255,255,255,0.05); border-left: 5px solid {accent}; padding: 15px; border-radius: 10px; }} h1, h2, h3, h4, p, span, label, div {{ color: white !important; }} .header-box h1, .header-box h2 {{ color: black !important; }}</style>", unsafe_allow_html=True)

        st.markdown(f'<div class="header-box"><h1>{name} 體能戰報</h1><h2>{rank_label}</h2></div>', unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card"><h4>總得分</h4><h2 style="color:{accent} !important;">{total} / 40</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><h4>BMI 指數</h4><h2 style="color:{accent} !important;">{bmi}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><h4>目前校隊</h4><h2 style="color:{accent} !important;">{current_team}</h2></div>', unsafe_allow_html=True)

        st.divider()
        g1, g2 = st.columns([1.2, 1])
        with g1:
            fig = go.Figure(go.Scatterpolar(r=scores + [scores[0]], theta=categories + [categories[0]], fill='toself', line=dict(color=accent), fillcolor=f"rgba({rgb}, 0.3)"))
            fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 10], gridcolor="#444")), paper_bgcolor='rgba(0,0,0,0)', height=450)
            st.plotly_chart(fig, use_container_width=True)
        
        with g2:
            st.markdown("### 🤖 AI 智能助教評語")
            ai_comment = [f"震撼！{name} 你具備頂尖素質。" if total >= 32 else f"加油 {name}！持續努力。"]
            ai_comment.append(f"你的 **{categories[scores.index(max(scores))]}** 表現最突顯。")
            st.info("\n\n".join(ai_comment))

        # 雲端同步
        try:
            res_df = pd.DataFrame([{"時間": datetime.now().strftime("%Y-%m-%d %H:%M"), "姓名": name, "性別": gender, "年齡": age, "所屬校隊": current_team, "BMI": bmi, "總分": total, "仰臥起坐": v1, "體前彎": v2, "手握力": v3, "9分鐘耐力跑": v4}])
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, res_df], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ 數據已同步。")
        except: st.warning("⚠️ 同步失敗。")

    # --- I. 老師大盤分析 (解決彈走問題) ---
    st.write("---")
    with st.expander("📊 老師專屬：全校管理後台"):
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
                    st.write(f"🧱 核心王：{all_db.loc[all_db['仰臥起坐'].idxmax()]['姓名']}")
                    st.write(f"🏃 耐力王：{all_db.loc[all_db['9分鐘耐力跑'].idxmax()]['姓名']}")
                except: st.write("計算中...")

            st.divider()
            # 關鍵修正：宣告 3 個 Tabs
            tab1, tab2, tab3 = st.tabs(["潛力新星搜尋", "現有隊員追蹤", "📊 全班數據解析"])
            
            with tab1:
                st.write("🔍 **非校隊尖子：**")
                st.dataframe(all_db[all_db['所屬校隊'] == "無"].nlargest(10, '總分')[['姓名', '總分', 'BMI']], hide_index=True)
                    
            with tab2:
                team_sel = st.selectbox("請選擇隊伍：", ["足球隊", "壁球隊", "乒乓球隊", "籃球隊", "田徑隊", "射箭隊"], key="mgr_team_sel")
                team_members = all_db[all_db['所屬校隊'] == team_sel].copy()
                if not team_members.empty:
                    def highlight_low_scores(row):
                        return ['background-color: #990000; color: white'] * len(row) if row.總分 < 24 else [''] * len(row)
                    st.dataframe(team_members[['姓名', '總分', 'BMI', '時間']].style.apply(highlight_low_scores, axis=1), use_container_width=True)
                else: st.warning("無紀錄")

            with tab3:
                st.subheader("📊 班級體能大數據")
                d1, d2 = st.columns(2)
                with d1:
                    st.write("📈 **BMI 分佈**")
                    bmi_bins = [0, 18.5, 24, 27, 100]
                    bmi_labels = ['體重過輕', '正常', '過重', '肥胖']
                    plot_df = all_db.copy()
                    plot_df['BMI分類'] = pd.cut(plot_df['BMI'], bins=bmi_bins, labels=bmi_labels)
                    st.bar_chart(plot_df['BMI分類'].value_counts())
                with d2:
                    st.write("🎯 **等級分佈**")
                    def get_rank_str(s):
                        if s >= 32: return "🥇 卓越"
                        if s >= 24: return "🥈 優良"
                        return "⚪ 需加強"
                    plot_df['等級'] = plot_df['總分'].apply(get_rank_str)
                    st.bar_chart(plot_df['等級'].value_counts())
                
                csv_data = all_db.to_csv(index=False).encode('utf-8-sig')
                st.download_button("💾 下載全校期末總表 (CSV)", csv_data, f"Fitness_{datetime.now().year}.csv", "text/csv")
        else: st.info("尚無紀錄")
else: st.error("❌ 找不到數據庫！")
















