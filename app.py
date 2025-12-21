import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# 1. 頁面與連線設定
st.set_page_config(page_title="體適能評測系統", page_icon="📊")

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
st.title("🏃‍♂️ 小學體適能評測系統")
data = load_data()

if data:
    # 3. 建立表單
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        gender = col1.radio("性別", ["男", "女"], horizontal=True)
        age = col2.number_input("年齡", 5, 13, 10)
        name = st.text_input("學生姓名/編號", "學生A")
        
        st.subheader("測量數值")
        h = st.number_input("身高 (cm)", 100.0, 180.0, 140.0)
        w = st.number_input("體重 (kg)", 15.0, 90.0, 35.0)
        v1 = st.number_input("仰臥起坐 (次)", 0)
        v2 = st.number_input("坐姿體前彎 (cm)", 0)
        v3 = st.number_input("手握力 (kg)", 0.0, 50.0, 15.0)
        v4 = st.number_input("9分鐘耐力跑 (米)", 0)
        
        submitted = st.form_submit_button("🌟 計算總成績")

    # 4. 提交後的處理 (按鈕按下後才執行以下所有內容)
    if submitted:
        # A. 分數判定與主題色設定 (改用 RGBA 格式)
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data)
        s3 = get_score(v3, gender, age, "grip_strength", data) 
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4

        # 定義不同獎項的「發光色」 (R, G, B)
        if total >= 15:
            base_rgb = "255, 215, 0"  # 鮮豔金
            rank_name = "GOLD ELITE"
        elif total >= 10:
            base_rgb = "0, 212, 255"  # 科技藍
            rank_name = "SILVER PRO"
        elif total >= 8:
            base_rgb = "255, 140, 0"  # 活力橘
            rank_name = "BRONZE ACTIVE"
        else:
            base_rgb = "255, 46, 99"  # 極限紅
            rank_name = "CHALLENGER"

        accent_color = f"rgb({base_rgb})"
        fill_color = f"rgba({base_rgb}, 0.3)" # 設定 30% 透明度

        # --- B. 注入 CSS (同步更新背景顏色引用) ---
        st.markdown(f"""
            <style>
            .stApp {{ background: radial-gradient(circle, #1A1A2E 0%, #0F0F1B 100%); color: #FFFFFF !important; }}
            .stats-card {{
                background: rgba(255, 255, 255, 0.05);
                border-left: 5px solid {accent_color};
                padding: 20px; border-radius: 10px; margin-bottom: 20px;
            }}
            h1, h2, h3, span, p, label {{ color: #FFFFFF !important; }}
            div[data-testid="stMetricValue"] {{ color: {accent_color} !important; }}
            </style>
        """, unsafe_allow_html=True)

        # ... (中間標題與 Metrics 部分不變) ...

        # --- E. 圖表區塊 (修正後的 Plotly 部分) ---
        st.divider()
        g1, g2 = st.columns([1, 1])
        with g1:
            categories = ['仰臥起坐', '坐姿體前彎', '手握力', '耐力跑']
            scores = [s1, s2, s3, s4]
            categories_closed = categories + [categories[0]]
            scores_closed = scores + [scores[0]]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores_closed,
                theta=categories_closed,
                fill='toself',
                line=dict(color=accent_color), # 修正顏色設定方式
                fillcolor=fill_color           # 修正顏色設定方式
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 5], gridcolor="#444", tickfont=dict(color="white")),
                    angularaxis=dict(gridcolor="#444", tickfont=dict(color="white"))
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False, height=350, margin=dict(l=40, r=40, t=30, b=30)
            )
            st.plotly_chart(fig, use_container_width=True)

        with g2:
            st.markdown(f"### ⚡ 專項分析")
            for label, score in zip(categories, scores):
                # 計算百分比
                pct = (score / 5) * 100
                
                # 使用 HTML 建立自定義霓虹進度條
                st.markdown(f"""
                    <div style="margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold; color: white;">{label}</span>
                            <span style="color: {accent_color}; font-weight: bold;">{score} / 5</span>
                        </div>
                        <div style="background-color: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; width: 100%;">
                            <div style="background-color: {accent_color}; 
                                        width: {pct}%; 
                                        height: 100%; 
                                        border-radius: 10px; 
                                        box-shadow: 0 0 10px {accent_color}AA;">
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        # F. 運動建議與同步邏輯 (其餘部分保持不變)
        st.divider()
        # ... (原本的自動同步與下載代碼) ...

        # D. 運動建議
        if s3 <= 2:
            st.warning("📍 **提升上肢肌力 (手握力)**")
            st.write("建議練習擠壓網球或使用握力器，每天每手 15 次，重複 3 組。")

        # E. 自動同步至 Google Sheets
        try:
            res_df = pd.DataFrame([{
                "時間": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                "姓名": name, "性別": gender, "年齡": age,
                "BMI": bmi, "總分": total,
                "仰臥起坐": v1, "體前彎": v2, "手握力": v3, "9分鐘耐力跑": v4
            }])
            
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, res_df], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ 數據已自動存入雲端試算表！")
            
        except Exception as e:
            error_msg = str(e)
            if "Public Spreadsheet cannot be written to" in error_msg:
                st.error("❌ 權限不足：請確認 Secrets 中的 Service Account 設定正確。")
            else:
                st.warning(f"⚠️ 同步失敗，請檢查試算表標題是否正確。錯誤：{e}")

        # F. 下載備份
        csv = res_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載本次報告 (CSV)", csv, f"{name}.csv", "text/csv")

else:
    st.error("❌ 找不到數據庫！請確保 norms.json 存在。")









