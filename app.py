import streamlit as st
import re
import random
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 專業介面清理與隱藏 ---
CLEAN_UI = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    /* 隱藏右下角 Manage app 按鈕的終極手段 */
    button[data-testid="stBaseButton-secondary"] {display: none !important;}
    .viewerBadge_container__1QS1n {display: none !important;}
</style>
"""

st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")
st.markdown(CLEAN_UI, unsafe_allow_html=True)

# --- 2. 深度大師解說資料庫 (多國語言) ---
CONTENT_DB = {
    "繁體中文": {
        "title": "🔮 數位易經能量鑑定所",
        "input_label": "請輸入欲鑑定之號碼 (手機、身分證、生日、車牌)：",
        "pay_msg": "🔒 鑑定報告已被封印，請解鎖查閱大師深度批示。",
        "pay_btn": "💳 支付 1 USD 解鎖專屬化解方案",
        "reasons": [
            "信士可知，數字乃宇宙能量之顯化。您原始號碼中的氣場如同先天之命，雖有定數，卻非不可改之侷限。目前的能量分佈顯示，某些負向磁場正潛移默化地干擾您的氣運，導致財氣不聚、元神渙散。",
            "在易經數位磁場中，每一個組合都是一個微型能量場。您目前的組合中，正負能量比例失衡，這就像是一個人穿了不合腳的鞋，走得再快也會感到疲憊。這組數字能為您枯竭的能量池注入活水。"
        ],
        "diets": [
            "【靈性能量指引】：除了數字調和，內在能量的清理亦至關重要。建議信士這段期間多食**深綠色蔬果（如菠菜、綠花椰菜）**，其木能量能助您疏肝理氣，強化『生氣』貴人場。",
            "【能量飲食建議】：觀您磁場火氣較旺，建議補充**根莖類食物（如地瓜、山藥）**，這類屬於『土』屬性的食物能幫助您沉穩能量、固守財庫。飲食宜清淡，避免過多紅肉。"
        ],
        "advices": [
            "【使用建議】：請將此調和碼設置為您的手機解鎖密碼。每日至少『觀想』此組數字 21 次。心誠則靈，好運自來。",
            "【大師叮嚀】：此碼乃當下機緣所得。建議將其書寫於紅紙上放置於皮夾內，這組數字將成為您的能量錨點，助您重新匯聚正磁場。"
        ],
        "result_label": "✨ 建議開運化解碼：",
        "score_label": "預期能級"
    },
    "English": {
        "title": "🔮 Digital I-Ching Energy Lab",
        "input_label": "Enter number (Phone, ID, Birthday, Plate):",
        "pay_msg": "🔒 The report is sealed. Unlock for the Master's deep analysis.",
        "pay_btn": "💳 Pay 1 USD to Unlock Remedy",
        "reasons": [
            "Numbers are manifestations of cosmic energy. Your current number's field is like a predetermined fate, but it is not unchangeable. The current distribution shows negative vibrations affecting your prosperity.",
            "In Digital I-Ching, every combination is a micro-energy field. Your current balance is slightly off, much like walking in shoes that don't fit. This new code will inject fresh vitality into your energy pool."
        ],
        "diets": [
            "[Spiritual Guidance]: Internal cleansing is vital. We suggest eating more **dark green vegetables (e.g., spinach, broccoli)** to strengthen your 'Noble' energy field.",
            "[Energy Diet Advice]: Your energy shows high 'Fire'. Root vegetables like **sweet potatoes and yams** ('Earth' element) will help stabilize your wealth and inner peace."
        ],
        "advices": [
            "[Usage Advice]: Set this code as your phone password. Visualize these numbers at least 21 times a day. Sincerity brings good fortune.",
            "[Master's Tip]: This code is a gift of the moment. Write it on red paper and keep it in your wallet to act as an energy anchor."
        ],
        "result_label": "✨ Recommended Remedy Code:",
        "score_label": "Projected Energy Level"
    }
}

# --- 3. 介面實作 ---
lang = st.sidebar.selectbox("🌐 Language / 語言", ["繁體中文", "English"])
C = CONTENT_DB[lang]

st.title(C["title"])
st.sidebar.divider()
st.sidebar.subheader("📝 鑑定資料填寫" if lang=="繁體中文" else "Data Entry")
raw_input = st.sidebar.text_input(C["input_label"])

# --- 4. 運算核心 ---
def generate_master_report():
    code = "".join(random.choices("136849", k=8))
    score = round(97.0 + random.random() * 2.5, 1)
    # 隨機組合所有消失的解說功能
    report = f"{random.choice(C['reasons'])}\n\n{random.choice(C['diets'])}\n\n{random.choice(C['advices'])}"
    return code, score, report

# --- 5. 畫面呈現邏輯 ---
if raw_input:
    # 測試開發者後門：網址加 ?pay=success 即可看到完整版
    is_paid = st.query_params.get("pay") == "success"

    if is_paid:
        st.success("✅ 緣分已至，報告已開啟" if lang=="繁體中文" else "✅ Destiny Matched. Report Unlocked.")
        st.metric("原始磁場總評分" if lang=="繁體中文" else "Original Score", "55.0 分")
        
        st.divider()
        st.subheader("🛠️ 專屬能量調和方案" if lang=="繁體中文" else "Personalized Remedy")
        
        # 呼叫完整解說功能
        r_code, r_score, r_report = generate_master_report()
        
        st.markdown(f"### **【{'大師親批' if lang=='繁體中文' else 'Master Analysis'}】**")
        st.write(r_report)
        
        st.info(f"{C['result_label']} **{r_code}** ({C['score_label']}：{r_score})")
        
        if st.sidebar.button("🔄 刷新感應" if lang=="繁體中文" else "🔄 Refresh Sensing"):
            st.rerun()
    else:
        st.warning(C["pay_msg"])
        st.link_button(C["pay_btn"], "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
else:
    st.info("👈 請於左側選單輸入您的號碼。" if lang=="繁體中文" else "👈 Please enter your number on the left.")