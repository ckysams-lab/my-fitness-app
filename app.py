import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. 頁面與連線設定
st.set_page_config(page_title="小學體適能數位戰報系統 v2.0", page_icon="🏃‍♂️", layout="wide")

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
        # A. 計算分數
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data) 
        s3 = get_score(v3, gender, age, "grip_strength", data)
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4
        categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘耐力跑']
        scores = [s1, s2, s3, s4]

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
            h1, h2, h3, h4, p, span, label, div {{ color: white !important; }}
            .header-box h1, .header-box h2 {{ color: black !important; }}
            div[data-testid="stProgress"] > div > div > div > div {{ background-color: {accent} !important; }}
            </style>
        """, unsafe_allow_html=True)

        # D. 個人戰報抬頭
        st.markdown(f'<div class="header-box"><h1>{name} 體能戰報</h1><h2>{rank_label}</h2></div>', unsafe_allow_html=True)
        
        # E. 數據看板
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card"><h4>總得分</h4><h2 style="color:{accent} !important;">{total} / 40</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><h4>BMI 指數</h4><h2 style="color:{accent} !important;">{bmi}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><h4>目前校隊</h4><h2 style="color:{accent} !important;">{current_team}</h2></div>', unsafe_allow_html=True)

        # F. 視覺化：雷達圖與 AI 助教
        st.divider()
        g1, g2 = st.columns([1.2, 1])
        with g1:
            fig = go.Figure(go.Scatterpolar(
                r=scores + [scores[0]], theta=categories + [categories[0]], 
                fill='toself', line=dict(color=accent), fillcolor=f"rgba({rgb}, 0.3)"
            ))
            fig.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 10], gridcolor="#444")),
                paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with g2:
            st.markdown("### 🤖 AI 智能助教評語")
            # AI 邏輯生成
            ai_comment = []
            if total >= 32: ai_comment.append(f"震撼！{name} 你具備頂尖運動員的素質。")
            elif total >= 24: ai_comment.append(f"出色！{name} 你的體能表現非常全面。")
            else: ai_comment.append(f"加油 {name}！專注於強項發展，你能做得更好。")
            
            best_idx = scores.index(max(scores))
            ai_comment.append(f"你的 **{categories[best_idx]}** 表現最為突出，這是你的天賦所在。")
            
            if bmi > 24: ai_comment.append("注意：增加有氧運動可減輕關節負擔。")
            elif bmi < 18.5: ai_comment.append("提醒：多攝取營養並強化力量訓練。")
            
            st.info("\n\n".join(ai_comment))

            # 天賦稱號
            titles = []
            if s1 == 10: titles.append("🧱 核心守護者")
            if s2 == 10: titles.append("🤸 柔軟大師")
            if s3 == 10: titles.append("💪 校園力王")
            if s4 == 10: titles.append("🔥 無盡引擎")
            if titles:
                st.write("✨ **解鎖稱號：**")
                title_html = "".join([f'<span style="background-color:gold; color:black; padding:4px 10px; border-radius:15px; margin-right:5px; font-weight:bold;">{t}</span>' for t in titles])
                st.markdown(title_html, unsafe_allow_html=True)

        # G. 運動處方
        st.divider()
        st.subheader("🎯 針對性運動處方")
        rec1, rec2 = st.columns(2)
        with rec1:
            st.write("🏆 **優勢推薦：**")
            if s1 >= 8: st.success("🏀 核心強：推薦籃球/足球隊")
            if s2 >= 8: st.success("🧘 柔軟好：推薦舞蹈/壁球隊")
            if s3 >= 8: st.success("🎾 力量大：推薦乒乓球/壁球")
            if s4 >= 8: st.success("⚽ 耐力佳：推薦田徑/足球隊")
        with rec2:
            st.write("🛠️ **弱項加強：**")
            if s1 <= 4: st.warning("🧱 每日練習 30s 棒式。")
            if s2 <= 4: st.warning("🧘 每日睡前拉筋伸展。")
            if s3 <= 4: st.warning("💪 使用握力器強化上肢。")
            if s4 <= 4: st.warning("🏃 每週兩次 10min 慢跑。")

        # H. 雲端同步與老師後台
        try:
            res_df = pd.DataFrame([{
                "時間": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "姓名": name, "性別": gender, "年齡": age, "所屬校隊": current_team,
                "BMI": bmi, "總分": total, "仰臥起坐": v1, "體前彎": v2, "手握力": v3, "9分鐘耐力跑": v4
            }])
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, res_df], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ 數據已雲端同步。")
        except:
            st.warning("⚠️ 雲端同步失敗。")

        # ---------------------------------------------------------
    # I. 老師大盤分析 (獨立於提交按鈕外，解決彈走問題)
    # ---------------------------------------------------------
    st.write("---")
    with st.expander("📊 老師專屬：全校管理後台 (不需點擊按鈕即可查看)"):
        all_db = conn.read(ttl=0)
        if not all_db.empty:
            # 1. 英雄榜區塊
            st.subheader("🏆 全校榮譽榜")
            h1, h2 = st.columns(2)
            with h1:
                st.write("✨ **總分 Top 5**")
                st.table(all_db.nlargest(5, '總分')[['姓名', '總分', '所屬校隊']])
            with h2:
                st.write("🔥 **單項最強王者**")
                # 預防數據報錯，使用 try 抓取
                try:
                    b1 = all_db.loc[all_db['仰臥起坐'].idxmax()]
                    b2 = all_db.loc[all_db['體前彎'].idxmax()]
                    b3 = all_db.loc[all_db['手握力'].idxmax()]
                    b4 = all_db.loc[all_db['9分鐘耐力跑'].idxmax()]
                    st.write(f"🧱 核心王：{b1['姓名']} ({int(b1['仰臥起坐'])}次)")
                    st.write(f"🤸 柔軟王：{b2['姓名']} ({int(b2['體前彎'])}cm)")
                    st.write(f"💪 力量王：{b3['姓名']} ({b3['手握力']}kg)")
                    st.write(f"🏃 耐力王：{b4['姓名']} ({int(b4['9分鐘耐力跑'])}m)")
                except:
                    st.write("計算中...")

            # 2. 校隊選拔與監控
            st.divider()
            st.subheader("🕵️ 校隊人才與成員監控")
            
            # 使用 tab 讓介面更整齊
            tab1, tab2, tab3 = st.tabs(["潛力新星搜尋", "現有隊員追蹤", "📊 全班數據解析"])
            
            with tab1:
                st.write("非校隊成員中，各項前 20% 的尖子：")
                non_team = all_db[all_db['所屬校隊'] == "無"]
                if not non_team.empty:
                    st.dataframe(non_team.nlargest(10, '總分')[['姓名', '總分', 'BMI', '時間']], hide_index=True)
                else:
                    st.info("目前所有學生皆已加入校隊。")
                    
            with tab2:
                team_sel = st.selectbox("請選擇要查看的隊伍：", ["足球隊", "壁球隊", "乒乓球隊", "籃球隊", "田徑隊", "射箭隊"], key="mgr_team_sel")
                team_members = all_db[all_db['所屬校隊'] == team_sel].copy()
                
                if not team_members.empty:
                    st.write(f"目前 {team_sel} 共有 {len(team_members)} 名隊員：")
                    
                    # --- 定義變色函數 ---
                    def highlight_low_scores(row):
                        # 如果總分低於 24，背景設為深紅色，文字設為白色
                        if row.總分 < 24:
                            return ['background-color: #990000; color: white'] * len(row)
                        return [''] * len(row)

                    # 套用樣式並顯示
                    styled_df = team_members[['姓名', '總分', 'BMI', '時間']].sort_values('總分', ascending=False).style.apply(highlight_low_scores, axis=1)
                    
                    st.dataframe(styled_df, use_container_width=True)
                else:
                    st.warning(f"資料庫中暫無 {team_sel} 的隊員紀錄。")
                
            with tab3: # 新增一個 Tab
                st.subheader("📊 全班體能與健康分佈")
                dist_col1, dist_col2 = st.columns(2)
                
                with dist_col1:
                    st.write("📈 **體位 (BMI) 分佈狀態**")
                    # 將 BMI 分類
                    bmi_bins = [0, 18.5, 24, 27, 100]
                    bmi_labels = ['體重過輕', '正常範圍', '過重', '肥胖']
                    all_db['BMI分類'] = pd.cut(all_db['BMI'], bins=bmi_bins, labels=bmi_labels)
                    bmi_counts = all_db['BMI分類'].value_counts()
                    st.bar_chart(bmi_counts)
                
                with dist_col2:
                    st.write("🎯 **體能等級佔比**")
                    # 根據總分定義等級
                    def get_rank(s):
                        if s >= 32: return "🥇 卓越"
                        if s >= 24: return "🥈 優良"
                        if s >= 16: return "🥉 尚可"
                        return "⚪ 待加強"
                    all_db['等級'] = all_db['總分'].apply(get_rank)
                    rank_counts = all_db['等級'].value_counts()
                    st.bar_chart(rank_counts)

                st.divider()
                st.write("📥 **行政存檔專區**")
                # 提供一鍵下載全班總表
                csv_all = all_db.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="💾 下載全校期末體能總表 (Excel 格式)",
                    data=csv_all,
                    file_name=f"Physical_Fitness_Final_{datetime.now().strftime('%Y')}.csv",
                    mime="text/csv"
                )
else:
    st.error("❌ 找不到數據庫 (norms.json)！")















