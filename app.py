import streamlit as st
import re
import random
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 極致介面清理 CSS (確保語言選單不被隱藏) ---
CLEAN_MARKUP = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    /* 修正：只隱藏內建導航，保留自定義 Widget */
    [data-testid="stSidebarNav"] {display: none;}
</style>
"""

st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")
st.markdown(CLEAN_MARKUP, unsafe_allow_html=True)

# --- 2. 多國語言字典設定 ---
LANG_DICT = {
    "繁體中文": {
        "title": "🔮 數位易經能量鑑定所",
        "input_label": "請輸入欲鑑定之號碼：",
        "placeholder": "例如：0912345678",
        "btn_refresh": "🔄 刷新當下能量感應",
        "paid_msg": "✅ 緣分已至，報告已開啟",
        "unpaid_msg": "🔒 鑑定報告已被封印",
        "pay_btn": "💳 支付 1 USD 解鎖大師報告",
        "remedy_title": "🛠️ 專屬能量調和方案",
        "reason_header": "### **【大師親批：為何需要此化解？】**",
        "advice_prefix": "✨ 建議開運化解碼：",
        "reasons": [
            "信士可知，數字乃宇宙能量之顯化。您原始號碼中的氣場如同先天之命，雖有定數，卻非不可改之侷限。",
            "在易經數位磁場中，每一個組合都是一個微型能量場。您目前的組合中，正負能量比例失衡。"
        ],
        "diets": [
            "【靈性能量指引】：建議這段期間多食**深綠色蔬果**，其木能量能助您強化貴人場。",
            "【能量飲食建議】：建議補充**根莖類食物（如地瓜、山藥）**，這類屬於『土』屬性能幫助固守財庫。"
        ]
    },
    "English": {
        "title": "🔮 Digital I-Ching Energy Lab",
        "input_label": "Enter Number to Analyze:",
        "placeholder": "e.g., +1 2345678",
        "btn_refresh": "🔄 Refresh Energy Sensing",
        "paid_msg": "✅ Destiny matched. Report unlocked.",
        "unpaid_msg": "🔒 Report is sealed.",
        "pay_btn": "💳 Pay 1 USD to unlock Master's Report",
        "remedy_title": "🛠️ Personalized Energy Remedy",
        "reason_header": "### **[Why do you need this remedy?]**",
        "advice_prefix": "✨ Recommended Remedy Code:",
        "reasons": [
            "Numbers are manifestations of cosmic energy. Your current number's field is like a predetermined fate, but it is not unchangeable.",
            "In Digital I-Ching, every combination is a micro-energy field. Your current balance is slightly off."
        ],
        "diets": [
            "[Spiritual Diet]: We suggest eating more **dark green vegetables** to strengthen your noble energy field.",
            "[Energy Diet]: Root vegetables like **sweet potatoes and yams** can help stabilize your wealth luck."
        ]
    }
}

# --- 3. 語言選擇器 (放在側邊欄最上方) ---
selected_lang = st.sidebar.selectbox("🌐 Language / 語言", ["繁體中文", "English"])
L = LANG_DICT[selected_lang]

# --- 4. 核心引擎 (延續大師解說邏輯) ---
class DigitalIChingPro:
    def __init__(self):
        self.star_config = {
            "天醫(Wealth)": ["13", "31", "68", "86", "49", "94", "27", "72"],
            "生氣(Noble)": ["14", "41", "67", "76", "39", "93", "28", "82"],
            "延年(Career)": ["19", "91", "78", "87", "34", "43", "26", "62"]
        }

    def analyze(self, nums):
        results = []
        score = 60
        for i in range(len(nums) - 1):
            pair = nums[i:i+2]
            found = False
            for star, pairs in self.star_config.items():
                if pair in pairs:
                    results.append({"Section": pair, "Star": star, "Score": 20})
                    score += 20
                    found = True; break
            if not found:
                results.append({"Section": pair, "Star": "Neutral", "Score": 0})
        return results, min(100, score)

    def generate_remedy(self):
        # 確保隨機生成且解說豐富
        code = "".join(random.choices("136849", k=8))
        explanation = f"{random.choice(L['reasons'])}\n\n{random.choice(L['diets'])}"
        return code, 98.5, explanation

# --- 5. 介面呈現 ---
st.title(L["title"])
st.sidebar.divider()
st.sidebar.subheader("📝 Settings")
raw_input = st.sidebar.text_input(L["input_label"], placeholder=L["placeholder"])

if raw_input:
    engine = DigitalIChingPro()
    clean_nums = "".join(re.findall(r'\d+', raw_input))
    details, score = engine.analyze(clean_nums)
    
    # 模擬支付狀態
    is_paid = st.query_params.get("pay") == "success"

    if is_paid:
        st.success(L["paid_msg"])
        st.metric("Energy Score", f"{score} pts")
        
        st.divider()
        st.subheader(L["remedy_title"])
        r_code, r_score, r_expl = engine.generate_remedy()
        
        st.markdown(L["reason_header"])
        st.write(r_expl)
        st.info(f"{L['advice_prefix']} **{r_code}**")
        
        if st.sidebar.button(L["btn_refresh"]):
            st.rerun()
    else:
        st.warning(L["unpaid_msg"])
        st.link_button(L["pay_btn"], "https://paypal.me/yourlink")
else:
    st.info("👈 Please enter a number to start.")