import streamlit as st
import pandas as pd
import re
import time
import random

# --- 1. 專業視覺佈局 (CSS 注入) ---
st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")

st.markdown("""
<style>
    /* 隱藏預設元件 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    
    /* 卡片式設計 */
    .report-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #6c757d;
        margin-bottom: 20px;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin: 20px 0;
    }
    .metric-box {
        flex: 1;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    .remedy-box { background-color: #e8f0fe; border: 1px solid #c2dbff; }
    .score-box { background-color: #e6f4ea; border: 1px solid #ceead6; }
    .highlight-num { font-size: 24px; font-weight: bold; color: #1a73e8; }
    .highlight-score { font-size: 24px; font-weight: bold; color: #188038; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心演算引擎 ---
STAR_DB = {
    "天醫(財運/Wealth)": ["13", "31", "68", "86", "49", "94", "27", "72"],
    "生氣(貴人/Noble)": ["14", "41", "67", "76", "39", "93", "28", "82"],
    "延年(事業/Carrer)": ["19", "91", "78", "87", "34", "43", "26", "62"],
    "伏位(平穩/Stable)": ["11", "22", "33", "44", "66", "77", "88", "99"],
    "絕命(凶/Risky)": ["12", "21", "69", "96", "48", "84", "37", "73"],
    "五鬼(凶/Variable)": ["18", "81", "79", "97", "36", "63", "24", "42"],
    "六煞(凶/Gossip)": ["16", "61", "47", "74", "38", "83", "29", "92"],
    "禍害(凶/Harm)": ["17", "71", "89", "98", "46", "64", "23", "32"]
}

def analyze_number(num_str):
    nums = "".join(re.findall(r'\d+', num_str))
    data = []
    total_score = 60
    for i in range(len(nums) - 1):
        pair = nums[i:i+2]
        star_name = "平穩磁場"; score = 0
        for k, v in STAR_DB.items():
            if pair in v:
                star_name = k
                score = 20 if "Wealth" in k else (15 if "Noble" in k or "Carrer" in k else (-20 if "凶" in k else 10))
                break
        data.append({"區段": pair, "星號": star_name, "分數": float(score)})
        total_score += score
    return pd.DataFrame(data), max(0, min(100, total_score))

# --- 3. 大師智慧隨機庫 ---
WHY_REMEDY = [
    "信士可知，數字乃宇宙萬物能量之體現。您原始號碼中蘊含的氣場，如同先天之命，雖有定數，卻非不可改之侷限。",
    "目前能量分布顯示，某些負向磁場（如五鬼、絕命）正潛移默化地干擾您的氣運，導致財氣不聚、元神渙散。",
    "這組數字的排列順序，暗合易經八卦之變。我將其設定為您的『開運密碼』，其原理在於每日的『重複共振』。"
]

# --- 4. 側邊欄與時效邏輯 ---
if 'pay_time' not in st.session_state: st.session_state.pay_time = None
if st.query_params.get("pay") == "success": st.session_state.pay_time = time.time()

st.sidebar.title("🔮 鑑定資料填寫")
selected_lang = st.sidebar.selectbox("Language / 語言", ["繁體中文", "English"])
raw_input = st.sidebar.text_input("請輸入鑑定之號碼：", placeholder="手機、生日、車牌")

# --- 5. 主畫面呈現 ---
st.title("🔮 數位易經能量鑑定所")

if raw_input:
    df_orig, score_orig = analyze_number(raw_input)
    
    # 判斷支付狀態 (15分鐘有效期)
    is_valid = False
    if st.session_state.pay_time:
        if time.time() - st.session_state.pay_time < 900: is_valid = True
        else: st.session_state.pay_time = None

    if is_valid:
        st.success(f"✅ 緣分已至，報告已開啟 (15分鐘內可重複查閱)")
        
        # 第一張圖：原始評分與叮嚀
        st.subheader("📜 命理師的叮嚀")
        st.write(f"「信士您好，觀您所測之號碼 {raw_input}，其能量正在隨天地運轉。」")
        st.metric("原始磁場評分", f"{score_orig} 分")
        
        with st.expander("📊 原始磁場詳細解析", expanded=True):
            st.table(df_orig)

        st.divider()

        # 第二張圖：專屬方案與能級對比
        st.subheader("🛠️ 專屬能量調和方案（大師親批）")
        st.markdown(f"### 【為何需要此數字化解？】")
        st.write(random.choice(WHY_REMEDY))
        st.caption("【大師食補方】：欲提升財運天醫能量，建議多攝取黃色系食物（如玉米、南瓜）。")
        
        # 產生化解碼
        remedy_code = "68131949" # 固定或隨機生成
        df_rem, score_rem = analyze_number(remedy_code)

        # 左右並排顯示開運碼與能級
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-box remedy-box">
                <div style="color: #4285f4; font-size: 14px;">✨ 建議開運化解碼：</div>
                <div class="highlight-num">{remedy_code}</div>
            </div>
            <div class="metric-box score-box">
                <div style="color: #34a853; font-size: 14px;">📈 化解後預期能級：</div>
                <div class="highlight-score">98.1</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 第三張圖：化解碼數據報表
        st.subheader("📋 化解碼磁場佈局報表")
        st.table(df_rem)
        st.caption("命理分析僅供參考，心誠則靈，好運自來。")
        
        if st.button("🔄 刷新感應 (15分鐘內免費)"): st.rerun()

    else:
        # 未支付狀態
        st.markdown(f"### 「信士您好，鑑定結果已出。」")
        st.metric("原始磁場總評分", f"{score_orig} 分")
        st.warning("🔒 此號碼蘊含之天機與詳細化解方案已被封印。")
        st.link_button("💳 支付 1 USD 解鎖大師報告", "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
        st.caption("⚠️ 支付完成後 15 分鐘內有效。超時需重新結緣。")
else:
    st.info("👈 請於左側輸入號碼以啟動磁場感應。")