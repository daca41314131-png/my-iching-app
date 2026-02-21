import streamlit as st
import re
import random
import pandas as pd
import time
from datetime import datetime, timedelta

# --- 1. 專業大師介面隱藏 ---
st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stDeployButton {display:none !important;} [data-testid="stSidebarNav"] {display: none;}
    button[data-testid="stBaseButton-secondary"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# --- 2. 108 種語言名稱列表 (擴展接口) ---
LANG_LIST = ["繁體中文", "English", "日本語", "한국어", "Français", "Deutsch", "Español", "Tiếng Việt", "ไทย"] # 可自行填滿至 108 種

# --- 3. 核心：大師智慧語境庫 (確保每次說法不同) ---
MASTER_WISDOM = {
    "problems": [
        "此數字共振出『絕命』磁場，預示您近期心神焦躁，財帛宮位有虛耗之象。",
        "觀此數組，能量呈現『五鬼』混亂，身邊恐有暗流湧動，貴人受阻。",
        "數位中火氣過旺，導致您雖然努力，卻往往在臨門一腳時功敗垂成。"
    ],
    "solutions": [
        "為此，大師特別為您推演此『生氣』調和碼，旨在引動東方木能量，化解戾氣。",
        "此開運碼能校準您的元神波段，將負向磁場轉化為平穩的『延年』能量。",
        "大師建議以此數位作為能量錨點，重建您的財氣屏障，阻斷小人干擾。"
    ],
    "guidance": [
        "【靈性指引】：每日清晨對此數字觀想三遍，心誠則靈，運勢必在三七二十一天後轉化。",
        "【大師叮嚀】：運由心生，數由命定。此碼乃當下機緣，請務必妥善運用，切莫外傳。",
        "【開運建議】：近期宜清淡飲食，並將此碼設置為通訊軟體密碼，強化震盪。"
    ]
}

# --- 4. 易經八星演算引擎 ---
STAR_DB = {
    "天醫(財運)": ["13", "31", "68", "86", "49", "94", "27", "72"],
    "生氣(貴人)": ["14", "41", "67", "76", "39", "93", "28", "82"],
    "延年(事業)": ["19", "91", "78", "87", "34", "43", "26", "62"],
    "絕命(凶)": ["12", "21", "69", "96", "48", "84", "37", "73"],
    "五鬼(凶)": ["18", "81", "79", "97", "36", "63", "24", "42"],
    "六煞(凶)": ["16", "61", "47", "74", "38", "83", "29", "92"],
    "禍害(凶)": ["17", "71", "89", "98", "46", "64", "23", "32"]
}

def analyze_energy(nums):
    res = []
    score = 55
    for i in range(len(nums) - 1):
        pair = nums[i:i+2]
        star = "平穩磁場"; val = 0
        for name, pairs in STAR_DB.items():
            if pair in pairs:
                star = name; val = 20 if "財運" in name else (-15 if "凶" in name else 15)
                break
        res.append({"區段": pair, "磁場星號": star, "能量分數": val})
        score += val
    return res, max(0, min(100, score))

# --- 5. 15 分鐘支付記憶邏輯 ---
if 'payment_time' not in st.session_state:
    st.session_state.payment_time = None

# 檢查 URL 參數 (PayPal 帶回)
if st.query_params.get("pay") == "success":
    st.session_state.payment_time = time.time()

# --- 6. 主畫面呈現 ---
selected_lang = st.sidebar.selectbox("🌐 全球語言切換 / International", LANG_LIST)
st.sidebar.divider()
st.sidebar.subheader("📝 鑑定資料填寫")
raw_input = st.sidebar.text_input("請輸入欲鑑定之數字組合：")

st.title("🔮 數位易經能量鑑定所")

if raw_input:
    # 檢查是否在 15 分鐘有效期內
    is_valid = False
    if st.session_state.payment_time:
        elapsed = time.time() - st.session_state.payment_time
        if elapsed < 900:  # 900秒 = 15分鐘
            is_valid = True
        else:
            st.session_state.payment_time = None  # 超時重置

    # 計算原始數據
    details, original_score = analyze_energy("".join(re.findall(r'\d+', raw_input)))

    if is_valid:
        # --- 支付成功：專業大師報告 ---
        st.success(f"✅ 緣分存續中 (剩餘有效觀看時間：{int((900-(time.time()-st.session_state.payment_time))/60)} 分鐘)")
        
        col1, col2 = st.columns(2)
        col1.metric("原始能量評分", f"{original_score} 分")
        col2.metric("化解後預期能級", "98.5 分", delta="優化成功")

        st.markdown("---")
        st.markdown(f"### 📜 大師親批：{raw_input}")
        
        # 隨機產生不重複的解說，增加專業感
        p_text = random.choice(MASTER_WISDOM["problems"])
        s_text = random.choice(MASTER_WISDOM["solutions"])
        g_text = random.choice(MASTER_WISDOM["guidance"])
        
        st.write(f"**【磁場現況報告】**\n{p_text}")
        st.write(f"**【化解因果說明】**\n{s_text}")
        
        remedy_code = "".join(random.choices("136849", k=8))
        st.info(f"✨ 建議開運化解碼：**{remedy_code}**")
        
        st.write(g_text)

        with st.expander("📊 查看八星詳細數據分析表格"):
            st.table(pd.DataFrame(details))
            
        if st.button("🔄 重新感應能量 (解說將刷新)"):
            st.rerun()

    else:
        # --- 未支付或超時：顯示基礎數據與支付按鈕 ---
        st.markdown(f"### 「信士您好，觀您所測之號碼 **{raw_input}**，鑑定結果已出。」")
        st.metric("原始磁場總評分", f"{original_score} 分")
        
        st.warning("🔒 此號碼蘊含之天機與詳細化解方案已被封印。")
        st.write("付費解鎖後，您將獲得：\n* 1. 專業大師長篇深度解說\n* 2. 針對性開運化解碼\n* 3. 15 分鐘內無限次刷新感應不重複內容")
        
        st.link_button("💳 支付 1 USD 解鎖大師報告", "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
        st.caption("⚠️ 支付完成後 15 分鐘內有效。超時需重新結緣。")
else:
    st.info("👈 大師正待命。請於左側輸入號碼以啟動磁場感應。")