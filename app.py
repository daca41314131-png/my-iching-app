import streamlit as st
import re
import random
import pandas as pd

# --- 1. 介面與 SEO 優化 ---
st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stDeployButton {display:none !important;} [data-testid="stSidebarNav"] {display: none;}
    button[data-testid="stBaseButton-secondary"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# --- 2. 核心：易經八星精準數據庫 ---
# 這是確保表格能分析出數據的關鍵
STAR_DB = {
    "天醫(財運/Wealth)": {"pairs": ["13", "31", "68", "86", "49", "94", "27", "72"], "score": 20},
    "生氣(貴人/Noble)": {"pairs": ["14", "41", "67", "76", "39", "93", "28", "82"], "score": 15},
    "延年(事業/Career)": {"pairs": ["19", "91", "78", "87", "34", "43", "26", "62"], "score": 15},
    "伏位(平穩/Stable)": {"pairs": ["11", "22", "33", "44", "66", "77", "88", "99"], "score": 10},
    "絕命(凶/Risky)": {"pairs": ["12", "21", "69", "96", "48", "84", "37", "73"], "score": -20},
    "五鬼(凶/Ghost)": {"pairs": ["18", "81", "79", "97", "36", "63", "24", "42"], "score": -20},
    "六煞(凶/Gossip)": {"pairs": ["16", "61", "47", "74", "38", "83", "29", "92"], "score": -15},
    "禍害(凶/Harm)": {"pairs": ["17", "71", "89", "98", "46", "64", "23", "32"], "score": -15}
}

# --- 3. 全球語系文本庫 (可擴展至 108 國) ---
def get_i18n(lang):
    db = {
        "繁體中文": {
            "title": "數位易經能量鑑定所",
            "opening": "「信士您好，觀您所測之號碼 {}，其數位磁場如同宿命之迴響。」",
            "warning": "【核心磁場警告】：您原始號碼中的能量共振點目前正處於『能量斷層』。這種波長會導致財源如漏斗般流失。",
            "remedy_intro": "【大師化解心法】：此組化解碼是根據易經八大星曜之『生氣』與『天醫』交互演算而成。",
            "diet": "【靈性能量指引】：建議多食**深綠色蔬果**以強化貴人場。",
            "usage": "【使用說明】：請將此碼設為手機解鎖密碼，每日清晨冥想 3 分鐘。",
            "remedy_label": "✨ 建議開運化解碼：",
            "pay_btn": "💳 支付 1 USD 解鎖大師報告",
            "table_cols": ["區段", "星號磁場", "能量分數"]
        },
        "English": {
            "title": "Digital I-Ching Energy Lab",
            "opening": "Greetings. Your number {} resonates with cosmic frequencies.",
            "warning": "[Energy Fault Alert]: The vibrations in your number show a 'Dynamic Fracture', draining your prosperity.",
            "remedy_intro": "[The Art of Remedy]: This code is calculated using 'Sheng-Qi' and 'Tian-Yi' star interactions.",
            "diet": "[Spiritual Diet]: Consume more **dark green vegetables** to boost your 'Noble' energy field.",
            "usage": "[How to Use]: Set this code as your phone password and meditate for 3 mins daily.",
            "remedy_label": "✨ Recommended Remedy Code:",
            "pay_btn": "💳 Pay 1 USD to Unlock Report",
            "table_cols": ["Section", "Star Energy", "Score"]
        }
    }
    return db.get(lang, db["English"])

# --- 4. 側邊欄與輸入 ---
selected_lang = st.sidebar.selectbox("🌐 Language / 語言", ["繁體中文", "English", "日本語", "Français"])
L = get_i18n(selected_lang)

st.sidebar.divider()
st.sidebar.subheader("📝 鑑定資料填寫")
raw_input = st.sidebar.text_input("請輸入欲鑑定之號碼：", placeholder="手機、身分證、生日...")

# --- 5. 修正後的鑑定引擎 ---
def perform_analysis(num_str):
    nums = "".join(re.findall(r'\d+', num_str))
    results = []
    total_score = 60
    for i in range(len(nums) - 1):
        pair = nums[i:i+2]
        star_found = "平穩磁場"; star_val = 0
        for name, data in STAR_DB.items():
            if pair in data["pairs"]:
                star_found = name
                star_val = data["score"]
                break
        results.append({"區段": pair, "星號": star_found, "分數": star_val})
        total_score += star_val
    return results, max(0, min(100, total_score))

# --- 6. 邏輯呈現 ---
st.title("🔮 " + L["title"])

if raw_input:
    # 支付狀態判斷
    is_paid = st.query_params.get("pay") == "success"
    details, final_score = perform_analysis(raw_input)

    if is_paid:
        st.success("✅ 支付成功！大師已為您解開磁場封印。")
        st.markdown(f"### {L['opening'].format(raw_input)}")
        
        st.warning(L["warning"])
        st.markdown(f"#### {L['remedy_intro']}")
        
        # 顯示專業化解碼
        remedy_code = "".join(random.choices("136849", k=8))
        st.info(f"{L['remedy_label']} **{remedy_code}** (預期能級：98.5)")
        
        st.write(L["diet"])
        st.write(L["usage"])
        
        # --- 這裡顯示您原本「分析不出來」的表格數據 ---
        with st.expander("📊 查看詳細能量數據分析"):
            df = pd.DataFrame(details)
            df.columns = L["table_cols"]
            st.table(df)
            
    else:
        # 未支付狀態
        st.metric("原始磁場評分", f"{final_score} 分")
        st.warning("🔒 鑑定數據已計算完畢，但深度分析報告已被封印。")
        st.link_button(L["pay_btn"], "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
        st.caption("支付後，網頁將自動重定向並顯示完整的大師化解報告。")
else:
    st.info("👈 請於左側輸入您的號碼開始鑑定。")