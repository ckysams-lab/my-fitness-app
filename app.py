import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="體適能評測系統", page_icon="📊")

# 1. 載入數據
def load_data():
    try:
        with open('norms.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

# 2. 評分邏輯
def get_score(val, gender, age, item_key, data):
    try:
        thresholds = data[item_key][gender][str(age)]
        for i, t in enumerate(thresholds):
            if val >= t: return 5 - i
        return 0
    except:
        return 0

# --- 主介面 ---
st.title("🏃‍♂️ 小學體適能評測與數據匯出")
data = load_data()

if data:
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
        v3 = st.number_input("立定跳遠 (cm)", 0)
        v4 = st.number_input("耐力跑 (米)", 0)
        
        submitted = st.form_submit_button("🌟 計算結果並生成報告")

    # 注意：所有結果顯示、運動建議、匯出按鈕，都必須在這個 if submitted 縮排內！
    if submitted:
        # 計算 BMI 與得分
        bmi = round(w / ((h/100)**2), 1)
        s1 = get_score(v1, gender, age, "sit_ups", data)
        s2 = get_score(v2, gender, age, "sit_reach", data)
        s3 = get_score(v3, gender, age, "long_jump", data)
        s4 = get_score(v4, gender, age, "run_9min", data)
        total = s1 + s2 + s3 + s4
        
        # --- 顯示結果與獎牌 ---
        st.divider()
        st.header(f"您的總分：{total} / 20 分")
        
        # 獎牌判定
        if total >= 15: st.success("🥇 獲得金獎！表現卓越！")
        elif total >= 12: st.info("🥈 獲得銀獎！繼續努力！")
        elif total >= 9: st.warning("🥉 獲得銅獎！還有進步空間！")
        else: st.error("⚪ 尚未達標，加油喔！")
        st.info(f"📊 BMI 指數: {bmi}")

        # 2. 個人化運動建議
        st.subheader("💡 專屬改善建議")
        
        # 仰臥起坐建議
        if s1 <= 2:
            st.warning("📍 **提升核心力量 (仰臥起坐)**")
            st.write("你的腹肌力量較弱。建議每天練習「平板支撐 (Plank)」30 秒，重複 3 組，有助於穩定核心肌群。")
            st.image("plank.jpeg", caption="平板支撐", width=300)

        # 坐姿體前彎建議
        if s2 <= 2:
            st.warning("📍 你的柔軟度較弱：建議練習坐姿體前彎。")
            st.image("stretch.jpg", caption="坐姿體前彎示範", width=300)

        # 立定跳遠建議
        if s3 <= 2:
            st.warning("📍 **提升爆發力 (立定跳遠)**")
            st.write("你的下肢爆發力有進步空間。建議練習「深蹲 (Squat)」或跳繩，每週 3 次，每次 3 組（每組 15 次）。")
            
        # 耐力跑建議
        if s4 <= 2:
            st.warning("📍 **提升心肺耐力 (耐力跑)**")
            st.write("建議進行規律慢跑訓練，每週兩次 15 分鐘，維持可以輕鬆呼吸的節奏。")

        st.divider()

        # 3. 準備並顯示匯出數據
        res_df = pd.DataFrame([{
            "學生": name, "性別": gender, "年齡": age,
            "BMI": bmi, "總得分": total,
            "仰臥起坐次數": v1, "體前彎距離": v2, 
            "跳遠距離": v3, "耐力跑距離": v4
        }])
        
        st.write("📋 預覽即將匯出的數據：", res_df)
        
        # 4. 下載 CSV 按鈕
        csv = res_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 下載數據報告 (CSV)",
            data=csv,
            file_name=f"{name}_體適能報告.csv",
            mime="text/csv"
        )
else:
    st.error("❌ 找不到數據庫！請確保 norms.json 存在於資料夾中。")