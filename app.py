import streamlit as st
import json
import pandas as pd
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
        # 請確保 norms.json 裡有 "grip_strength" 這一項
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
        v3 = st.number_input("手握力 (kg)", 0.0, 50.0, 15.0) # 改成手握力
        v4 = st.number_input("耐力跑 (米)", 0)
        
        submitted = st.form_submit_button("🌟 計算並同步數據")

    # 4. 提交後的處理 (必須在 st.form 之外，且在下方)
    if submitted:
        # A. 計算分數
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data)
        s3 = get_score(v3, gender, age, "grip_strength", data) # 改成 grip_strength
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4
        
        # B. 顯示結果
        st.divider()
        st.header(f"您的總分：{total} / 20 分")
        if total >= 15: st.success("🥇 獲得金獎！表現卓越！")
        elif total >= 9: st.warning("🥉 獲得銅獎！還有進步空間！")
        st.info(f"📊 BMI 指數: {bmi}")

        # C. 運動建議 (這裡示範握力建議)
        if s3 <= 2:
            st.warning("📍 **提升上肢肌力 (手握力)**")
            st.write("建議練習擠壓網球或使用握力器，每天每手 15 次，重複 3 組。")

        # D. 自動同步至 Google Sheets
        try:
            res_df = pd.DataFrame([{
                "時間": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                "姓名": name, "性別": gender, "年齡": age,
                "BMI": bmi, "總分": total,
                "仰臥起坐": v1, "體前彎": v2, "手握力": v3, "耐力跑": v4
            }])
            
            # 讀取並更新
            existing_data = conn.read()
            updated_df = pd.concat([existing_data, res_df], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ 數據已自動存入雲端試算表！")
        except Exception as e:
            st.warning(f"⚠️ 雲端同步失敗，請確認標題欄位是否一致。錯誤：{e}")

        # E. 下載備份
        csv = res_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載本次報告 (CSV)", csv, f"{name}.csv", "text/csv")

else:
    st.error("❌ 找不到數據庫！請確保 norms.json 存在。")
