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
        # A. 計算分數
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data)
        s3 = get_score(v3, gender, age, "grip_strength", data) 
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4

        # B. 根據分數決定主題色
        if total >= 15:
            rank_color = "#FFD700"  # 金色
            rank_label = "🥇 卓越 (Gold)"
        elif total >= 10:
            rank_color = "#C0C0C0"  # 銀色
            rank_label = "🥈 優良 (Silver)"
        elif total >= 8:
            rank_color = "#CD7F32"  # 銅色
            rank_label = "🥉 尚可 (Bronze)"
        else:
            rank_color = "#E74C3C"  # 紅色
            rank_label = "⚪ 待加強"

        # C. 專業儀表板抬頭
        st.markdown(f"""
            <div style="background-color:{rank_color}; padding:20px; border-radius:10px; text-align:center;">
                <h1 style="color:white; margin:0;">{name} 的體能戰報</h1>
                <h2 style="color:white; margin:0;">{rank_label}</h2>
            </div>
        """, unsafe_allow_html=True)

        # D. 核心數據大指標
        st.write("")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("總得分", f"{total} / 20")
        m_col2.metric("BMI 狀態", bmi, delta="正常" if 18.5 <= bmi <= 24 else "異常", delta_color="normal" if 18.5 <= bmi <= 24 else "inverse")
        m_col3.metric("評測等級", rank_label.split(" ")[1])

        # E. 雷達圖與進度條分析 (左右並列)
        st.divider()
        g_col1, g_col2 = st.columns([1, 1])

        with g_col1:
            st.subheader("🕸️ 體能雷達圖")
            categories = ['仰臥起坐', '坐姿體前彎', '手握力', '耐力跑']
            scores = [s1, s2, s3, s4]
            categories_closed = categories + [categories[0]]
            scores_closed = scores + [scores[0]]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores_closed, theta=categories_closed, fill='toself',
                line_color=rank_color, fillcolor=rank_color, opacity=0.6
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, height=350, margin=dict(l=40, r=40, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with g_col2:
            st.subheader("📊 分項強弱分析")
            for label, score in zip(categories, scores):
                st.write(f"**{label}** ({score}/5)")
                st.progress(score / 5) # 自動生成運動感進度條

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






