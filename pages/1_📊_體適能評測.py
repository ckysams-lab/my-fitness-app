import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from utils import load_norms, get_score

# 1. 頁面基本設定
st.set_page_config(page_title="正覺蓮社學校 - 體適能評測", layout="wide")

# 2. 陽光活力版 CSS (明亮淺色系)
st.markdown("""
    <style>
        /* 整體背景：淺灰色漸變，光亮舒適 */
        .stApp { 
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); 
        }
        
        /* 側邊欄改為純白 */
        [data-testid="stSidebar"] { background-color: #ffffff !important; }
        [data-testid="stSidebar"] a { font-size: 20px !important; color: #2c3e50 !important; }
        [data-testid="stSidebar"] h3 { color: #3498db !important; text-align: center; }

        /* 標題區塊 */
        .header-box { 
            padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: white;
            border-top: 8px solid;
        }
        .header-box h1 { color: #2c3e50 !important; font-size: 2.5rem; font-weight: 800; }
        
        /* 等級標籤 */
        .badge { 
            background: #2c3e50; color: white !important; padding: 8px 25px; 
            border-radius: 50px; font-weight: bold; display: inline-block; margin-top: 15px; 
        }

        /* 數據卡片：白底深字 */
        .metric-card { 
            background: white; padding: 20px; border-radius: 15px; margin: 10px 0; 
            border-left: 6px solid; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        
        /* 強制所有標題與內文為深色，方便閱讀 */
        h1, h2, h3, h4, p, span, label { color: #2c3e50 !important; }
        
        /* 表單區域美化 */
        [data-testid="stForm"] {
            background: white; border-radius: 20px; padding: 30px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: none;
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
    st.page_link("pages/04_🌟_體育之星.py", label="體育之星", icon="🌟")

# 3. 準備數據與連線
data = load_norms()
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("雲端連線異常")

st.title("📊 學生體適能評測系統")
st.markdown("請輸入數據，系統將自動生成 AI 分析戰報。")

if data:
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

        # 顏色邏輯 (活力亮色)
        if total >= 32: accent, rank_label = "#f1c40f", "🥇 卓越 (GOLD)" # 金黃
        elif total >= 24: accent, rank_label = "#3498db", "🥈 優良 (SILVER)" # 天藍
        elif total >= 16: accent, rank_label = "#e67e22", "🥉 尚可 (BRONZE)" # 活力橙
        else: accent, rank_label = "#e74c3c", "⚪ 待加強 (CHALLENGER)" # 警告紅

        st.markdown(f"""
            <div class="header-box" style="border-top-color: {accent};">
                <h1>{name} 同學的體能戰報</h1>
                <div class="badge">{rank_label}</div>
            </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card" style="border-left-color:{accent}"><h4>總分</h4><h2 style="color:{accent} !important">{total} / 40</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card" style="border-left-color:{accent}"><h4>BMI 指數</h4><h2 style="color:{accent} !important">{bmi}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card" style="border-left-color:{accent}"><h4>時間 (HKT)</h4><h2 style="color:{accent} !important; font-size:1.5rem;">{hk_now.strftime("%H:%M")}</h2></div>', unsafe_allow_html=True)

        st.divider()

        g_col1, g_col2 = st.columns([1.2, 1])
        with g_col1:
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]], theta=categories + [categories[0]],
                fill='toself', fillcolor=f"rgba(52, 152, 219, 0.2)",
                line=dict(color='#3498db', width=4)
            ))
            fig.update_layout(
                polar=dict(bgcolor="white", radialaxis=dict(visible=True, range=[0, 10], gridcolor="#eee")),
                paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#2c3e50", size=14), height=500
            )
            st.plotly_chart(fig, use_container_width=True)

        with g_col2:
            st.subheader("🤖 AI 智能助教分析")
            
            # 邏輯引擎
            if bmi < 18.5: bmi_note = "體重較輕，建議增加蛋白質攝取，配合肌力訓練。"
            elif bmi < 23: bmi_note = "體態非常標準，請繼續保持均衡飲食與運動。"
            else: bmi_note = "體重指標偏高，建議增加有氧運動時間，並注意飲食份量。"

            advice_map = {
                "仰臥起坐": "核心肌群稍弱。建議每日進行『平板支撐』訓練，增強腹部力量。",
                "坐姿體前彎": "柔軟度限制了活動範圍。建議每天運動後進行 5 分鐘下肢伸展。",
                "手握力": "上肢爆發力有進步空間。可以嘗試多做攀爬架運動或引體上升。",
                "9分鐘跑": "心肺耐力是基石。建議每週末嘗試 15 分鐘慢跑，循序漸進。"
            }

            scores_dict = dict(zip(categories, scores))
            best_item = max(scores_dict, key=scores_dict.get)
            worst_item = min(scores_dict, key=scores_dict.get)

            with st.container(border=True):
                st.info(f"⚖️ **體態評估：** {bmi_note}")
                st.success(f"🔥 **核心優勢：** 你在「{best_item}」展現了極佳天賦！")
                st.warning(f"🛠️ **重點突破：** 目前「{worst_item}」得分較低。{advice_map.get(worst_item)}")
                st.markdown("---")
                st.write("💡 **助教寄語：** 每天進步 1%，一年後你將煥然一新！加油！")

        # 雲端同步
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






