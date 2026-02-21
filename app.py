import streamlit as st
import re
import random
import pandas as pd
from datetime import datetime

# --- 1. 介面極限清理 (專業形象) ---
CLEAN_CSS = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    button[data-testid="stBaseButton-secondary"] {display: none !important;}
    .stSelectbox div[data-baseweb="select"] {cursor: pointer;}
</style>
"""
st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")
st.markdown(CLEAN_CSS, unsafe_allow_html=True)

# --- 2. 核心：大師級 108 種語言支援與專業文本 (範例展示核心語系) ---
# 註：這裡使用字典擴展，可對應全球語系，並具備大師語氣
LANG_MASTER = {
    "繁體中文": {
        "title": "🔮 數位易經能量鑑定所",
        "input_label": "請輸入鑑定號碼 (手機、身分證、生日、車牌)：",
        "pay_msg": "🔒 鑑定報告已被封印，請解鎖查閱大師深度批示。",
        "pay_btn": "💳 支付 1 USD 領取大師化解方案",
        "master_note": "📜 命理師的叮嚀",
        "opening": "「信士您好，觀您所測之號碼 **{}**，其數位磁場如同宿命之迴響，與您的元神震盪息息相關。」",
        "reasons": [
            "【磁場衝突解析】：您原始號碼中蘊含的負向震盪正侵蝕您的財氣屏障。此種不和諧的共振，如同在逆水行舟，讓您的努力往往事倍功半。",
            "【能量斷層警告】：易經八星顯示，此組合在事業位出現了能量斷層，導致貴人遠離、小人近身。若不以特定磁場調和，恐難突破現有困局。"
        ],
        "remedy_title": "🛠️ 專屬能量調和方案",
        "diet": "【靈性能量指引】：建議多食**深綠色蔬果**（木能量）以疏肝理氣，並於每日清晨觀想此組開運碼。",
        "remedy_label": "✨ 建議開運化解碼：",
        "table_cols": ["區段", "星號", "分數"]
    },
    "English": {
        "title": "🔮 Digital I-Ching Energy Lab",
        "input_label": "Enter Number (Phone, ID, Birthday, Plate):",
        "pay_btn": "💳 Pay 1 USD for Master's Remedy",
        "master_note": "📜 Master's Spiritual Note",
        "opening": "Greetings, your number **{}** resonates with cosmic frequencies that reflect your inner destiny.",
        "reasons": [
            "[Energy Conflict]: The negative vibrations in your number are eroding your prosperity barrier. This disharmony makes your efforts feel like rowing against the tide.",
            "[Vibration Alert]: I-Ching analysis reveals an 'Energy Fault' in your career alignment, causing missed opportunities. A specific harmonic code is needed to realign your path."
        ],
        "remedy_title": "🛠️ Exclusive Energy Alignment",
        "diet": "[Spiritual Diet]: Consume more **dark green vegetables** to boost your wood energy, and visualize the remedy code daily at dawn.",
        "remedy_label": "✨ Recommended Remedy Code:"
    },
    "日本語": {
        "title": "🔮 デジタル易経エネルギー鑑定所",
        "input_label": "鑑定番号入力（携帯、身分証、誕生日、ナンバープレート）：",
        "pay_btn": "💳 1 USDを支払って鑑定書を受け取る",
        "master_note": "📜 鑑定士の助言",
        "opening": "「こんにちは、あなたの番号 **{}** は、運命の響きとして、あなたの魂の振動と深く関わっています。」",
        "reasons": [
            "【磁場衝突の解析】：元の番号に含まれる負の振動が、あなたの金運の障壁を侵食しています。この不調和は、努力が空回りする原因となります。",
            "【エネルギー断層の警告】：易経八星によると、この組み合わせは仕事運に断層を生じさせています。特定のコードで調和させる必要があります。"
        ],
        "remedy_title": "🛠️ 専用エネルギー調和案",
        "diet": "【スピリチュアル指引】：緑の野菜を多く摂り、毎朝この開運コードを瞑想することをお勧めします。"
    }
}

# --- 3. 側邊欄：語言與輸入 ---
# 支援手動選擇，您可以根據需要擴展到 108 種，或串接翻譯 API
selected_lang = st.sidebar.selectbox("🌐 Select Language / 選擇語言", list(LANG_MASTER.keys()))
L = LANG_MASTER[selected_lang]

st.sidebar.divider()
st.sidebar.subheader(L["title"])
raw_input = st.sidebar.text_input(L["input_label"], placeholder="...")

# --- 4. 演算邏輯 ---
STAR_CONFIG = {
    "天醫(Wealth)": ["13", "31", "68", "86", "49", "94", "27", "72"],
    "生氣(Noble)": ["14", "41", "67", "76", "39", "93", "28", "82"],
    "延年(Career)": ["19", "91", "78", "87", "34", "43", "26", "62"],
    "絕命(Risky)": ["12", "21", "69", "96", "48", "84", "37", "73"],
    "五鬼(Ghost)": ["18", "81", "79", "97", "36", "63", "24", "42"],
    "禍害(Harm)": ["17", "71", "89", "98", "46", "64", "23", "32"]
}

def analyze_ching(nums):
    res = []
    score = 60
    for i in range(len(nums) - 1):
        pair = nums[i:i+2]
        star_found = "平穩磁場"
        val = 0
        for star, pairs in STAR_CONFIG.items():
            if pair in pairs:
                star_found = star
                val = 20 if "Wealth" in star else (-20 if "Risky" in star or "Ghost" in star else 15)
                break
        res.append({"p": pair, "s": star_found, "v": val})
        score += val
    return res, max(0, min(100, score))

# --- 5. 主畫面呈現 ---
st.title(L["title"])

if raw_input:
    clean_nums = "".join(re.findall(r'\d+', raw_input))
    details, score = analyze_ching(clean_nums)
    
    # 支付檢查
    is_paid = st.query_params.get("pay") == "success"

    # --- 鑑定結果 (大師氣氛) ---
    st.markdown(f"### {L['master_note']}")
    st.write(L["opening"].format(raw_input))
    
    st.metric("原始磁場評分" if selected_lang=="繁體中文" else "Energy Score", f"{score} 分")

    with st.expander("📊 磁場能量分布細節" if selected_lang=="繁體中文" else "Energy Details"):
        df = pd.DataFrame(details)
        df.columns = L.get("table_cols", ["Section", "Star", "Score"])
        st.table(df)

    st.divider()

    if is_paid:
        st.success("✅ 緣分已啟，大師批示如下")
        st.subheader(L["remedy_title"])
        
        # 專業長篇解說
        st.markdown(f"#### {random.choice(L['reasons'])}")
        st.info(L["diet"])
        
        remedy_code = "".join(random.choices("136849", k=8))
        st.markdown(f"### {L.get('remedy_label', 'Code:')} `{remedy_code}`")
        st.caption("建議將此碼設為手機解鎖密碼，或書寫於紅紙隨身攜帶。")
    else:
        st.warning(L["pay_msg"])
        st.link_button(L["pay_btn"], "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
else:
    st.info("👈 請於左側輸入您的號碼，開啟改運之門。")