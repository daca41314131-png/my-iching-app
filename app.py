import streamlit as st
import re
import random
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 專業介面隱藏規則 ---
CLEAN_UI = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    button[data-testid="stBaseButton-secondary"] {display: none !important;}
</style>
"""

st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")
st.markdown(CLEAN_UI, unsafe_allow_html=True)

# --- 2. 核心：八星演算字典 ---
STAR_MAP = {
    "天醫(財運/Wealth)": {"pairs": ["13", "31", "68", "86", "49", "94", "27", "72"], "score": 20, "desc": "正財、聰明、地產"},
    "生氣(貴人/Noble)": {"pairs": ["14", "41", "67", "76", "39", "93", "28", "82"], "score": 15, "desc": "貴人、樂觀、轉機"},
    "延年(事業/Career)": {"pairs": ["19", "91", "78", "87", "34", "43", "26", "62"], "score": 15, "desc": "專業、領導、意志"},
    "伏位(平穩/Stable)": {"pairs": ["11", "22", "33", "44", "66", "77", "88", "99"], "score": 10, "desc": "蓄勢、被動、等待"},
    "絕命(凶/Risky)": {"pairs": ["12", "21", "69", "96", "48", "84", "37", "73"], "score": -20, "desc": "情緒、官司、意外"},
    "五鬼(凶/Ghost)": {"pairs": ["18", "81", "79", "97", "36", "63", "24", "42"], "score": -20, "desc": "多變、血光、智慧"},
    "六煞(凶/Gossip)": {"pairs": ["16", "61", "47", "74", "38", "83", "29", "92"], "score": -15, "desc": "桃花、糾結、憂鬱"},
    "禍害(凶/Harm)": {"pairs": ["17", "71", "89", "98", "46", "64", "23", "32"], "score": -15, "desc": "口舌、病痛、小人"}
}

# --- 3. 語言字典 ---
LANG_DB = {
    "繁體中文": {
        "title": "🔮 數位易經能量鑑定所",
        "input_label": "請輸入欲鑑定之號碼 (手機、身分證、生日、車牌)：",
        "pay_msg": "🔒 鑑定報告已被封印，請解鎖查閱大師深度解析。",
        "pay_btn": "💳 支付 1 USD 解鎖專屬化解方案",
        "table_cols": ["區段", "星號", "分數"],
        "master_note": "📜 命理師的叮嚀",
        "reasons": ["數字乃宇宙能量之顯化。您目前的能量分佈顯示財氣不聚、元神渙散。", "正負能量比例失衡，需要特定碼位中和磁場。"],
        "diet": "【能量飲食建議】：多食**深綠色蔬果**強化貴人場。",
        "remedy_label": "✨ 建議開運化解碼："
    },
    "English": {
        "title": "🔮 Digital I-Ching Energy Lab",
        "input_label": "Enter number (Phone, ID, Birthday, Plate):",
        "pay_msg": "🔒 Report sealed. Unlock for Master's analysis.",
        "pay_btn": "💳 Pay 1 USD to Unlock Remedy",
        "table_cols": ["Section", "Star", "Score"],
        "master_note": "📜 Master's Note",
        "reasons": ["Numbers are cosmic energy. Your current field shows scattered energy.", "Balance is key. This remedy will realign your frequency."],
        "diet": "[Diet Advice]: Eat more **green vegetables** to boost your Noble star.",
        "remedy_label": "✨ Recommended Remedy Code:"
    }
}

# --- 4. 邏輯引擎 ---
class IChingEngine:
    def analyze_numbers(self, nums):
        results = []
        total_score = 60
        for i in range(len(nums) - 1):
            pair = nums[i:i+2]
            found = False
            for star, info in STAR_MAP.items():
                if pair in info["pairs"]:
                    results.append({"p": pair, "s": star, "v": info["score"]})
                    total_score += info["score"]
                    found = True; break
            if not found:
                results.append({"p": pair, "s": "平穩磁場", "v": 0})
        return results, max(0, min(100, total_score))

# --- 5. 介面實作 ---
lang = st.sidebar.selectbox("🌐 Language / 語言", ["繁體中文", "English"])
L = LANG_DB[lang]
st.title(L["title"])

raw_input = st.sidebar.text_input(L["input_label"])

if raw_input:
    engine = IChingEngine()
    clean_nums = "".join(re.findall(r'\d+', raw_input))
    details, score = engine.analyze_numbers(clean_nums)
    
    # 測試後門：網址末端加 ?pay=success
    is_paid = st.query_params.get("pay") == "success"

    # --- 顯示基礎鑑定 (不論是否付費) ---
    st.markdown(f"### {L['master_note']}")
    st.write(f"「信士您好，觀您所測之號碼 **{raw_input}**，其數位磁場中蘊含之能量與您氣運息息相關。」")
    st.metric("原始磁場總評分", f"{score} 分")

    with st.expander("📊 原始磁場分佈解析"):
        df = pd.DataFrame(details)
        df.columns = L["table_cols"]
        st.table(df)

    st.divider()

    # --- 付費內容：化解方案與長篇解說 ---
    if is_paid:
        st.success("✅ 緣分已至，報告已為您開啟")
        st.subheader("🛠️ 專屬能量調和方案")
        
        # 生成隨機化解碼與解說
        remedy_code = "".join(random.choices("136849", k=8))
        st.markdown(f"**{random.choice(L['reasons'])}**")
        st.write(L["diet"])
        st.info(f"{L['remedy_label']} **{remedy_code}** (預期能級：98.5)")
    else:
        st.warning(L["pay_msg"])
        st.link_button(L["pay_btn"], "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
else:
    st.info("👈 請於左側選單輸入您的號碼。")