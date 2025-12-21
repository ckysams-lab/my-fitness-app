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
            if val >= t: return 5 - i
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
            # 在姓名輸入框下方加入
            enable_cam = st.checkbox("📸 開啟相機拍攝球員照")
            photo = None
        if enable_cam:
            photo = st.camera_input("請對準學生拍照")
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
        
        submitted = st.form_submit_button("🌟 生成個人戰報並同步雲端")

    # 4. 提交後的處理 (核心邏輯)
    if submitted:
        # A. 計算分數
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)×2
        s2 = get_score(v2, gender, age, "sit_reach", data)×2
        s3 = get_score(v3, gender, age, "grip_strength", data)×2 
        s4 = get_score(v4, gender, age, "run_9min", data)×2
        total = s1 + s2 + s3 + s4

        # B. 決定等級與主題色
        if total >= 15:
            rgb, rank_label = "255, 215, 0", "🥇 卓越 (GOLD ELITE)"
        elif total >= 10:
            rgb, rank_label = "0, 212, 255", "🥈 優良 (SILVER PRO)"
        elif total >= 8:
            rgb, rank_label = "255, 140, 0", "🥉 尚可 (BRONZE)"
        else:
            rgb, rank_label = "255, 46, 99", "⚪ 待加強 (CHALLENGER)"

        accent = f"rgb({rgb})"
        
        # C. 注入 CSS
        st.markdown(f"""
            <style>
            .stApp {{ background: radial-gradient(circle, #1A1A2E 0%, #0F0F1B 100%); color: white !important; }}
            .header-box {{ background-color: {accent}; padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 0 20px {accent}; margin-bottom: 25px; color: black !important; }}
            .metric-card {{ background: rgba(255,255,255,0.05); border-left: 5px solid {accent}; padding: 15px; border-radius: 10px; }}
            div[data-testid="stProgress"] > div > div > div > div {{ background-color: {accent} !important; }}
            h1, h2, h3, h4, p, span, label {{ color: white !important; }}
            </style>
        """, unsafe_allow_html=True)

        # D. 個人戰報抬頭與勳章
        st.markdown(f'<div class="header-box"><h1 style="color:black !important; margin:0;">{name} 體能戰報</h1><h2 style="color:black !important; margin:0;">{rank_label}</h2></div>', unsafe_allow_html=True)
        
        # --- 勳章與照片顯示 ---
        st.divider()
        c1, c2 = st.columns([1, 2])
        
        with c1:
            if photo:
                st.image(photo, caption=f"{name} 選手", use_container_width=True)
            else:
                st.info("尚未拍攝照片")
                
        with c2:
            st.markdown("### 🏆 獲得勳章")
            badges = []
            if s1 == 5: badges.append("🧱 鋼鐵核心")
            if s2 == 5: badges.append("🤸 柔軟大師")
            if s3 == 5: badges.append("⚡ 神力超人")
            if s4 == 5: badges.append("🔥 耐力之王")
            
            if badges:
                for b in badges:
                    st.success(f"🏅 {b}")
            else:
                st.write("繼續努力，解鎖專項勳章！")

        # E. 數據看板
        st.write("")
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card"><h4>總得分</h4><h2 style="color:{accent} !important;">{total} / 20</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><h4>BMI 指數</h4><h2 style="color:{accent} !important;">{bmi}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><h4>目前隊伍</h4><h2 style="color:{accent} !important;">{current_team}</h2></div>', unsafe_allow_html=True)

        # F. 體能球員卡看板 (照片與雷達圖)
        st.divider()
        g1, g2, g3 = st.columns([1, 1.2, 1]) # 三欄佈局：照片 | 雷達圖 | 分數
        
        with g1:
            st.markdown("### 👤 選手動態")
            if photo:
                # 顯示拍攝的照片
                st.image(photo, use_container_width=True)
                st.markdown(f"<p style='text-align:center;'>{current_team} 成員</p>", unsafe_allow_html=True)
            else:
                # 若未拍照則顯示預設圖示
                st.markdown(f"""
                    <div style="height:250px; background:rgba(255,255,255,0.05); 
                                display:flex; align-items:center; justify-content:center; border-radius:15px;">
                        <span style="font-size:5rem;">👤</span>
                    </div>
                """, unsafe_allow_html=True)

        with g2:
            st.markdown("### 🕸️ 均衡度分析")
            categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘耐力跑']
            scores = [s1, s2, s3, s4]
            fig = go.Figure(go.Scatterpolar(
                r=scores + [scores[0]], theta=categories + [categories[0]], 
                fill='toself', line=dict(color=accent), fillcolor=f"rgba({rgb}, 0.3)"
            ))
            fig.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 5], gridcolor="#444")),
                paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=300, margin=dict(l=30, r=30, t=30, b=30)
            )
            st.plotly_chart(fig, use_container_width=True)

        with g3:
            st.markdown("### 📊 分數統計")
            for label, score in zip(categories, scores):
                st.write(f"**{label}**")
                st.progress(score / 5)

        # G. 智能社團推薦與處方
        st.divider()
        st.subheader("🎯 運動處方與推薦")
        score_dict = dict(zip(categories, scores))
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            if s4 >= 4: st.success("⚽ **推薦社團：足球 / 田徑** (具備優秀耐力)")
            elif s3 >= 4: st.success("🎾 **推薦社團：壁球 / 乒乓球** (上肢力量強)")
            elif s1 >= 4: st.success("🏀 **推薦社團：籃球** (核心穩定性佳)")
            else: st.info("🏃 **建議：** 多方嘗試各項校隊，找出最有興趣的項目！")
            
        with rec_col2:
            if s2 <= 2: st.warning("🧘 **運動建議：** 每天進行坐姿體前彎拉伸 5 分鐘。")
            if s4 <= 2: st.warning("🏃 **運動建議：** 每週進行兩次 15 分鐘慢跑提升心肺。")

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
            st.success("✅ 數據已自動同步至雲端！")
        except:
            st.warning("⚠️ 雲端同步失敗，請下載 CSV 備份。")

        # 下載按鈕
        st.download_button("📥 下載本次報告 (CSV)", res_df.to_csv(index=False).encode('utf-8-sig'), f"{name}_report.csv")

        # I. 老師大盤分析
        st.write("")
        with st.expander("📊 老師專屬：班級/校隊大盤分析"):
            all_db = conn.read(ttl=0)
            if not all_db.empty:
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    st.write("🏃 **各校隊平均總分對比**")
                    st.bar_chart(all_db.groupby("所屬校隊")["總分"].mean())
                with c_col2:
                    st.write("📈 **全校體能分佈**")
                    st.line_chart(all_db["總分"].value_counts().sort_index())
                st.write("⚠️ **健康預警名單 (總分 < 8)**")
                st.dataframe(all_db[all_db["總分"] < 8][["姓名", "所屬校隊", "總分", "BMI"]])
else:
    st.error("❌ 找不到 norms.json 數據庫！")





















