with st.sidebar:
    st.markdown("### 正覺蓮社學校\n### 體育組")
    st.divider()
    
    # 修正重點 1: 首頁通常直接寫檔案名
    st.page_link("🏠_首頁.py", label="首頁", icon="🏠")
    
    # 修正重點 2: 檢查 pages/ 資料夾入面嘅檔名
    # 請確保左邊 pages/ 資料夾入面個名同下面一字不差
    try:
        st.page_link("pages/1_📊_體適能評測.py", label="體適能評測", icon="📊")
        st.page_link("pages/02_🔐_管理後台.py", label="老師管理後台", icon="🔐")
        st.page_link("pages/03_🏸_器材管理.py", label="器材管理", icon="🏸")
        st.page_link("pages/04_⭐_體育之星.py", label="體育之星", icon="⭐")
    except Exception as e:
        st.error(f"側邊欄連結出錯：{e}")




