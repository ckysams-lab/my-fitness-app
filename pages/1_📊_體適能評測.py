import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from utils import load_norms, get_score  # 確保 utils.py 在根目錄

# 1. 頁面基本設定 (Sidebar 導航)
st.set_page_config(page_title="正覺蓮社學校 - 體適能評測", layout="wide")

# 2. Sidebar 導航與 深色科技感 CSS (已還原)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] a { font-size: 22px !important; margin-bottom: 10px; }
        [data-testid="stSidebar"] h3 { font-size: 28px !important; color: #FFD700; text-align: center; }
        /* 還原深色背景 */
        .stApp { background: radial-gradient(circle, #1A1A2E 0%, #0F0F1B 100%); }
        .header-box { padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; }
        .header-box h1 { color: white !important; margin: 0; font-size: 2.5rem; font-weight: 800; }
        .badge { background: white; color: black !important; padding: 10px 30px; border-radius: 50px; font-weight: bold; font-size: 1.2rem; display: inline-block; margin-top: 15px; }
        /* 修正後的數據卡片樣式 */
        .metric-card { 
            background: rgba(255,255,255,0.08); 
            padding: 25px 20px; 
            border-radius: 12px; 
            margin: 10px 0; 
            border-left: 6px solid; 
            /* 新增下面這兩行來確保對稱 */
            min-height: 140px; 
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🏫 正覺蓮社學校\n### 🏆 體育組")
    st.divider()
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
    st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
    st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")
    # 確保這一行存在，體育之星才會出現
    st.page_link("pages/04_🌟_體育之星.py", label="體育之星", icon="🌟")

# 3. 準備環境
data = load_norms()
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"雲端連線異常: {e}")

st.title("📊 學生體適能評測系統")
st.markdown("請在下方輸入測驗數據，系統將自動生成 AI 分析戰報。")

if data:
    # --- A. 輸入區域 (Form) ---
    with st.form("input_form"):
        st.subheader("📝 基本資料")
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

        st.divider()
        st.subheader("💪 測驗數據")
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        v1 = v_col1.number_input("仰臥起坐 (次)", 0)
        v2 = v_col2.number_input("坐姿體前彎 (cm)", 0)
        v3 = v_col3.number_input("手握力 (kg)", 0.0, 100.0, 10.0)
        v4 = v_col4.number_input("9分鐘耐力跑 (米)", 0)
        
        submitted = st.form_submit_button("🌟 生成個人戰報並啟動 AI 分析")

    # --- B. 提交後的結果顯示區域 ---
    if submitted:
        hk_now = datetime.utcnow() + timedelta(hours=8)
        hk_time_str = hk_now.strftime("%Y-%m-%d %H:%M:%S")
        
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data) 
        s3 = get_score(v3, gender, age, "grip_strength", data)
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4
        categories = ['仰臥起坐', '坐姿體前彎', '手握力', '9分鐘跑']
        scores = [s1, s2, s3, s4]

        if total >= 32: rgb, rank_label = "255, 215, 0", "🥇 卓越 (GOLD)"
        elif total >= 24: rgb, rank_label = "0, 212, 255", "🥈 優良 (SILVER)"
        elif total >= 16: rgb, rank_label = "255, 140, 0", "🥉 尚可 (BRONZE)"
        else: rgb, rank_label = "255, 46, 99", "⚪ 待加強 (CHALLENGER)"
        accent = f"rgb({rgb})"

        st.markdown(f"""
            <div class="header-box" style="background-color: {accent};">
                <h1 style="color: black !important;">{name} 同學的體能戰報</h1>
                <div class="badge">{rank_label}</div>
            </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; gap: 20px; margin: 20px 0;">
                <div class="metric-card" style="flex: 1; border-left-color: {accent}; margin: 0;">
                    <h4>總分</h4>
                    <h2 style="color: {accent} !important;">{total} / 40</h2>
                </div>
                <div class="metric-card" style="flex: 1; border-left-color: {accent}; margin: 0;">
                    <h4>BMI 指數</h4>
                    <h2 style="color: {accent} !important;">{bmi}</h2>
                </div>
                <div class="metric-card" style="flex: 1; border-left-color: {accent}; margin: 0;">
                    <h4>時間 (HKT)</h4>
                    <h2 style="color: {accent} !important; font-size: 2.2rem;">{hk_now.strftime("%H:%M")}</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        g_col1, g_col2 = st.columns([1.2, 1])
        with g_col1:
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]], theta=categories + [categories[0]],
                fill='toself', fillcolor=f"rgba({rgb}, 0.3)",
                line=dict(color=accent, width=4)
            ))
            fig.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 10], gridcolor="#444")),
                paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white", size=14), height=500
            )
            st.plotly_chart(fig, use_container_width=True)

        with g_col2:
            st.subheader("🤖 AI 智能助教深度分析")
            if bmi < 18.5: bmi_note = "體重較輕，建議增加蛋白質攝取，配合肌力訓練。"
            elif bmi < 23: bmi_note = "體態非常標準，請繼續保持均衡飲食與運動。"
            else: bmi_note = "體重指標偏高，建議增加有氧運動時間，並注意飲食份量。"

            advice_map = {
                "仰臥起坐": "核心肌群稍弱。建議每日進行『平板支撐』訓練，穩定脊椎並增強腹部力量。",
                "坐姿體前彎": "柔軟度限制了你的活動範圍。建議每天運動後進行 5 分鐘下肢伸展。",
                "手握力": "上肢爆發力有進步空間。可以嘗試多做攀爬架運動或引體上升。",
                "9分鐘跑": "心肺耐力是運動的基石。建議每週末嘗試 15 分鐘慢跑，提升心肺功能。"
            }

            scores_dict = {"仰臥起坐": s1, "坐姿體前彎": s2, "手握力": s3, "9分鐘跑": s4}
            best_item = max(scores_dict, key=scores_dict.get)
            worst_item = min(scores_dict, key=scores_dict.get)

            with st.container(border=True):
                st.info(f"⚖️ **體態評估：** {bmi_note}")
                st.success(f"🔥 **核心優勢：** 你在「{best_item}」展現了極佳天賦！")
                st.warning(f"🛠️ **重點突破：** 目前「{worst_item}」得分相對較低。{advice_map.get(worst_item)}")
                st.markdown("---")
                st.write("💡 **助教寄語：** 每天進步 1%，一年後你將煥然一新！加油！")

        try:
            res_df = pd.DataFrame([{
                "時間": hk_time_str, "姓名": name, "性別": gender, "年齡": age, 
                "總分": total, "BMI": bmi, "等級": rank_label,
                "仰臥起坐": v1, "體前彎": v2, "手握力": v3, "9分鐘跑": v4
            }])
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, res_df], ignore_index=True)
            conn.update(data=updated_df)
            st.toast("✅ 數據已雲端同步")
        except:
            st.warning("⚠️ 數據未能存檔")
        
        st.balloons()
else:
    st.error("找不到數據庫，請確認檔案路徑。")









