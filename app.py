import streamlit as st
import re
import random
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 專業介面清理與 SEO (完全背景化) ---
CLEAN_MARKUP = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
</style>
"""

st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")
st.markdown(CLEAN_MARKUP, unsafe_allow_html=True)

# --- 2. 多國語言專業字典 ---
LANG_DICT = {
    "繁體中文": {
        "title": "🔮 數位易經能量鑑定所",
        "sidebar_header": "📝 鑑定資料填寫",
        "input_label": "請輸入欲鑑定之號碼 (手機、身分證、生日、車牌)：",
        "placeholder": "請輸入號碼...",
        "pay_msg": "🔒 鑑定報告已被封印，請解鎖查閱大師批示。",
        "pay_btn": "💳 支付 1 USD 解鎖專屬化解方案",
        "remedy_title": "🛠️ 專屬能量調和方案",
        "master_report": "### **【大師親批：數字能量解析】**",
        "reasons": [
            "信士可知，數字乃宇宙能量之顯化。您原始號碼中的氣場如同先天之命，雖有定數，卻非不可改之侷限。",
            "在易經數位磁場中，每一個組合都是一個微型能量場。您目前的組合中，正負能量比例失衡，需以特定碼位中和。"
        ],
        "advice": "✨ 建議開運化解碼：",
        "diet_tip": "【靈性能量指引】：建議多食綠色蔬果以平衡元神磁場。"
    },
    "English": {
        "title": "🔮 Digital I-Ching Energy Lab",
        "sidebar_header": "📝 Data Entry",
        "input_label": "Enter number (Phone, ID, Birthday, Plate):",
        "placeholder": "Type numbers here...",
        "pay_msg": "🔒 The report is sealed. Unlock to see the Master's advice.",
        "pay_btn": "💳 Pay 1 USD to Unlock Remedy",
        "remedy_title": "🛠️ Personalized Energy Remedy",
        "master_report": "### **[Master's Spiritual Analysis]**",
        "reasons": [
            "Numbers are the manifestation of cosmic energy. Your original field is like destiny, which can be harmonized.",
            "In Digital I-Ching, every combination is a micro-energy field. Your current balance needs a specific frequency to align."
        ],
        "advice": "✨ Recommended Remedy Code:",
        "diet_tip": "[Spiritual Advice]: Eating more green vegetables will help balance your inner energy field."
    }
}

# --- 3. 介面配置 ---
selected_lang = st.sidebar.selectbox("🌐 Language / 語言", ["繁體中文", "English"])
L = LANG_DICT[selected_lang]

st.title(L["title"])
st.sidebar.divider()
st.sidebar.subheader(L["sidebar_header"])
selected_type = st.sidebar.selectbox("選擇類型 / Type", ["手機號碼", "身分證字號", "出生日期", "車牌號碼"])
raw_input = st.sidebar.text_input(L["input_label"], placeholder=L["placeholder"])

# --- 4. 核心邏輯 ---
class DigitalIChingPro:
    def analyze(self, nums):
        # 模擬易經八星解析
        results = []
        score = 55.0  # 基礎分
        if len(nums) >= 2:
            pair = nums[-2:]
            results.append({"區段/Section": pair, "星號/Star": "感應中...", "分數/Score": 10.0})
        return results, score

    def generate_remedy(self):
        # 生成隨機化解碼與專業解說
        code = "".join(random.choices("136849", k=8))
        explanation = f"{random.choice(L['reasons'])}\n\n{L['diet_tip']}"
        return code, 98.5, explanation

# --- 5. 執行與呈現 ---
if raw_input:
    engine = DigitalIChingPro()
    clean_nums = "".join(re.findall(r'\d+', raw_input))
    
    # 檢查 URL 參數是否模擬支付成功 (測試用)
    is_paid = st.query_params.get("pay") == "success"

    if is_paid:
        st.success("✅ 緣分已至，報告已開啟")
        details, score = engine.analyze(clean_nums)
        st.metric("原始磁場總評分", f"{score} 分")
        
        st.divider()
        st.subheader(L["remedy_title"])
        r_code, r_score, r_expl = engine.generate_remedy()
        st.markdown(L["master_report"])
        st.write(r_expl)
        st.info(f"{L['advice']} **{r_code}** (預期能級：{r_score})")
    else:
        st.warning(L["pay_msg"])
        # 使用您提供的 PayPal 連結
        st.link_button(L["pay_btn"], "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
else:
    st.info("👈 請於左側選單輸入您的號碼，開啟命運之門。")